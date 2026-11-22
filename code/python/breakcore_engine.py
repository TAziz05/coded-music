"""A steady-breakcore song builder. Every sound is code: drums, instruments and ambience (rain, thunder, wind...).
Songs are described as settings (see seasons.py); build(cfg) renders one to MP3."""
import subprocess
import numpy as np, scipy.signal as ss
from scipy.io import wavfile
from engine import *
from engine import reverb_ir
from instruments2 import guitar, chorus, voice, ks, envN
from songs import piano, slice_fx, ride
from songs3 import glock, mallet, flute
from songs5 import violins, harp
from songs7 import stretch2

# ---------------- chords ----------------
NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
QUAL = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10], 'm9': [0, 3, 7, 10, 14],
        'maj9': [0, 4, 7, 11, 14], 'add9': [0, 4, 7, 14], 'sus4': [0, 5, 7], '7sus': [0, 5, 7, 10], '6': [0, 4, 7, 9]}
def chord(name):
    r = name[:2] if len(name) > 1 and name[1] in '#b' else name[:1]; q = name[len(r):]
    pc = NOTE[r]; base = 52 + (pc - 4) % 12          # chord tones start between E3 and D#4
    tones = [base + i for i in QUAL[q]]
    return tones, 36 + pc - (12 if pc >= 8 else 0)   # tones, bass root (G#1..G2)

# ---------------- break kits ----------------
def make_kit(st, kit):
    """kit: dict with 'K','S','G' (two bars of kick/snare/ghost steps), 'hat' style, crunch, tone."""
    BM = Mix(32 * st)
    for bar in (0, 1):
        o = bar * 16 * st
        for k in kit['K'][bar]: kick(BM, o + k * st, 1., punch=kit.get('punch', 1.1))
        for k in kit['S'][bar]: snare(BM, o + k * st, .95); clap(BM, o + k * st, kit.get('clap', .25))
        for k in kit['G'][bar]: snare(BM, o + k * st, .16)
        h = kit.get('hat', 'ride')
        if h == 'ride':
            for k in range(0, 16, 2): ride(BM, o + k * st, .9 if k % 4 == 0 else .6)
        elif h == 'hats16':
            for k in range(16): hat(BM, o + k * st, .45 if k % 2 == 0 else .25, open_=(k == 14))
        elif h == 'hats8':
            for k in range(0, 16, 2): hat(BM, o + k * st, .5 if k % 4 == 2 else .32)
        if kit.get('shaker'):
            for k in range(16): shaker(BM, o + k * st, .5 if k % 2 else .25)
    x = np.tanh(BM.buses['drums'] * kit.get('crunch', 1.6)) / 1.2
    if kit.get('tone'): x = np.array([lp(c, kit['tone']) for c in x])
    n = int(st * SR); return [x[:, i * n:(i + 1) * n].copy() for i in range(32)], n

PATS = {
 'P0': list(range(24)) + [8, 9, 10, 11, 28, 29, 28, 31],
 'P1': [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 4, 5, 22, 23, 24, 25, 10, 11, 12, 13, 12, 15],
 'P2': [0, 1, 16, 17, 4, 5, 6, 7, 0, 1, 10, 11, 12, 13, 4, 15, 16, 17, 18, 19, 20, 21, 4, 23, 24, 25, 10, 11, 28, 29, 12, 12],
 'P3': [0, 1, 2, 3, 4, 5, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 2, 3, 20, 21, 20, 21, 24, 25, 26, 27, 12, 12, 30, 31],
 'P4': [0, 1, 2, 3, 12, 13, 6, 7, 8, 9, 2, 3, 12, 13, 14, 15, 16, 17, 18, 19, 12, 13, 22, 23, 0, 1, 26, 27, 12, 13, 12, 13]}
HALF = [0, 2, 4, 6, 8, 10, 12, 14, 16, 3, 20, 22, 24, 26, 28, 31]

# ---------------- ambience (all code) ----------------
def amb_rain(M, T, vol=1.):
    N = int(T * SR); bed = bp(noise(N), 700, 7000) * .12
    bed *= 1 + .2 * np.sin(2 * np.pi * .07 * tarr(N))
    drops = np.zeros(N); pos = rng.integers(0, N, int(T * 25)); drops[pos] = rng.uniform(.2, 1, len(pos))
    drops = bp(ss.lfilter([1], [1, -.9], drops), 2000, 9000) * .35
    M.add('amb', 0, (bed + drops) * vol, (np.roll(bed, 997) + np.roll(drops, 1777)) * vol)
def amb_thunder(M, t, vol=1.):
    N = int(5 * SR); tt = tarr(N)
    crack = hp(noise(N), 1500) * np.exp(-tt / .08) * .6
    rum = lp(lp(noise(N), 180), 120) * np.clip(tt / .3, 0, 1) * np.exp(-tt / 1.6) * 3.
    M.add('amb', t, (crack + rum) * vol)
def amb_wind(M, T, vol=1.):
    N = int(T * SR); x = noise(N); out = np.zeros(N); c = int(.25 * SR)
    for i in range(0, N, c):
        fc = 500 + 900 * (.5 + .5 * np.sin(2 * np.pi * i / SR * .11)) + 300 * np.sin(2 * np.pi * i / SR * .37)
        seg = bp(x[max(0, i - 3000):i + c], fc * .7, fc * 1.5)[-min(c, N - i):]; out[i:i + len(seg)] = seg
    gust = .5 + .5 * np.sin(2 * np.pi * .05 * tarr(N)) ** 2
    out = lp(out, 3000) * gust * .5
    M.add('amb', 0, out * vol, np.roll(out, 4410) * vol)
def amb_birds(M, T, vol=1.):
    t = 1.
    while t < T - 1:
        for j in range(rng.integers(2, 5)):
            N = int(.09 * SR); tt = tarr(N); f0 = rng.uniform(2800, 4200)
            f = f0 * (1 + .25 * np.sin(np.pi * tt / .09)); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / .09)
            M.add('amb', t + j * .12, x * vol * .12, pan=rng.uniform(-.7, .7))
        t += rng.uniform(1.5, 4.)
def amb_cicadas(M, T, vol=1.):
    N = int(T * SR); tt = tarr(N); x = bp(noise(N), 4000, 6500) * (.5 + .5 * np.sign(np.sin(2 * np.pi * 32 * tt)))
    x *= (.5 + .5 * np.sin(2 * np.pi * .1 * tt)) * .1
    M.add('amb', 0, x * vol, np.roll(x, 2000) * vol)
def amb_leaves(M, T, vol=1.):
    t = .5
    while t < T - 1:
        N = int(rng.uniform(.3, .8) * SR); tt = tarr(N); x = bp(noise(N), 2000, 8000) * np.sin(np.pi * tt / tt[-1]) ** 2
        x *= (rng.random(N) > .6) * 1.5
        M.add('amb', t, lp(x, 7000) * vol * .1, pan=rng.uniform(-.6, .6)); t += rng.uniform(1., 3.)
def amb_foghorn(M, times, vol=1.):
    for t in times:
        N = int(4 * SR); tt = tarr(N); f = mtof(38)
        x = lp(saw(f, N) + saw(f * 1.5, N) * .5, 400) * np.clip(tt / .6, 0, 1) * np.where(tt < 2.5, 1., np.exp(-(tt - 2.5) / .4))
        M.add('amb', t, x * vol * .25)
def amb_drone(M, T, n, vol=1.):
    N = int(T * SR); x = lp(saw(mtof(n), N) + saw(mtof(n + 7) * 1.002, N), 300) * .1
    M.add('amb', 0, x * vol, np.roll(x, 3000) * vol)
def amb_bells(M, T, st, vol=1.):   # sleigh bells on every 8th
    t = 0.
    while t < T:
        N = int(.2 * SR); x = np.zeros(N)
        for o in rng.uniform(0, .025, 4):
            i = int(o * SR); x[i:] += bp(noise(N - i), 6000, 12000) * np.exp(-tarr(N - i) / .04)
        M.add('amb', t, x * vol * .18, pan=.4); t += 2 * st
def vinyl(M, T, vol=1.):
    N = int(T * SR); d = np.zeros(N); pos = rng.integers(0, N, int(T * 6)); d[pos] = rng.uniform(-.7, .7, len(pos))
    M.add('amb', 0, (lp(d, 6000) * .3 + hp(noise(N), 3000) * .006) * vol)

# ---------------- instruments ----------------
def b808(M, t, n, dur, vol, glide=None):
    N = int((dur + .05) * SR); tt = tarr(N); f = mtof(n) * (1 + 1.2 * np.exp(-tt / .015))
    if glide: f = f * 2 ** (((glide - n) * np.exp(-tt / .06)) / 12)
    x = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 1.8) * envN(N, dur, .003, .5, .85, .05)
    M.add('sub', t, lp(x, 1200) * vol)
def subbass(M, t, n, dur, vol, drive=2.5):
    N = int((dur + .04) * SR); x = np.tanh(sine(mtof(n), N) * drive) * envN(N, dur, .004, .3, .9, .03); M.add('sub', t, lp(x, 900) * vol)
def reese(M, t, n, dur, vol):
    N = int((dur + .05) * SR); tt = tarr(N); f = mtof(n)
    x = saw(f * 2 ** (-.14 / 12), N) + saw(f * 2 ** (.14 / 12), N); lo = lp(x, 250); hi = lp(x, 1200)
    m = .5 + .5 * np.sin(2 * np.pi * .4 * (tt + t)); y = np.tanh((lo + (hi - lo) * m) * 1.4) * .5 * envN(N, dur, .01, .3, .9, .05)
    M.add('sub', t, y * vol + sine(f / 2, N) * envN(N, dur, .005, .3, .95, .04) * vol * .9)

def taiko(M, t, vol=1., n=36):
    N = int(1.2 * SR); tt = tarr(N); f = mtof(n) * (1 + .4 * np.exp(-tt / .03))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .35) + lp(noise(N), 900) * np.exp(-tt / .04) * .8
    M.add('perc', t, np.tanh(x * 1.5) * vol * .8)
def gong(M, t, vol=1.):
    N = int(4 * SR); tt = tarr(N); x = np.zeros(N)
    for r, a, d in ((1, 1, 2.5), (1.48, .6, 1.8), (2.1, .45, 1.2), (2.76, .3, .9), (3.4, .2, .6)):
        x += a * np.sin(2 * np.pi * 110 * r * tt * (1 + .002 * np.sin(2 * np.pi * 3 * tt))) * np.exp(-tt / d)
    M.add('perc', t, x * np.clip(tt / .05, 0, 1) * vol * .3)
def koto(M, t, n, dur, vol, pan=0.):
    y = ks(mtof(n), min(dur, 2.) + .3, .85, .9975); N = len(y); tt = tarr(N)
    bend = np.interp(np.clip(np.cumsum(1 + .003 * np.exp(-tt / .05)), 0, N - 1), np.arange(N), y)
    M.add('keys', t, lp(bend, 6500) * vol * .5, pan=pan)
def shaku(M, t, n, dur, vol, pan=0.):
    N = int((dur + .15) * SR); tt = tarr(N)
    bend = -1.2 * np.exp(-tt / .08) + np.clip((tt - .3) / .3, 0, 1) * .25 * np.sin(2 * np.pi * 4.5 * tt)
    f = mtof(n + bend); x = sine(f, N) + .2 * sine(2 * f, N) + bp(noise(N), 800, 4500) * (.12 + .15 * np.exp(-tt / .1))
    M.add('mel', t, x * envN(N, dur, .06, .3, .85, .12) * vol * .35, pan=pan)
def rage(M, t, n, dur, vol, bus='mel'):
    N = int((dur + .05) * SR); x = np.zeros(N)
    for d in (-.3, -.18, -.06, .06, .18, .3, 0): x += saw(mtof(n + d), N)
    x = np.tanh(x * .9) ; x = lp(hp(x, 180), 6000) * envN(N, dur, .003, .2, .85, .04)
    M.add(bus, t, x * vol * .25)
def crunch_lead(M, t, n, dur, vol):
    y = ks(mtof(n), dur + .05, .6, .9993); y = np.tanh(y * 2.8) * .5; y = lp(hp(y, 90), 3800)
    M.add('mel', t, y * vol * .5)
def chick(M, t, notes, vol, pan=.4):
    L = int(.12 * SR); y = np.zeros(L)
    for j, n in enumerate(notes):
        k = ks(mtof(n), .08, .7, .97); o = int(j * .003 * SR); y[o:o + len(k)] += k[:L - o]
    M.add('keys', t, hp(y, 300) * np.exp(-tarr(L) / .03) * vol, pan=pan)

def play_keys(M, kind, t0, st, tones, root, vol, bar_in_chord):
    if callable(kind): return kind(M, t0, st, tones, root, vol, bar_in_chord)   # a song can bring its own instrument
    arp = [tones[0], tones[1], tones[2], tones[-1], tones[1] + 12, tones[2] + 12, tones[-1], tones[1]]
    if kind == 'piano':
        if bar_in_chord == 0: piano(M, 'keys', t0, root + 12, 16 * st * 2, .7 * vol, pan=-.2)
        for k in range(8): piano(M, 'keys', t0 + k * 2 * st, arp[k], 2 * st * 3, .4 * vol, pan=-.1 + (k % 2) * .2)
    elif kind == 'ep':
        for s in (0, 3, 6, 10, 12):
            for j, c in enumerate(tones[:4]): epiano(M, 'keys', t0 + s * st + j * .006, c, st * (2.4 if s in (0, 6) else 1.3), .08 * vol, pan=(j - 1.5) * .2)
    elif kind == 'guitar':
        for k in range(8): guitar(M, 'keys', t0 + k * 2 * st, arp[k] + 12, 2 * st * 3, .5 * vol, pan=(-.4 if k % 2 else .4), bright=.6, decay=.998)
    elif kind == 'nylon':
        for k in range(8): guitar(M, 'keys', t0 + k * 2 * st, arp[k], 2 * st * 3, .55 * vol, pan=(-.3 if k % 2 else .3), bright=.35, decay=.997)
    elif kind == 'pluck':
        pat = [0, 1, 2, 3, 4, 3, 2, 1] * 2
        for k in range(16): pluck(M, 'keys', t0 + k * st, arp[pat[k]] + 12, st * .9, .13 * vol, pan=(-.4, .4)[k % 2], dec=.07)
    elif kind == 'harp':
        for k in range(8): harp(M, t0 + k * 2 * st, arp[k] + 12, .9 * vol, pan=-.35 + k * .1)
    elif kind == 'funk':
        for k in range(16):
            if k % 4 in (1, 3) or k % 4 == 2: chick(M, t0 + k * st, tones + [tones[0] + 12], (.18 if k % 2 else .11) * vol)
    elif kind == 'koto':
        pat = [0, 2, 4, 3, 1, 3, 5, 4]
        for k in range(8): koto(M, t0 + k * 2 * st, arp[pat[k] % 8] + 12, 2 * st * 3, .9 * vol, pan=(-.35 if k % 2 else .35))
    elif kind == 'celesta':
        for k in range(8): glock(M, t0 + k * 2 * st, arp[k] + 24, .25 * vol, pan=(-.4 if k % 2 else .4))

def play_mel(M, kind, t, n, dur, vol):
    if callable(kind): return kind(M, t, n, dur, vol)
    if kind == 'piano': piano(M, 'mel', t, n, dur, .62 * vol, pan=.15)
    elif kind == 'glock': glock(M, t, n, .8 * vol, pan=.15)
    elif kind == 'flute': flute(M, 'mel', t, n, dur * .95, 1.1 * vol, pan=.1)
    elif kind == 'lead': supersaw(M, 'mel', t, n, dur * .95, .22 * vol, cut=3200, a=.01, r=.15, voices=5)
    elif kind == 'darklead': supersaw(M, 'mel', t, n, dur * .95, .2 * vol, cut=1800, a=.02, r=.2, voices=5, detune=.25)
    elif kind == 'vibes': mallet(M, 'mel', t, n, dur, 1.2 * vol, ratio=4., dec=1., trem=.35)
    elif kind == 'voice': voice(M, 'mel', t, n, dur * .95, .8 * vol)
    elif kind == 'strings': violins(M, t, n, dur * .97, .7 * vol, att=.08, bus='mel')
    elif kind == 'brass': brass(M, 'mel', t, n, dur * .92, .45 * vol)
    elif kind == 'guitar': guitar(M, 'mel', t, n, dur * 1.3, .5 * vol, bright=.7, decay=.999)
    elif kind == 'crunch': crunch_lead(M, t, n, dur * .95, vol)
    elif kind == 'rage': rage(M, t, n, dur * .95, vol)
    elif kind == 'shaku': shaku(M, t, n, dur * .95, 1.1 * vol)
    elif kind == 'koto': koto(M, t, n, dur, 1.1 * vol, pan=.15)

# ---------------- the builder ----------------
SECTIONS = [('intro', 8), ('build', 4), ('dropA', 16), ('half', 8), ('dropB', 16), ('outro', 8)]
TARGET = {'intro': -18., 'build': -16.5, 'dropA': -12.5, 'half': -14.5, 'dropB': -12., 'outro': -18.}

def build(cfg):
    st = 60 / cfg['bpm'] / 4; B = 16 * st; R = np.random.default_rng(cfg.get('seed', 7))
    slices, n = make_kit(st, cfg['kit'])
    SECS = cfg.get('sections', SECTIONS); TG = dict(TARGET, **cfg.get('targets', {}))
    end = cfg.get('ending', 'button'); full_out = end in ('dropout', 'tapestop'); te = None
    plan = [(s, i, nb) for s, nb in SECS for i in range(nb)]
    T = len(plan) * B + 5; M = Mix(T)
    put = lambda t, sl, g=1.: M.add('break', t, sl[0] * g, sl[1] * g)
    ch = [chord(c) for c in cfg['chords']]          # 4 chords, 2 bars each
    prev = None; starts = {}
    for b, (sec, i, nb) in enumerate(plan):
        t0 = b * B; starts.setdefault(sec, t0)
        ci = (b // 2) % 4; tones, root = ch[ci]; half = b % 2
        kv = {'intro': 1.2, 'build': 1., 'dropA': .85, 'half': 1., 'dropB': .85, 'outro': 1.2}[sec]
        if sec == 'outro' and full_out: kv = .85
        play_keys(M, cfg['keys'], t0, st, tones, root, kv, half)
        if cfg.get('pad') and half == 0 and not (sec == 'outro' and end == 'dropout' and i >= 4):
            for nn in tones[1:4]: supersaw(M, 'pad', t0, nn + 12, 2 * B, cfg['pad'] * (1.4 if sec in ('intro', 'outro', 'half') else 1.), cut=cfg.get('padcut', 1400), a=.5, r=.8, voices=3)
        mel = cfg['melody'][ci]
        out_mel = sec == 'outro' and full_out and (end == 'tapestop' or i < 2)
        if half == 0 and (sec in ('dropA', 'dropB', 'half') or (sec == 'intro' and i >= 4) or out_mel):
            mk = cfg['mel'] if sec not in ('dropB', 'outro') else cfg.get('melB', cfg['mel'])
            mv = .75 if sec in ('intro', 'half') else 1.
            for s, nn, L in mel:
                play_mel(M, mk, t0 + s * st, nn + (cfg.get('upB', 0) if sec == 'dropB' else 0), L * st, mv)
                if sec == 'dropB' and cfg.get('layerB'): play_mel(M, cfg['layerB'], t0 + s * st, nn - 12, L * st, .7)
        if cfg.get('extra'): cfg['extra'](M, sec, i, t0, st, tones, root)   # per-bar extras (e.g. tabla)
        # ---- breaks ----
        if sec == 'build':
            fc = 400 * (12 ** ((i + .5) / 4))
            for k in range(16):
                sl = slices[(b % 2) * 16 + k]
                if i == 3 and k >= 12: sl = slice_fx(slices[4], n, 'roll', 2 if k < 14 else 4)
                put(t0 + k * st, np.array([lp(c, fc) for c in sl]), .55 + .12 * i)
            if i == 0: riser(M, t0, 4 * B, .5)
        if cfg.get('taiko') and sec in ('build', 'dropA', 'dropB', 'half'):
            for s in ((0, 8) if sec != 'build' else (0, 4, 8, 12)): taiko(M, t0 + s * st, .9 if s == 0 else .6)
        if cfg.get('gong') and sec in ('dropA', 'dropB', 'half') and i == 0: gong(M, t0, .9)
        out_brk = sec == 'outro' and full_out and (end == 'tapestop' or i < 6)
        if sec in ('dropA', 'dropB') or out_brk:
            if i == 0 and sec != 'outro': crash(M, t0, .85); impact(M, t0, .6)
            if i == 8: crash(M, t0, .5)
            pat = PATS[cfg['patA'] if sec == 'dropA' else cfg['patB']]
            if sec == 'outro' and end == 'dropout' and i >= 4: pat = [0 if k_ % 8 == 0 else (2 if k_ % 2 == 0 else 3) for k_ in range(32)]   # thinned: just kick and hats
            for k in range(16):
                sl = slices[pat[(b % 2) * 16 + k]]
                if half == 1 and i % 4 == 3 and k >= 14: sl = slice_fx(slices[12], n, 'roll', 2 if k == 14 else 4)
                put(t0 + k * st, sl)
            bk = cfg['bass'] if not (sec == 'outro' and end == 'dropout' and i >= 4) else None
            if bk == '808':
                for s, L in ((0, 7), (7, 3), (10, 6)): b808(M, t0 + s * st, root, L * st * .95, .55, glide=prev if (s == 0 and half == 0 and prev and prev != root) else None)
            elif bk == 'sub':
                for s, L in ((0, 6), (6, 2), (10, 6)): subbass(M, t0 + s * st, root, L * st * .95, .5, 2.5 if sec == 'dropA' else 3.5)
            elif bk == 'reese':
                for s, L in ((0, 6), (6, 2), (8, 3), (11, 1), (12, 4)): reese(M, t0 + s * st, root + 12, L * st * .95, .45)
            prev = root
        if sec == 'half':
            for k in range(0, 16, 2): put(t0 + k * st, stretch2(slices[HALF[(b % 2) * 8 + k // 2]], n), .85)
            subbass(M, t0, root, B * .95, .45, 1.5)
            if i == nb - 1: riser(M, t0, B, .45)
        if sec == 'outro' and i < 4 and not full_out:
            for k in range(0, 16, 4): put(t0 + k * st, np.array([lp(c, 1500 - 300 * i) for c in slices[(b % 2) * 16 + k]]), .45 - .08 * i)
        if sec == 'outro' and i == nb - 1 and cfg.get('ending') == 'roll':   # rolled-chord ending (plucked, harp-like)
            tones0, r0 = ch[0]; play_mel(M, cfg['mel'], t0 + B, tones0[0] + 12, 3., .8)
            for j, nn in enumerate([r0 + 12] + tones0): piano(M, 'keys', t0 + B + j * .04, nn, 3., .3) if cfg['keys'] == 'piano' else guitar(M, 'keys', t0 + B + j * .04, nn + 12, 3., .35, bright=.5)
        elif sec == 'outro' and end == 'custom' and i == 0: cfg['ending_fn'](M, t0, st, B, nb, ch)
        elif sec == 'outro' and end == 'tapestop' and i == 0: te = t0 + cfg.get('stop_bar', 4) * B
        elif sec == 'outro' and end == 'dropout' and i == nb - 1:   # last one standing: a soft final chord on the keys alone
            tones0, r0 = ch[0]
            for nn in [r0 + 12] + tones0:
                if cfg['keys'] == 'piano': piano(M, 'keys', t0 + B, nn, 3.5, .26)
                else: epiano(M, 'keys', t0 + B, nn + 12, 3., .08)
        elif sec == 'outro' and i == nb - 1 and end == 'button':   # the ending: one 'button' hit with the whole band, then let it ring
            tones0, r0 = ch[0]; te = t0 + B
            kick(M, te, .8, punch=1.2); crash(M, te, .6); impact(M, te, .35)
            subbass(M, te, r0, 2.2, .55, 1.6)
            for nn in tones0: supersaw(M, 'pad', te, nn + 12, 2.5, cfg.get('pad', .06) * 2.2, cut=cfg.get('padcut', 1400), a=.02, r=1.2, voices=3)
            for nn in [r0 + 12] + tones0:
                if cfg['keys'] == 'piano': piano(M, 'keys', te, nn, 3., .32)
                else: epiano(M, 'keys', te, nn + 12, 2.5, .09)
            play_mel(M, cfg['mel'], te, tones0[-1] + 12 if tones0[-1] < 72 else tones0[-1], 2.5, .8)
    # ---- ambience ----
    Ttot = len(plan) * B + 4
    for a in cfg.get('amb', []):
        kind, vol = a
        if kind == 'rain': amb_rain(M, Ttot, vol)
        elif kind == 'thunder':
            for s in ('intro', 'dropA', 'half', 'dropB'): amb_thunder(M, starts[s] + (B * 2 if s == 'intro' else 0), vol)
        elif kind == 'wind': amb_wind(M, Ttot, vol)
        elif kind == 'birds': amb_birds(M, Ttot, vol)
        elif kind == 'cicadas': amb_cicadas(M, Ttot, vol)
        elif kind == 'leaves': amb_leaves(M, Ttot, vol)
        elif kind == 'foghorn': amb_foghorn(M, [starts['intro'] + B, starts['half'], starts['outro'] + B * 2], vol)
        elif kind == 'drone': amb_drone(M, Ttot, ch[0][1], vol)
        elif kind == 'bells': amb_bells(M, Ttot, st, vol)
        elif kind == 'vinyl': vinyl(M, Ttot, vol)
    # ---- mix ----
    if cfg.get('lofi'):   # dusty, slightly crushed breaks
        x = M.buses['break']; step = 2; idx = (np.arange(x.shape[1]) // step) * step; x = x[:, idx]; x = np.round(x * 64) / 64
        M.buses['break'] = np.array([lp(c, 6000) for c in x])
    if cfg['keys'] in ('guitar', 'nylon'): M.buses['keys'] = chorus(M.buses['keys'], mix=.3)
    if 'mel' in M.buses: M.buses['mel_d'] = pingpong(M.buses['mel'], 3 * st, .3)
    levels = {'perc': .9, 'keys': 1., 'pad': .8, 'mel': 1.1, 'mel_d': .35, 'break': .75, 'sub': .7, 'amb': 1., 'fx': .7, 'glock': 1.1, 'harp': .9, 'drums': .8}
    levels.update(cfg.get('levels', {}))
    sends = {'tabla': .12, 'harm': .25, 'dotara': .2, 'flute': .35, 'drone': .3, 'perc': .25, 'keys': .3, 'pad': .5, 'mel': .35, 'glock': .45, 'harp': .4, 'break': .05, 'fx': .25, 'amb': .1}
    sends.update(cfg.get('sends', {}))
    # balance: keep the keys/melody within a few dB of the breaks in the drops, so they never get buried
    DRUMISH = {'break', 'drums', 'perc', 'sub', 'fx', 'amb', 'tabla', 'bass'}
    acc = 0
    for sec_, nb_ in SECS:
        if sec_ == 'dropA': a0, a1 = int(acc * B * SR), int((acc + nb_) * B * SR)
        acc += nb_
    lv = lambda ks_: 20 * np.log10(np.sqrt((sum(M.buses[k][:, a0:a1] * levels.get(k, 1.) for k in ks_) ** 2).mean()) + 1e-9)
    mk_ = [k for k in M.buses if k not in DRUMISH]; dk_ = [k for k in M.buses if k in ('break', 'sub', 'drums')]
    if mk_ and dk_:
        gap = lv(dk_) - lv(mk_)
        if cfg.get('debug'): print('music gap', round(gap, 1))
        if gap > cfg.get('mus_gap', 6.):
            f_ = 10 ** ((gap - cfg.get('mus_gap', 6.)) / 20)
            for k in mk_: levels[k] = levels.get(k, 1.) * f_
    out = np.zeros((2, M.n)); send = np.zeros((2, M.n))
    for k, x in M.buses.items(): out += x * levels.get(k, 1.); send += x * levels.get(k, 1.) * sends.get(k, 0.)
    ir = reverb_ir(cfg.get('verb', 2.2), cfg.get('decay', .55)); out += np.array([ss.fftconvolve(send[c], ir[c])[:M.n] for c in range(2)])
    out = np.array([hp(c, 28) for c in out])
    # automatic section leveling, so quiet parts never vanish under the loud ones
    # ...and so the music never seems to fade away when the breaks come in: the intro, build, breakdown and outro
    # may not have their keys/melody louder than in the neighbouring drop (they start low instead)
    DRUMISH = {'break', 'drums', 'perc', 'sub', 'fx', 'amb', 'tabla', 'bass'}
    mus = sum(x * levels.get(k, 1.) for k, x in M.buses.items() if k not in DRUMISH)
    g = np.ones(M.n); acc = 0; gs, rm, span = {}, {}, {}
    for sec, nb in SECS:
        a, bnd = int(acc * B * SR), int((acc + nb) * B * SR); span[sec] = (a, bnd)
        r = 20 * np.log10(np.sqrt((out[:, a:bnd] ** 2).mean()) + 1e-9)
        rm[sec] = 20 * np.log10(np.sqrt((mus[:, a:bnd] ** 2).mean()) + 1e-9)
        gs[sec] = 10 ** ((TG[sec] - r) / 20); acc += nb
    for s_, ref_ in (('intro', 'dropA'), ('build', 'dropA'), ('half', 'dropB'), ('outro', 'dropB')):
        if s_ in gs and ref_ in gs: gs[s_] = min(gs[s_], gs[ref_] * 10 ** ((rm[ref_] - rm[s_] + cfg.get('cont_tol', 1.5)) / 20))
    if cfg.get("debug"): print({k: (round(rm[k], 1), round(20 * np.log10(gs[k]), 1)) for k in gs}, sorted((k, round(float(np.sqrt((x ** 2).mean())), 4)) for k, x in M.buses.items()))
    for sec, (a, bnd) in span.items(): g[a:bnd] = gs[sec]
    g[int(acc * B * SR):] = g[int(acc * B * SR) - 1]
    from scipy.ndimage import minimum_filter1d; g = minimum_filter1d(g, int(.6 * SR))   # lean to the quieter side at boundaries (no spikes)
    g = ss.filtfilt(*ss.butter(1, 1.2, fs=SR), g)       # smooth ~0.5 s transitions between sections
    out = out * g
    if te is not None:   # tape stop: the whole band slows down to a halt
        a = int(te * SR); D = int(cfg.get('stop_len', 1.8) * SR); rate = np.linspace(1, 0, D) ** 1.3
        pos = a + np.cumsum(rate); seg = np.array([np.interp(pos, np.arange(out.shape[1]), c) for c in out]) * np.linspace(1, 0, D) ** .4
        out = np.concatenate([out[:, :a], seg, np.zeros((2, int(.6 * SR)))], axis=1)
    if cfg.get('lofi'):   # tape wobble + warm top end
        t = np.arange(out.shape[1]); d = .0012 * SR * np.sin(2 * np.pi * .55 * t / SR) + .0004 * SR * np.sin(2 * np.pi * 3.1 * t / SR)
        out = np.array([np.interp(t - d - 60, t, c) for c in out]); out = np.array([lp(c, 7000) for c in out])
    nz = np.nonzero(np.abs(out).max(0) > 1e-4)[0]; out = out[:, :nz[-1] + int(.3 * SR)]
    f = int(1.5 * SR)
    if te is None: out[:, -f:] *= np.linspace(1, 0, f) ** 2
    body = min(int(len(plan) * B * SR), int(te * SR) if te else 10 ** 12)          # set loudness from the song itself, not the final hit
    out = out / np.abs(out[:, :body]).max() * 1.15; out = np.tanh(out) / np.tanh(1.15) * .89
    a_ = np.abs(out); out = np.where(a_ > .93, np.sign(out) * (.93 + .05 * np.tanh((a_ - .93) / .05)), out)   # gentle limiter for the ending
    name = cfg['file']
    wavfile.write(f'{name}.wav', SR, (out.T * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{name}.wav', '-b:a', '320k', f'{name}.mp3'], check=True)
    # report
    acc = 0; rep = []
    for sec, nb in SECS:
        seg = out[:, int(acc * B * SR):int((acc + nb) * B * SR)]; rep.append(f"{sec} {20 * np.log10(np.sqrt((seg ** 2).mean())):.1f}"); acc += nb
    a = int((12 + 2) * B * SR); seg = out[:, a:a + int(12 * B * SR)].mean(0); w = int(.1 * SR)
    spread = np.std([20 * np.log10(np.sqrt((seg[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(seg) - w, w)])
    print(name, f"{out.shape[1] / SR:.1f}s |", ' | '.join(rep), f"| drop spread {spread:.2f} dB")
