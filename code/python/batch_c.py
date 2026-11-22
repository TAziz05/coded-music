"""World flutes journey, Marshmello-style and Charli xcx (Brat-era) style songs, plus steady breakcore versions.
python batch_c.py all  (or: flutes mello mello_bc charli charli_bc)"""
import sys
import numpy as np, scipy.signal as ss
import popkit
from popkit import build as pbuild, keys_bar, LEADS
from breakcore_engine import build as bbuild, chord, koto, shaku, taiko, gong, b808, subbass
from seasons import AMEN, FUNK
from engine import *
from instruments2 import ks, envN, voice, guitar
from songs import render, piano
from southasia import bansuri, tabla_bar, harmonium, tanpura, dotara

# ---------------- flutes of the world (all code) ----------------
def fl(M, t, n, dur, vol, kind, prev=None, pan=0.):
    N = int((dur + .15) * SR); tt = tarr(N)
    if kind == 'whistle':    # Irish tin whistle: bright, with a quick 'cut' grace note above
        p = 2. * ((tt < .035) * 1.); vib = 0; harm = (.35, .12); breath = .05; chiff = .15
    elif kind == 'pan':      # Andean pan flute: very breathy, strong chiff
        p = 0; vib = np.clip((tt - .3) / .3, 0, 1) * .15 * np.sin(2 * np.pi * 5 * tt); harm = (.1, .05); breath = .22; chiff = .5
    elif kind == 'dizi':     # Chinese dizi: bright with the buzzing membrane
        p = ((prev - n) * np.exp(-tt / .05)) if prev else 0; vib = np.clip((tt - .2) / .2, 0, 1) * .25 * np.sin(2 * np.pi * 6 * tt); harm = (.5, .3); breath = .06; chiff = .1
    elif kind == 'native':   # Native American cedar flute: low, warm, breathy, warbling
        p = ((prev - n) * np.exp(-tt / .08)) if prev else -.8 * np.exp(-tt / .06); vib = .2 * np.sin(2 * np.pi * 4 * tt) * np.clip((tt - .2) / .3, 0, 1); harm = (.15, .04); breath = .16; chiff = .2
    elif kind == 'fula':     # West African fula flute: breathy, with the player humming along
        p = 0; vib = np.clip((tt - .15) / .2, 0, 1) * .3 * np.sin(2 * np.pi * 6.5 * tt); harm = (.25, .1); breath = .25; chiff = .3
    f = mtof(n + p + vib); x = sine(f, N) + harm[0] * sine(2 * f, N) + harm[1] * sine(3 * f, N)
    if kind == 'dizi': x += bp(noise(N), 2000, 6000) * (.4 + .6 * (sine(f, N) > .6)) * .18
    if kind == 'fula': x += .35 * sine(f / 2, N) * (1 + .3 * sine(110, N))
    x += bp(noise(N), 1000, 7000) * (breath + chiff * np.exp(-tt / .04))
    M.add('flute', t, x * envN(N, dur, .03, .3, .85, .1) * vol * .3, pan=pan)

def drum(M, t, n, dec, vol, bus='perc', pan=0.):
    N = int((dec * 4 + .05) * SR); tt = tarr(N); f = mtof(n) * (1 + .3 * np.exp(-tt / .02))
    M.add(bus, t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / dec) * vol * .6 + lp(noise(N), 2500) * np.exp(-tt / .008) * vol * .2, pan=pan)
def click(M, t, f, vol, pan=0.):
    N = int(.06 * SR); tt = tarr(N); M.add('perc', t, (np.sin(2 * np.pi * f * tt) + bp(noise(N), f, f * 2.5) * .5) * np.exp(-tt / .012) * vol * .35, pan=pan)
def strum(M, t, notes, dur, vol, bright=.75, gap=.008, pan=.2, down=True):
    for j, c in enumerate(notes if down else notes[::-1]): M.add('keys', t + j * gap, lp(ks(mtof(c), dur, bright, .996), 6500) * vol * (1 - .05 * j), pan=pan)
def rainstick(M, t, dur, vol):
    N = int(dur * SR); d = np.zeros(N); pos = rng.integers(0, N, int(dur * 400)); d[pos] = rng.uniform(.2, 1, len(pos))
    M.add('perc', t, bp(ss.lfilter([1], [1, -.8], d), 3000, 9000) * np.sin(np.pi * tarr(N) / dur) * vol * .3)

def winds_of_the_world():
    bpm = 104; st = 60 / bpm / 4; B = 16 * st
    regions = [
     ('andes', ['Dm', 'C', 'F', 'A'], 'pan', [[74,-1,77,76,74,-1,72,-1],[72,-1,74,72,69,-1,-1,-1],[69,-1,72,74,-1,77,-1,76],[73,-1,-1,-1,0,0,0,0]]),
     ('ireland', ['D', 'G', 'D', 'A'], 'whistle', [[78,76,74,76,78,-1,81,-1],[83,81,79,-1,78,76,74,-1],[78,76,74,76,78,-1,81,79],[76,-1,74,-1,0,0,0,0]]),
     ('japan', ['Gm', 'Eb', 'Dm', 'Bb'], 'shaku', [[74,-1,-1,75,-1,74,70,-1],[67,-1,-1,-1,69,-1,-1,-1],[70,-1,69,67,-1,63,-1,62],[62,-1,-1,-1,0,0,0,0]]),
     ('india', ['D', 'C', 'G', 'D'], 'bansuri', [[74,-1,76,78,-1,79,78,76],[74,-1,72,-1,71,-1,69,-1],[71,-1,72,74,-1,76,74,72],[74,-1,-1,-1,0,0,0,0]]),
     ('china', ['D', 'Bm', 'G', 'A'], 'dizi', [[78,-1,81,-1,83,81,78,-1],[76,-1,78,76,74,-1,-1,-1],[74,-1,76,78,-1,81,-1,83],[81,-1,-1,-1,0,0,0,0]]),
     ('native', ['Dm', 'Dm', 'C', 'Dm'], 'native', [[62,-1,-1,65,-1,67,-1,-1],[69,-1,-1,67,65,-1,-1,-1],[67,-1,-1,65,-1,62,-1,60],[62,-1,-1,-1,-1,-1,0,0]]),
     ('africa', ['D', 'C', 'G', 'D'], 'fula', [[74,-1,74,72,-1,74,-1,79],[78,-1,76,74,-1,72,-1,-1],[74,-1,76,74,-1,72,71,-1],[69,-1,-1,-1,0,0,0,0]]),
     ('finale', ['D', 'G', 'D', 'A'], 'all', [[78,76,74,76,78,-1,81,-1],[83,81,79,-1,78,76,74,-1],[78,76,74,76,78,-1,81,79],[76,-1,74,-1,74,-1,-1,-1]])]
    plan = [('intro', 0)] * 2 + [(r[0], i) for r in regions for i in range(8)] + [('end', 0)]
    M = Mix(len(plan) * B + 6); prev = [None]
    tanpura_on = []
    for b, (name, i) in enumerate(plan):
        t0 = b * B
        if name == 'intro':
            rainstick(M, t0, B * 1.5, .8) if b == 0 else None
            fl(M, t0 + (0 if b == 0 else 2 * st), 69 if b == 0 else 74, B * .9, .7, 'native'); continue
        if name == 'end':
            for k in ('pan', 'whistle', 'dizi', 'native'): fl(M, t0 + .02 * len(k), {'pan': 74, 'whistle': 86, 'dizi': 81, 'native': 62}[k], 3., .45, k)
            shaku(M, t0, 74, 3., .6); bansuri(M, t0, 78, 3., .6); gong(M, t0, .6); strum(M, t0, [50, 57, 62, 66, 69], 3., .4); continue
        reg = next(r for r in regions if r[0] == name); chs, kind, mel = reg[1], reg[2], reg[3]
        tones, root = chord(chs[i % 4])
        row = mel[i % 4] if not (i >= 4 and name != 'finale') else [x + (12 if (x > 0 and name in ('native',)) else 0) for x in mel[i % 4]]
        # the melody
        for k, x in enumerate(row):
            if x > 0:
                L = 1
                while k + L < 8 and row[k + L] == -1: L += 1
                tt, d = t0 + k * 2 * st, L * 2 * st * .95
                if kind == 'shaku': shaku(M, tt, x, d, 1.1)
                elif kind == 'bansuri': bansuri(M, tt, x, d, 1., prev=prev[0])
                elif kind == 'all':
                    fl(M, tt, x, d, .6, 'whistle', pan=-.3); fl(M, tt, x - 12, d, .5, 'pan', pan=.3); bansuri(M, tt, x - 12, d, .5, prev=prev[0]); fl(M, tt, x, d, .35, 'dizi', prev=prev[0])
                else: fl(M, tt, x, d, 1., kind, prev=prev[0])
                prev[0] = x
        # each region's own accompaniment and percussion
        if name == 'andes':
            for s in (0, 2, 4, 6, 8, 10, 12, 14): strum(M, t0 + s * st, [c + 12 for c in tones], st * 1.5, .22, bright=.85, gap=.005, down=(s % 4 == 0))
            for s in (0, 6, 8): drum(M, t0 + s * st, 38, .2, .8)
            for s in (4, 12): click(M, t0 + s * st, 900, .7)
        elif name == 'ireland':
            for s, dn in ((0, 1), (3, 0), (6, 1), (8, 1), (11, 0), (14, 1)): strum(M, t0 + s * st, [root + 12] + tones, st * 2.5, .2, bright=.55, down=bool(dn))
            for k in range(16): drum(M, t0 + k * st, 45 if k % 4 == 0 else 52, .08 if k % 4 else .18, .55 if k % 4 == 0 else .25)   # bodhran
        elif name == 'japan':
            for k in range(8): koto(M, t0 + k * 2 * st, (tones + [tones[0] + 12, tones[1] + 12])[[0, 2, 4, 3, 1, 3, 4, 2][k] % 5] + 12, 2 * st * 3, .8)
            if i % 2 == 0: taiko(M, t0, .9); taiko(M, t0 + 8 * st, .6)
            for s in (12, 14): click(M, t0 + s * st, 1400, .5)
        elif name == 'india':
            harmonium(M, t0, tones[:3], B * .97, .8); tabla_bar(M, t0, st, .85, fill=(i % 4 == 3))
            if i == 0: tanpura_on.append(t0)
        elif name == 'china':
            for k in range(16): M.add('keys', t0 + k * st, lp(ks(mtof((tones + [tones[0] + 12])[[0, 1, 2, 3, 2, 1, 2, 3][k % 8]] + 12), st * 2, .8, .995), 7000) * .3, pan=-.3)   # guzheng
            for s in (0, 4, 8, 12): click(M, t0 + s * st, 1200 if s % 8 == 0 else 1700, .7, pan=.3)   # woodblocks
            if i % 4 == 0: gong(M, t0, .5)
        elif name == 'native':
            M.add('keys', t0, lp(saw(mtof(root - 12), int(B * SR)) + saw(mtof(root - 5) * 1.002, int(B * SR)), 300) * .05)   # drone
            for s in (0, 4, 8, 12): drum(M, t0 + s * st, 40, .3, .7 if s == 0 else .45)   # frame drum heartbeat
            if i % 4 == 2: rainstick(M, t0, B, .5)
        elif name == 'africa':
            for k in range(8): M.add('keys', t0 + k * 2 * st, lp(ks(mtof((tones + [tones[0] + 12, tones[1] + 12])[[0, 2, 1, 3, 4, 2, 3, 1][k]] + 12), 2 * st * 3, .7, .9985), 6000) * .3, pan=-.2)   # kora
            for s, kind_ in ((0, 'b'), (3, 't'), (4, 's'), (6, 't'), (8, 'b'), (10, 's'), (11, 't'), (14, 's')):   # djembe: bass, tone, slap
                if kind_ == 'b': drum(M, t0 + s * st, 41, .2, .8)
                elif kind_ == 't': drum(M, t0 + s * st, 60, .07, .5, pan=.2)
                else: click(M, t0 + s * st, 2200, .6, pan=.25)
        elif name == 'finale':
            for s, dn in ((0, 1), (3, 0), (6, 1), (8, 1), (11, 0), (14, 1)): strum(M, t0 + s * st, [root + 12] + tones, st * 2.5, .2, bright=.6, down=bool(dn))
            harmonium(M, t0, tones[:3], B * .97, .5)
            for s in (0, 8): taiko(M, t0 + s * st, .7)
            for s in (4, 12): drum(M, t0 + s * st, 60, .07, .5); click(M, t0 + s * st, 2200, .5)
            for k in range(16): drum(M, t0 + k * st, 52, .06, .2)
            if i == 0: gong(M, t0, .7)
    if tanpura_on:
        t1 = tanpura_on[0]; sub = Mix(8 * B + 2); tanpura(sub, 8 * B, 1., step=8 * st)   # one pluck every 2 beats, locked to the tabla; M.add('drone', t1, sub.buses['drone'][0], sub.buses['drone'][1])
    M.buses['flute_d'] = pingpong(M.buses['flute'], 3 * st, .25)
    render(M, 'Winds_of_the_World_104bpm', sends={'flute': .35, 'keys': .2, 'perc': .2, 'harm': .2, 'tabla': .12, 'drone': .3},
           levels={'flute': 1.1, 'flute_d': .3, 'keys': 1., 'perc': .9, 'harm': .8, 'tabla': .9, 'drone': .6, 'perc_': 1}, duck=(), fade=0.)

# ---------------- Marshmello-style future bass ----------------
def chop(M, t, n, dur, vol):   # pitched-up 'vocal chop' lead
    voice(M, 'lead', t, n, min(dur, .3) * .9, .9 * vol)
LEADS['chop'] = lambda M, t, n, d, v: chop(M, t, n + 12, d, v)
def fb_drums(M, t0, st, S, i, n, tones, root):   # half-time future-bass beat
    kick(M, t0, .9); kick(M, t0 + S(10), .7); snare(M, t0 + S(8), .8); clap(M, t0 + S(8), .8)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .25)
    if i % 4 == 3:
        for k in range(12, 16): snare(M, t0 + S(k), .4)
def build_sweep(M, t0, st, S, i, n, tones, root):   # chords speed up and open up, kicks pulse, chops climb, then one beat of silence
    rate = [4, 2, 1, 1][min(i, 3)]; stop = 16 if i < 3 else 12; cut = 700 * 2 ** (i * .9)
    for s in range(0, stop, rate):
        for c in tones[:4]: supersaw(M, 'keys', t0 + s * st, c + 12, st * rate * .8, .045 * (.7 + .15 * i), cut=cut, a=.004, r=.05, voices=3)
    for s in range(0, stop, 4 if i < 2 else 2): kick(M, t0 + s * st, .55 + .1 * i, punch=1.2)
    if i >= 2:
        arp = [c + 12 for c in tones[:3]] + [c + 24 for c in tones[:3]]
        for k in range(0, stop, 2 if i == 2 else 1): chop(M, t0 + k * st, arp[(k // (2 if i == 2 else 1)) % len(arp)] + (12 if i == 3 and k >= 6 else 0), st * .9, .6)
    if i == 3: crash(M, t0 + 12 * st, .25)
def build_roll(M, t0, st, S, i, n, tones, root):
    for s in np.arange(0, 16, [4, 2, 1, .5][min(i, 3)]): snare(M, t0 + s * st, .3 + .1 * i)

# ---------------- Charli xcx (Brat-era) club ----------------
def rave(M, t0, st, S, tones, vol):   # abrasive distorted saw stabs on the offbeats
    for s in (2, 6, 10, 14, 15):
        N = int(st * 1.2 * SR); x = np.zeros(N)
        for c in tones:
            for d in (-.2, 0, .2): x += saw(mtof(c + 12 + d), N)
        x = np.tanh(x * .6) * envN(N, st, .002, .1, .7, .02); M.add('keys', t0 + S(s), lp(x, 5000) * vol * .12)
def brat_keys(M, style, t0, st, S, tones, root, v):
    if style == 'rave': return rave(M, t0, st, S, tones, v)
    return _orig_keys(M, style, t0, st, S, tones, root, v)
_orig_keys = popkit.keys_bar; popkit.keys_bar = brat_keys

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d
MELLO = [[76,-1,76,79,-1,76,74,72],[74,-1,-1,71,-1,72,74,-1],[72,-1,72,76,-1,79,-1,76],[77,-1,-1,76,-1,72,-1,-1]]
CHARLI = [[76,-1,0,76,-1,74,0,71],[72,-1,0,72,74,-1,0,0],[74,-1,0,74,-1,78,0,74],[71,-1,-1,-1,0,0,0,0]]
def blocks(rows4):
    flat = [x for r in rows4 * 2 for x in r]; ev = []
    for i, x in enumerate(flat):
        if x > 0:
            L = 1
            while i + L < len(flat) and flat[i + L] == -1: L += 1
            ev.append((i * 2, x, L * 2))
    return [[(s - 32 * b, n, min(L, 32 * (b + 1) - s)) for s, n, L in ev if 32 * b <= s < 32 * (b + 1)] for b in range(4)]

SONGS = {
 'mello': ('pop', dict(file='Sugar_Cloud_Smile', title='Sugar Cloud Smile', bpm=140, chorus_keys=True, sections={
   'intro': sec(4, ['Fmaj7', 'G', 'Em7', 'Am'], keys=['piano'], lead='chop', mel=MELLO, lv=.7),
   'verse': sec(8, ['Fmaj7', 'G', 'Em7', 'Am'], keys=['piano', 'pluck'], drums='halfpop', bass='long', lead='voice', lv=.8,
                mel=[[72,-1,72,74,-1,72,71,-1],[71,-1,-1,67,-1,69,71,-1],[72,-1,74,76,-1,74,-1,72],[72,-1,-1,-1,0,0,0,0]]),
   'build': sec(4, ['Fmaj7', 'G', 'Am', 'G'], keys=['pad'], kv=.6, extra=build_sweep, kind='pre'),
   'drop': sec(8, ['Fmaj7', 'G', 'Em7', 'Am'], keys=['futurebass', 'pluck'], bass='808', lead='chop+synth', impact=True, extra=fb_drums, mel=MELLO),
   'outro': sec(2, ['Fmaj7', 'Fmaj7'], keys=['piano'], fill=False)},
   order=['intro', 'verse', 'build', 'drop', 'verse', 'build', 'drop', 'outro'], levels={'lead': 1.2})),
 'mello_bc': ('bc', dict(file='Sugar_Cloud_Breaks', title='Sugar Cloud Breaks', bpm=174, chords=['Fmaj7', 'G', 'Em7', 'Am'], keys='piano', pad=.07, mel=lambda M, t, n, d, v: chop(M, t, n + 12, d, v),
   melB=lambda M, t, n, d, v: chop(M, t, n + 12, d, v), layerB='lead', bass='808', kit=dict(FUNK, crunch=1.5, clap=.5), patA='P0', patB='P3', melody=blocks(MELLO), seed=191, ending='dropout', targets={'outro': -14.})),
 'charli': ('pop', dict(file='Lime_Green_Afterparty', title='Lime Green Afterparty', bpm=132, sections={
   'intro': sec(4, ['Em', 'C', 'D', 'Bm'], keys=['rave'], bass='heavy808'),
   'verse': sec(8, ['Em', 'C', 'D', 'Bm'], keys=['rave'], drums='fourfloor', bass='heavy808', lead='vocoder', lv=.8,
                mel=[[71,-1,0,71,-1,69,0,67],[67,-1,0,0,69,-1,0,0],[69,-1,0,69,-1,71,0,74],[71,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Em', 'C', 'D', 'Bm'], keys=['rave', 'pad'], drums='fourfloor', bass='heavy808', lead='vocoder+synth', impact=True, mel=CHARLI),
   'break': sec(4, ['Em', 'Em', 'C', 'D'], keys=['pad'], bass='heavy808', riser=True, kind='bridge'),
   'outro': sec(2, ['Em', 'Em'], keys=['rave'], drums='fourfloor', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'break', 'chorus', 'outro'], levels={'lead': 1.2, 'sub': 1.1})),
 'charli_bc': ('bc', dict(file='Lime_Green_Breaks', title='Lime Green Breaks', bpm=172, chords=['Em', 'C', 'D', 'Bm'],
   keys=lambda M, t0, st, tones, root, vol, bar: rave(M, t0, st, lambda k: k * st, tones, vol), pad=.04, mel=lambda M, t, n, d, v: popkit.vocoder(M, t, n, d * .95, v),
   melB=lambda M, t, n, d, v: popkit.vocoder(M, t, n, d * .95, v), layerB='lead', bass='808', kit=dict(FUNK, crunch=2.4, clap=.5, punch=1.4), patA='P4', patB='P2', melody=blocks(CHARLI), seed=201, levels={'sub': 1.},
   ending='none', sections=[('intro', 8), ('build', 4), ('dropA', 16), ('half', 8), ('dropB', 16), ('outro', 4)])),
}

if __name__ == '__main__':
    names = ['flutes'] + list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names:
        if k == 'flutes': winds_of_the_world(); continue
        kind, cfg = SONGS[k]
        (pbuild if kind == 'pop' else bbuild)(cfg)
