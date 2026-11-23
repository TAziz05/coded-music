"""A section-based pop/hip-hop song builder (all sounds are code). Songs are described as settings; build(cfg) renders one.
cfg: file, bpm, swing, sections (list of dicts), order (list of section names), levels/sends overrides.
section: bars, chords (one per bar, cycled), mel (8 eighth-notes per bar, -1 hold, 0 rest; cycled), lead, keys (list),
         drums (style), bass (style), plus optional flags: hey, scratch, riser, impact, bell, gong, fill (default True)."""
import subprocess
import numpy as np, scipy.signal as ss
from scipy.io import wavfile
from engine import *
from engine import reverb_ir
from instruments2 import guitar, chorus, voice, ks, envN, fbass, sax
from songs import piano, ride
from songs3 import glock, flute, timpani
from songs5 import violins, horn, oboe, cymbal
from songs9 import organ, chick, boom_kick, boom_snare, scratch
from songs4 import dist_gtr, power
from breakcore_engine import chord, b808, subbass, reese, taiko, gong, koto, shaku, crunch_lead
from songs10 import hey, heavy808

# ---------------- extra instruments ----------------
def reed(M, t, n, dur, vol, pan=0.):            # piercing double reed (taepyeongso-like)
    N = int((dur + .1) * SR); tt = tarr(N); v = np.clip((tt - .1) / .15, 0, 1) * .35 * np.sin(2 * np.pi * 6.5 * tt)
    f = mtof(n + v - .8 * np.exp(-tt / .03)); x = saw(f, N) * .6 + sqr(f, N, .3) * .4
    y = 1.3 * bp(x, 1100, 2400) + .5 * bp(x, 2800, 4200) + .2 * lp(x, 800)
    M.add('lead', t, np.tanh(y * 1.5) * envN(N, dur, .02, .2, .9, .06) * vol * .25, pan=pan)
def vocoder(M, t, n, dur, vol):                  # robotic 'vocoder' hook: saw chord through vowel formants
    N = int((dur + .1) * SR); x = saw(mtof(n), N) + .6 * saw(mtof(n + 12), N) + .4 * saw(mtof(n - 12), N)
    y = 1.2 * bp(x, 650, 1000) + 1.0 * bp(x, 1100, 1500) + .4 * bp(x, 2500, 3200) + .15 * hp(x, 5000)
    M.add('lead', t, y * envN(N, dur, .01, .2, .9, .05) * vol * .14)
def acoustic(M, t, notes, dur, vol, down=True, pan=.2):
    seq = notes if down else notes[::-1]
    for j, n in enumerate(seq): guitar(M, 'keys', t + j * .01, n, dur, vol * (1 - .05 * j), pan=pan, bright=.5, decay=.996)
def clank(M, t, vol=1.):                         # industrial metal hit
    N = int(.4 * SR); tt = tarr(N); x = np.zeros(N)
    for f, d in ((1230, .08), (2710, .05), (3990, .04), (5300, .03)): x += np.sin(2 * np.pi * f * tt) * np.exp(-tt / d)
    x += bp(noise(N), 3000, 9000) * np.exp(-tt / .01)
    M.add('perc', t, x * vol * .25, pan=.3)
def kkwaeng(M, t, vol=1.):                       # small Korean gong: bright, clanging
    N = int(.5 * SR); tt = tarr(N); x = np.zeros(N)
    for f, a in ((900, 1.), (1350, .7), (2080, .5), (3100, .3)): x += a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / .12)
    M.add('perc', t, x * vol * .18, pan=-.3)
def janggu(M, t, high=True, vol=1.):             # hourglass drum: deep 'kung' or sharp 'tta'
    if high:
        N = int(.15 * SR); tt = tarr(N); M.add('perc', t, (bp(noise(N), 1500, 6000) * .6 + np.sin(2 * np.pi * 600 * tt)) * np.exp(-tt / .025) * vol * .4, pan=.25)
    else: taiko(M, t, vol * .7, n=41)
def temple_bell(M, t, vol=1.):
    N = int(8 * SR); tt = tarr(N); x = np.zeros(N)
    for r, a, d in ((1, 1., 6.), (2.0, .5, 4.), (2.76, .35, 3.), (5.4, .2, 1.5), (8.9, .1, .8)): x += a * np.sin(2 * np.pi * 64 * r * tt) * np.exp(-tt / d) * (1 + .05 * np.sin(2 * np.pi * .9 * tt))
    M.add('perc', t, x * np.clip(tt / .01, 0, 1) * vol * .35)

def fm(M, bus, t, n, dur, vol, ratio=2., index=3., dec=.4, pan=0.):   # 2-operator FM, like the Sega Genesis chip
    N = int((dur + .1) * SR); tt = tarr(N); f = mtof(n); I = index * (.3 + .7 * np.exp(-tt / dec))
    x = np.sin(2 * np.pi * f * tt + I * np.sin(2 * np.pi * f * ratio * tt))
    M.add(bus, t, x * envN(N, dur, .003, .3, .8, .05) * vol * .3, pan=pan)
def gbpulse(M, bus, t, n, dur, vol, duty=.25, pan=0.):                # Game Boy pulse channel
    N = int((dur + .02) * SR); x = np.where((np.arange(N) * mtof(n) / SR) % 1 < duty, 1., -1.)
    M.add(bus, t, x * envN(N, dur, .001, .2, .8, .02) * vol * .12, pan=pan)
def gbwave(M, bus, t, n, dur, vol):                                    # Game Boy wave channel (4-bit triangle-ish)
    N = int((dur + .02) * SR); ph = (np.arange(N) * mtof(n) / SR) % 1; x = np.round((4 * np.abs(ph - .5) - 1) * 7) / 7
    M.add(bus, t, x * envN(N, dur, .001, .1, 1., .01) * vol * .3)
def nylon(M, t, n, dur, vol, pan=0.):
    y = ks(mtof(n), dur + .2, .35, .997); M.add('lead', t, lp(y, 4500) * vol * .55, pan=pan)
def glitch(M, t0, st, tones, vol):                                     # stuttering chopped synth chord
    for k in (0, 1, 2, 6, 7, 10, 12, 13, 14, 15):
        for c in tones: supersaw(M, 'keys', t0 + k * st, c + 24 * (k in (13, 15)), st * .45, .035 * vol, cut=5000, a=.002, r=.01, voices=3)

LEADS = {
 'brass': lambda M, t, n, d, v: brass(M, 'lead', t, n, d * .92, .45 * v),
 'brass2': lambda M, t, n, d, v: (brass(M, 'lead', t, n, d * .92, .42 * v), brass(M, 'lead', t, n - 12, d * .92, .28 * v, pan=.2)),
 'synth': lambda M, t, n, d, v: supersaw(M, 'lead', t, n, d * .93, .2 * v, cut=3400, a=.01, r=.15, voices=5),
 'square': lambda M, t, n, d, v: leadsq(M, 'lead', t, n, d * .92, .5 * v),
 'voice': lambda M, t, n, d, v: voice(M, 'lead', t, n, d * .94, .8 * v),
 'whistle': lambda M, t, n, d, v: flute(M, 'lead', t, n + 12, d * .9, 1.1 * v),
 'flute': lambda M, t, n, d, v: flute(M, 'lead', t, n, d * .93, 1.1 * v),
 'crunch': lambda M, t, n, d, v: crunch_lead(M, t, n, d * .95, 1.2 * v),
 'piano': lambda M, t, n, d, v: piano(M, 'lead', t, n, d, .6 * v, pan=.15),
 'reed': lambda M, t, n, d, v: reed(M, t, n, d * .95, v),
 'vocoder': lambda M, t, n, d, v: vocoder(M, t, n, d * .95, v),
 'guitar': lambda M, t, n, d, v: guitar(M, 'lead', t, n, d * 1.2, .55 * v, bright=.7, decay=.999),
 'gayageum': lambda M, t, n, d, v: koto(M, t, n, d, 1.2 * v, pan=.1),
 'danso': lambda M, t, n, d, v: shaku(M, t, n, d * .95, 1.1 * v),
 'sax': lambda M, t, n, d, v: sax(M, 'lead', t, n, d * .95, .7 * v),
 'fm': lambda M, t, n, d, v: fm(M, 'lead', t, n, d * .92, 1.1 * v, ratio=1., index=2.5, dec=.3),
 'fmbell': lambda M, t, n, d, v: fm(M, 'lead', t, n, d * .92, .9 * v, ratio=3.5, index=2., dec=.2),
 'gb': lambda M, t, n, d, v: gbpulse(M, 'lead', t, n, d * .92, 1. * v, .25),
 'gb12': lambda M, t, n, d, v: gbpulse(M, 'lead', t, n, d * .92, .9 * v, .125),
 'nylon': lambda M, t, n, d, v: nylon(M, t, n, d, v),
 'trumpet': lambda M, t, n, d, v: brass(M, 'lead', t, n, d * .9, .42 * v, bright=1.2),
 'strings': lambda M, t, n, d, v: violins(M, t, n, d * .97, .6 * v, att=.06, bus='lead'),
 'metal': lambda M, t, n, d, v: crunch_lead_hot(M, t, n, d * .95, v),
 'choirbrass': lambda M, t, n, d, v: (brass(M, 'lead', t, n, d * .92, .4 * v), voice(M, 'lead', t, n - 12, d * .94, .5 * v)),
}

# ---------------- per-bar parts ----------------
def crunch_lead_hot(M, t, n, dur, vol):
    y = ks(mtof(n), dur + .05, .65, .9994); y = np.tanh(y * 7) * .5; y = lp(hp(y, 100), 4500) + .3 * bp(y, 1500, 3000)
    M.add('lead', t, y * vol * .4)

EXTRA_KEYS, EXTRA_DRUMS, EXTRA_BASS = {}, {}, {}   # other song files can register their own styles here

def keys_bar(M, style, t0, st, S, tones, root, v):
    if style in EXTRA_KEYS: return EXTRA_KEYS[style](M, t0, st, S, tones, root, v)
    T = tones; arp = T + [T[0] + 12, T[1] + 12]
    if style == 'piano':
        piano(M, 'keys', t0, root + 12, 8 * st, .5 * v, pan=-.2)
        for s in (0, 6, 10):
            for c in T: piano(M, 'keys', t0 + S(s), c, st * 2.5, .24 * v)
    elif style == 'pianoriff':
        for k in range(8): piano(M, 'keys', t0 + S(2 * k), [T[0], T[1], T[2], T[1]][k % 4], 2 * st * 1.5, .38 * v)
    elif style == 'pad':
        for nn in T: supersaw(M, 'pad', t0, nn + 12, 16 * st, .055 * v, cut=1600, a=.3, r=.5, voices=3)
    elif style == 'pluck':
        for k in range(16): pluck(M, 'keys', t0 + S(k), arp[[0, 2, 4, 1, 3, 2, 4, 1][k % 8]] + 12, st * .9, .1 * v, pan=(-.4, .4)[k % 2], dec=.08)
    elif style == 'guitar':
        for k in range(8): guitar(M, 'keys', t0 + S(2 * k), arp[[0, 1, 2, 3, 2, 1, 2, 4][k]], 2 * st * 2.5, .35 * v, pan=-.35, bright=.55)
    elif style == 'acoustic':
        for s, dn in ((0, True), (4, True), (6, False), (10, False), (12, True), (14, False)): acoustic(M, t0 + S(s), [root + 12] + T, st * 3, .22 * v, down=dn)
    elif style == 'stabs':
        for s in (0, 3, 6):
            for c in T: brass(M, 'keys', t0 + S(s), c + 12, st * 1.3, .17 * v)
    elif style == 'ep':
        for s in (0, 3, 6, 10, 12):
            for j, c in enumerate(T): epiano(M, 'keys', t0 + S(s) + j * .006, c + 12 if c < 60 else c, st * (2.4 if s in (0, 6) else 1.3), .075 * v, pan=(j - 1.5) * .2)
    elif style == 'strings':
        for j, c in enumerate(T): violins(M, t0, c + 12, 16 * st * .98, .45 * v, att=.2, pan=(j - 1) * .3)
    elif style == 'organ':
        for c in T: organ(M, t0, c + 12, 16 * st * .97, .45 * v, pan=.25)
    elif style == 'chick':
        for k in range(16):
            if k % 4 in (1, 2, 3): chick(M, t0 + S(k), T + [T[0] + 12], (.16 if k % 2 else .1) * v)
    elif style == 'power':
        r2 = root if root < 44 else root - 12
        for s, L in ((0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)):
            dist_gtr(M, 'gtrL', t0 + S(s), power(r2 + 12), L * st * .92, .28 * v, pan=-.65, gain=4., warm=True)
            dist_gtr(M, 'gtrR', t0 + S(s) + .007, power(r2 + 12), L * st * .92, .28 * v, pan=.65, gain=4., warm=True)
    elif style == 'darkgtr':
        for k in range(8): guitar(M, 'keys', t0 + S(2 * k), arp[[0, 2, 1, 3, 2, 4, 3, 1][k]], 2 * st * 3, .3 * v, pan=-.3, bright=.4, decay=.997)
    elif style == 'futurebass':   # chopped supersaw chords that swell in
        for s, L in ((0, 3), (3, 3), (6, 4), (10, 2), (12, 4)):
            for c in T: supersaw(M, 'keys', t0 + S(s), c + 12, L * st * .9, .06 * v, cut=3500, a=L * st * .5, r=.05, voices=5, detune=.2)
    elif style == 'dembowpluck':
        for s in (0, 3, 6, 8, 11, 14): pluck(M, 'keys', t0 + S(s), arp[s % 5] + 12, st * 1.4, .12 * v, dec=.12, cut=3000)
    elif style == 'gayageum':
        for k in range(8): koto(M, t0 + S(2 * k), arp[[0, 2, 4, 3, 1, 3, 5, 4][k] % len(arp)] + 12, 2 * st * 3, .8 * v, pan=(-.35 if k % 2 else .35))
    elif style == 'chug':   # palm-muted low chugs with accents (metal / nu-metal)
        r2 = root if root < 44 else root - 12; r2 = r2 - 12 if r2 > 40 else r2
        for k in range(16):
            acc = k in (0, 3, 6, 10, 14)
            dist_gtr(M, 'gtrL', t0 + S(k), power(r2 + 12) if acc else [r2 + 12], st * (1.6 if acc else .9), (.3 if acc else .2) * v, mute=not acc, pan=-.7, gain=9.)
            dist_gtr(M, 'gtrR', t0 + S(k) + .006, power(r2 + 12) if acc else [r2 + 12], st * (1.6 if acc else .9), (.3 if acc else .2) * v, mute=not acc, pan=.7, gain=9.)
    elif style == 'tremolo':   # fast tremolo-picked metal guitar on the chord tones
        for k in range(16): dist_gtr(M, 'gtrL', t0 + S(k), [T[(k // 4) % len(T)] + 12], st * .9, .18 * v, pan=-.5, gain=8.)
    elif style == 'glitch': glitch(M, t0, st, T, v)
    elif style == 'fm':
        for s in (0, 3, 6, 10, 12):
            for c in T: fm(M, 'keys', t0 + S(s), c + 12, st * 1.4, .35 * v, ratio=2., index=1.5, dec=.15)
    elif style == 'gbarp':
        for k in range(16): gbpulse(M, 'keys', t0 + S(k), arp[k % 4] + 12, st * .8, .7 * v, .5, pan=-.3)
    elif style == 'nylon':
        for s, dn in ((0, True), (3, True), (6, False), (8, True), (11, True), (14, False)):
            for j, c in enumerate(([root + 12] + T) if dn else T[::-1]): nylon(M, t0 + S(s) + j * .012, c, st * 2.5, .3 * v)
    elif style == 'jazzpiano':
        for s in (0, 7, 10):
            for c in T: piano(M, 'keys', t0 + S(s), c, st * 2, .22 * v)
    elif style == 'horns':
        for j, c in enumerate(T): horn(M, t0, c, 16 * st * .97, .5 * v, pan=(j - 1) * .3)

def drums_bar(M, style, t0, st, S, i, n, fill=True):
    if style in EXTRA_DRUMS: return EXTRA_DRUMS[style](M, t0, st, S, i, n, fill)
    last = (i == n - 1) and fill
    if style == 'boombap':
        for s in (0, 7, 10): boom_kick(M, t0 + S(s), 1. if s == 0 else .8)
        for s in (4, 12): boom_snare(M, t0 + S(s))
        for k in range(0, 16, 2): hat(M, t0 + S(k), .32 if k % 4 == 2 else .2)
    elif style == 'rock':
        for s in (0, 6, 8, 10): kick(M, t0 + S(s), .9)
        for s in (4, 12): snare(M, t0 + S(s), .85)
        for k in range(8): ride(M, t0 + S(2 * k), .5)
    elif style == 'fourfloor':
        for k in range(4): kick(M, t0 + S(4 * k), .9)
        clap(M, t0 + S(4), .7); clap(M, t0 + S(12), .7)
        for k in range(16): hat(M, t0 + S(k), .4 if k % 4 == 2 else .18, open_=(k % 4 == 2))
    elif style == 'halfpop':
        kick(M, t0, .8); kick(M, t0 + S(10), .6); snare(M, t0 + S(8), .7)
        for k in range(0, 16, 2): hat(M, t0 + S(k), .22)
    elif style == 'trap':
        for s in ((0, 7, 10) if i % 2 == 0 else (0, 3, 11)): kick(M, t0 + S(s), .85, punch=1.2)
        snare(M, t0 + S(8), .85); clap(M, t0 + S(8), .6)
        for k in range(0, 16, 2): hat(M, t0 + S(k), .3 if k % 4 == 0 else .2)
        if i % 2 == 1:
            for j in range(8): hat(M, t0 + 14 * st + j * st / 4, .13 + .02 * j)
    elif style == 'dembow':
        for s in (0, 8): kick(M, t0 + S(s), .9)
        for s in (3, 6, 11, 14): snare(M, t0 + S(s), .55); rim_(M, t0 + S(s))
        for k in range(0, 16, 2): hat(M, t0 + S(k), .22)
    elif style == 'gqom':
        for s in (0, 3, 6, 10): kick(M, t0 + S(s), .85 if s == 0 else .65)
        for s in (2, 7, 9, 13): tom(M, t0 + S(s), [45, 48, 43, 52][s % 4], .55)
        for s in (4, 12): clap(M, t0 + S(s), .6)
        for k in range(16): shaker(M, t0 + S(k), .5 if k % 2 else .3)
    elif style == 'funk':
        for s in (0, 3, 8, 10): kick(M, t0 + S(s), .8)
        for s in (4, 12): snare(M, t0 + S(s), .65); clap(M, t0 + S(s), .55)
        for k in range(16): hat(M, t0 + S(k), .3 if k % 2 == 0 else .16, open_=(k == 14))
    elif style == 'march':
        for s in (0, 8): kick(M, t0 + S(s), 1., punch=.9); timpani(M, t0 + S(s), 38, .45)
        for s in (4, 12): snare(M, t0 + S(s), .9); clap(M, t0 + S(s), .4)
        for k in range(16): snare(M, t0 + S(k), .12 + (.1 if k % 4 == 0 else 0))
        if i % 4 == 0: cymbal(M, t0, .5)
    elif style == 'lofi':
        kick(M, t0, .6, punch=.7); kick(M, t0 + S(10), .45, punch=.7)
        for s in (4, 12): rim_(M, t0 + S(s), 1.3)
        for k in range(16): shaker(M, t0 + S(k), .45 if k % 2 else .25)
    elif style == 'metal':
        for k in range(16): kick(M, t0 + S(k), .55 if k % 2 else .7, punch=1.3)
        for s in (4, 12): snare(M, t0 + S(s), .95)
        for k in range(0, 16, 2): ride(M, t0 + S(k), .5)
        if i % 4 == 0: crash(M, t0, .55)
    elif style == 'punk':
        for s in (0, 6, 8, 10, 14): kick(M, t0 + S(s), .85)
        for s in (4, 12): snare(M, t0 + S(s), .85)
        for k in range(8): hat(M, t0 + S(2 * k), .4, open_=True)
    elif style == 'jazz':
        for k in range(4):
            ride(M, t0 + S(4 * k), .55); ride(M, t0 + S(4 * k) + 2.67 * st, .35)
        for s in (4, 12): hat(M, t0 + S(s), .3)
        kick(M, t0, .35, punch=.6); snare(M, t0 + S(14), .15)
    elif style == 'house':
        for k in range(4): kick(M, t0 + S(4 * k), .9)
        for s in (4, 12): clap(M, t0 + S(s), .6)
        for k in range(4): hat(M, t0 + S(4 * k + 2), .45, open_=True)
        for k in range(16): shaker(M, t0 + S(k), .4 if k % 2 else .2)
    elif style == 'breakbeat':
        for s in (0, 10): kick(M, t0 + S(s), .9)
        for s in (4, 12): snare(M, t0 + S(s), .85)
        for s in (7, 9, 15): snare(M, t0 + S(s), .2)
        for k in range(16): hat(M, t0 + S(k), .25 if k % 2 == 0 else .14)
    elif style == 'gb':
        for s in (0, 8, 10): gbpulse(M, 'drums', t0 + S(s), 30, .05, 3., .5)
        for s in (4, 12): M.add('drums', t0 + S(s), noise(int(.08 * SR)) * np.exp(-tarr(int(.08 * SR)) / .03) * .25)
        for k in range(0, 16, 2): M.add('drums', t0 + S(k), hp(noise(int(.03 * SR)), 6000) * .12)
    if last and style not in ('lofi', 'none', 'halfpop', 'gb', 'jazz'):
        for s, nn in zip(range(12, 16), (52, 48, 45, 41)): tom(M, t0 + S(s), nn, .5)
def rim_(M, t, v=1.):
    N = int(.06 * SR); tt = tarr(N)
    M.add('drums', t, (bp(noise(N), 1500, 5000) * .5 + np.sin(2 * np.pi * 820 * tt)) * np.exp(-tt / .012) * v * .3, pan=-.2)

def bass_bar(M, style, t0, st, S, root):
    if style in EXTRA_BASS: return EXTRA_BASS[style](M, t0, st, S, root)
    r = root if root < 44 else root - 12
    if style == '808':
        for s, L in ((0, 6), (7, 3), (10, 6)): b808(M, t0 + S(s), r, L * st * .95, .55)
    elif style == 'heavy808':
        for s, L in ((0, 7), (10, 6)): heavy808(M, t0 + S(s), r, L * st * .95, .6)
    elif style == 'sub':
        subbass(M, t0, r, 16 * st * .95, .45, 1.6)
    elif style == 'synth8':
        for k in range(8): bass(M, 'bass', t0 + S(2 * k), r, 2 * st * .8, .5, cut=1000)
    elif style == 'octave':
        for k in range(8): bass(M, 'bass', t0 + S(2 * k), r + (12 if k % 2 else 0), 2 * st * .75, .5, cut=1200)
    elif style == 'finger':
        for s, o, L in ((0, 0, 3), (3, 0, 1), (6, 7, 2), (8, 0, 3), (11, 12, 2), (14, 7, 2)): fbass(M, t0 + S(s), r + o, L * st * .9, .6)
    elif style == 'funky':
        for s, o, L in ((0, 0, 2), (2, 12, 1), (3, 0, 2), (6, 10, 2), (8, 0, 2), (10, 12, 1), (11, 7, 2), (14, 0, 2)): fbass(M, t0 + S(s), r + o, L * st * .8, .65)
    elif style == 'reese':
        for s, L in ((0, 6), (6, 2), (8, 8)): reese(M, t0 + S(s), r + 12, L * st * .95, .4)
    elif style == 'long':
        fbass(M, t0, r, 16 * st * .9, .55)
    elif style == 'fm':
        for s, o, L in ((0, 0, 2), (3, 12, 1), (4, 0, 2), (7, 0, 1), (8, 12, 2), (10, 0, 2), (12, 7, 2), (14, 10, 2)): fm(M, 'bass', t0 + S(s), r + o, L * st * .85, .9, ratio=1., index=4., dec=.08)
    elif style == 'gbwave':
        for k in range(8): gbwave(M, 'bass', t0 + S(2 * k), r + (12 if k % 2 else 0), 2 * st * .8, .9)
    elif style == 'walking':
        for k in range(4): fbass(M, t0 + S(4 * k), r + [0, 4, 7, 9][k], 4 * st * .9, .6)
    elif style == 'metalbass':
        for k in range(16): fbass(M, t0 + S(k), (r - 12 if r > 40 else r), st * .9, .5)

TARGET = {'intro': -18., 'verse': -15., 'pre': -14.5, 'chorus': -12.5, 'drop': -12.5, 'bridge': -15.5, 'break': -16., 'outro': -17.5}

def build(cfg):
    st = 60 / cfg['bpm'] / 4; B = 16 * st; sw = cfg.get('swing', 0) * st
    S = lambda k: k * st + (sw if k % 2 else 0)
    secs = cfg['sections']; order = cfg['order']
    plan = [(name, i, secs[name]['bars']) for name in order for i in range(secs[name]['bars'])]
    M = Mix(len(plan) * B + 6); marks = []
    for b, (name, i, n) in enumerate(plan):
        sec = secs[name]; t0 = b * B
        if i == 0: marks.append((name, t0, n))
        tones, root = chord(sec['chords'][i % len(sec['chords'])])
        for ks_ in sec.get('keys', []): keys_bar(M, ks_, t0, st, S, tones, root, sec.get('kv', 1.))
        if sec.get('drums'): drums_bar(M, sec['drums'], t0, st, S, i, n, sec.get('fill', True))
        if sec.get('bass'): bass_bar(M, sec['bass'], t0, st, S, root)
        if sec.get('mel') and sec.get('lead'):
            rows = sec['mel']; row = rows[i % len(rows)]; flat = row
            nxt = rows[(i + 1) % len(rows)]
            for k, x in enumerate(flat):
                if x > 0:
                    L = 1
                    while k + L < 8 and flat[k + L] == -1: L += 1
                    if k + L == 8:   # hold across the bar line
                        j = 0
                        while j < 8 and nxt[j] == -1: L += 1; j += 1
                    for ld in sec['lead'].split('+'): LEADS[ld](M, t0 + S(2 * k), x + sec.get('up', 0), L * 2 * st, sec.get('lv', 1.))
        if i == 0 and sec.get('impact'): crash(M, t0, .8); impact(M, t0, .6)
        if i == 0 and sec.get('crash', True) and sec.get('drums') and name not in ('intro',): crash(M, t0, .45)
        if sec.get('riser') and i == n - 1: riser(M, t0, B, .5)
        if sec.get('hey') and i % 2 == 1: hey(M, t0 + S(sec.get('heystep', 8)), .9)
        if sec.get('scratch') and i % 4 == 3: scratch(M, t0 + S(12), .8)
        if sec.get('bell') and i == 0: temple_bell(M, t0, 1.)
        if sec.get('gong') and i == 0: gong(M, t0, .8)
        if sec.get('kkwaeng'):
            for s in (0, 3, 6, 10): kkwaeng(M, t0 + S(s), .8)
        if sec.get('janggu'):
            for s, h in ((0, False), (3, True), (6, True), (8, False), (11, True), (14, True)): janggu(M, t0 + S(s), h, .8)
        if sec.get('clank'):
            for s in (6, 14): clank(M, t0 + S(s), .9)
        if sec.get('extra'): sec['extra'](M, t0, st, S, i, n, tones, root)
    for k in ('keys', 'gtrL', 'gtrR'):
        if k in M.buses and cfg.get('chorus_keys'): M.buses[k] = chorus(M.buses[k], mix=.3)
    if 'lead' in M.buses: M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .25)
    levels = {'keys': 1., 'pad': .8, 'lead': 1.1, 'lead_d': .3, 'bass': .9, 'sub': .9, 'drums': .9, 'perc': .9, 'fx': .8, 'str': .8, 'gtrL': 1.8, 'gtrR': 1.8, 'organ': .7}
    levels.update(cfg.get('levels', {}))
    sends = {'keys': .25, 'pad': .45, 'lead': .3, 'drums': .05, 'perc': .25, 'fx': .25, 'str': .4, 'organ': .25, 'gtrL': .08, 'gtrR': .08}
    sends.update(cfg.get('sends', {}))
    # balance: in the chorus, keep the keys/lead within a few dB of the drums and bass so the music never gets buried
    DR = ('drums', 'perc', 'bass', 'sub')
    ref = next((m for m in marks if secs[m[0]].get('kind', m[0].rstrip('0123456789')) in ('chorus', 'drop')), marks[min(1, len(marks) - 1)])
    a0, a1 = int(ref[1] * SR), int((ref[1] + ref[2] * B) * SR)
    lv = lambda ks_: 20 * np.log10(np.sqrt((sum(M.buses[k][:, a0:a1] * levels.get(k, 1.) for k in ks_) ** 2).mean()) + 1e-9)
    mk_ = [k for k in M.buses if k not in DR + ('fx',)]; dk_ = [k for k in M.buses if k in DR]
    if mk_ and dk_ and cfg.get('mus_gap', 5.) is not None:
        gap = lv(dk_) - lv(mk_)
        if gap > cfg.get('mus_gap', 5.):
            f_ = 10 ** ((gap - cfg.get('mus_gap', 5.)) / 20)
            for k in mk_: levels[k] = levels.get(k, 1.) * f_
    out = np.zeros((2, M.n)); send = np.zeros((2, M.n))
    for k, x in M.buses.items(): out += x * levels.get(k, 1.); send += x * levels.get(k, 1.) * sends.get(k, 0.)
    ir = reverb_ir(cfg.get('verb', 2.2), cfg.get('decay', .55)); out += np.array([ss.fftconvolve(send[c], ir[c])[:M.n] for c in range(2)])
    out = np.array([hp(c, 28) for c in out])
    g = np.ones(M.n); TG = dict(TARGET, **cfg.get('targets', {}))
    mus = sum(x * levels.get(k, 1.) for k, x in M.buses.items() if k not in ('drums', 'perc', 'bass', 'sub', 'fx'))
    gl, rl = [], []
    for name, t0, nb in marks:
        a, bnd = int(t0 * SR), int((t0 + nb * B) * SR); seg = out[:, a:bnd]
        r = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9); kind = secs[name].get('kind', name.rstrip('0123456789'))
        gl.append(10 ** ((TG.get(kind, -15.) - r) / 20)); rl.append(20 * np.log10(np.sqrt((mus[:, a:bnd] ** 2).mean()) + 1e-9))
    # keep the music continuous: the intro and outro (no drums) may not have their keys/lead louder than the section next to them
    tol = cfg.get('cont_tol', 1.5)
    if len(marks) > 1:
        gl[0] = min(gl[0], gl[1] * 10 ** ((rl[1] - rl[0] + tol) / 20)); gl[-1] = min(gl[-1], gl[-2] * 10 ** ((rl[-2] - rl[-1] + tol) / 20))
    for (name, t0, nb), gg in zip(marks, gl): g[int(t0 * SR):int((t0 + nb * B) * SR)] = gg
    body = int(len(plan) * B * SR); g[body:] = g[body - 1]
    from scipy.ndimage import minimum_filter1d; g = minimum_filter1d(g, int(.6 * SR))   # lean to the quieter side at boundaries (no spikes)
    g = ss.filtfilt(*ss.butter(1, 1.2, fs=SR), g); out = out * g
    if cfg.get('ride'):   # gentle gain riding inside sections, for an even, steady level (background music)
        w = int(2 * B * SR); e = np.sqrt(ss.filtfilt(*ss.butter(1, .5, fs=SR), (out ** 2).mean(0)) + 1e-12)
        ref = np.sqrt(ss.filtfilt(*ss.butter(1, 1 / (8 * B), fs=SR), e ** 2)); gr = np.clip((ref / e) ** cfg['ride'], 10 ** (-3 / 20), 10 ** (3 / 20)); gr[body:] = gr[body - 1]   # smooth out wobble around the local (8-bar) level only
        out = out * ss.filtfilt(*ss.butter(1, .4, fs=SR), gr)
    if cfg.get('fadeout'):   # ending: fade out over the last N seconds of the song body
        f_ = int(cfg['fadeout'] * SR); out[:, body - f_:body] *= np.linspace(1, 0, f_) ** 1.5; out[:, body:] = 0
    if cfg.get('tapestop'):   # ending: the whole band slows to a halt at the start of the last section
        a_ = int(marks[-1][1] * SR); D = int(cfg.get('stop_len', 1.6) * SR); rate = np.linspace(1, 0, D) ** 1.3
        pos = a_ + np.cumsum(rate); seg = np.array([np.interp(pos, np.arange(out.shape[1]), c) for c in out]) * np.linspace(1, 0, D) ** .4
        out = np.concatenate([out[:, :a_], seg, np.zeros((2, int(.5 * SR)))], axis=1); body = min(body, a_)
    nz = np.nonzero(np.abs(out).max(0) > 1e-4)[0]; out = out[:, :nz[-1] + int(.3 * SR)]
    f = int(1.2 * SR); out[:, -f:] *= np.linspace(1, 0, f) ** 2
    out = out / np.abs(out[:, :body]).max() * 1.15; out = np.tanh(out) / np.tanh(1.15) * .89
    a_ = np.abs(out); out = np.where(a_ > .93, np.sign(out) * (.93 + .05 * np.tanh((a_ - .93) / .05)), out)
    if cfg.get('crush'):   # old-console sample rate + bit depth
        rate, bits = cfg['crush']; step = SR / rate; idx = (np.floor(np.arange(out.shape[1]) / step) * step).astype(int)
        out = out[:, idx]; q = 2 ** (bits - 1); out = np.round(out * q) / q
        out = np.array([lp(c, min(rate * .48, 15000), 1) for c in out]); out = out / np.abs(out).max() * .89
    name = cfg['file']; wavfile.write(f'{name}.wav', SR, (out.T * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{name}.wav', '-b:a', '320k', f'{name}.mp3'], check=True)
    rep = []
    for nm, t0, nb in marks:
        seg = out[:, int(t0 * SR):int((t0 + nb * B) * SR)]; rep.append(f"{nm} {20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9):.1f}")
    print(name, f"{out.shape[1] / SR:.1f}s |", ' | '.join(rep))
