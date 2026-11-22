"""Bengali / South Asian-inspired songs. Every sound is code: tabla, dotara, ektara, harmonium, bansuri, tanpura.
python southasia.py song   -> Riverbank Evening (Baul-folk style, kaharba rhythm, Khamaj-flavoured melody, tihai ending)
python southasia.py breaks -> Monsoon Breaks (steady breakcore with tabla, harmonium and bansuri)"""
import sys
from engine import *
from instruments2 import ks, envN
from songs import render, sections_to_bars

SA = 62  # Sa = D4

# ---------------- instruments ----------------
def bayan(M, t, vol=1., glide=False):          # tabla bass drum (left), optional pitch rise (the 'ge' meend)
    N = int(.6 * SR); tt = tarr(N); f = 95 * (1 + (.35 * (1 - np.exp(-tt / .12)) if glide else .1 * np.exp(-tt / .03)))
    M.add('tabla', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / (.45 if glide else .3)) * vol * .8, pan=-.15)
def dayan(M, t, vol=1., open_=True, n=SA):      # tabla treble drum (right), tuned to Sa; open = ringing 'na', closed = 'ti'
    N = int(.5 * SR); tt = tarr(N); f = mtof(n); dec = .28 if open_ else .045; x = np.zeros(N)
    for h, a in ((1, 1.), (2, .6), (3, .45), (4, .25), (5, .12)): x += a * np.sin(2 * np.pi * f * h * tt) * np.exp(-tt / (dec / (1 + .25 * h)))
    x += bp(noise(N), 2000, 7000) * np.exp(-tt / .006) * .5
    M.add('tabla', t, x * vol * .35, pan=.15)
def ka(M, t, vol=1.):                           # flat slap on the bass drum
    N = int(.08 * SR); M.add('tabla', t, lp(noise(N), 1500) * np.exp(-tarr(N) / .012) * vol * .5, pan=-.15)
BOL = {'dha': lambda M, t, v: (bayan(M, t, v), dayan(M, t, v)), 'ge': lambda M, t, v: bayan(M, t, v, glide=True),
       'na': lambda M, t, v: dayan(M, t, v), 'ti': lambda M, t, v: dayan(M, t, v * .8, open_=False),
       'ka': lambda M, t, v: ka(M, t, v), 'dhi': lambda M, t, v: (bayan(M, t, v), dayan(M, t, v * .7, open_=False)), '-': lambda M, t, v: None}
KAHARBA = ['dha', 'ge', 'na', 'ti', 'na', 'ka', 'dhi', 'na']   # 8 beats, one per eighth note
def tabla_bar(M, t0, st, vol=1., fill=False):
    bols = KAHARBA if not fill else ['dha', 'ti', 'dha', 'ti', 'dha', 'ge', 'na', 'dha']
    for k, b in enumerate(bols): BOL[b](M, t0 + k * 2 * st, vol * (1. if k in (0, 6) else .75))
    if fill:
        for k in (9, 11, 13): dayan(M, t0 + k * st, vol * .5, open_=False)
def dotara(M, t, n, dur, vol, pan=-.2):
    y = ks(mtof(n), min(dur, 1.5) + .2, .85, .997); N = len(y); tt = tarr(N)
    idx = np.clip(np.cumsum(1 - .02 * np.exp(-tt / .03)), 0, N - 1)   # tiny slide up into the note
    M.add('dotara', t, lp(np.interp(idx, np.arange(N), y), 7000) * vol * .45, pan=pan)
def ektara(M, t, vol=1.):                       # one string, squeezed: pitch bends up then relaxes ('boing')
    N = int(.7 * SR); y = ks(mtof(SA - 12), .6, .7, .996)[:N]; tt = tarr(len(y))
    rate = 1 + .06 * np.sin(np.pi * np.clip(tt / .35, 0, 1)); idx = np.clip(np.cumsum(rate), 0, len(y) - 1)
    M.add('dotara', t, np.interp(idx, np.arange(len(y)), y) * vol * .35, pan=.3)
def harmonium(M, t, notes, dur, vol):
    N = int((dur + .15) * SR); tt = tarr(N); x = np.zeros(N)
    for n in notes: x += saw(mtof(n), N) * .5 + sqr(mtof(n), N, .45) * .3
    x = lp(x, 2400) + .4 * bp(x, 900, 1600); x *= 1 + .08 * np.sin(2 * np.pi * 5 * tt)   # bellows tremolo
    M.add('harm', t, x * envN(N, dur, .06, .2, .9, .12) * vol * .07)
def bansuri(M, t, n, dur, vol, prev=None, pan=.1):
    N = int((dur + .15) * SR); tt = tarr(N)
    meend = ((prev - n) * np.exp(-tt / .05)) if prev else -.6 * np.exp(-tt / .04)      # glide from the last note
    vib = np.clip((tt - .25) / .25, 0, 1) * .22 * np.sin(2 * np.pi * 5.2 * tt)
    f = mtof(n + meend + vib); x = sine(f, N) + .25 * sine(2 * f, N) + .08 * sine(3 * f, N)
    x += bp(noise(N), 1200, 6000) * (.06 + .1 * np.exp(-tt / .08))
    M.add('flute', t, x * envN(N, dur, .05, .3, .85, .1) * vol * .32, pan=pan)
def tanpura(M, T, vol=1., step=.9):                      # drone: Pa, Sa, Sa, low Sa, plucked over and over with the buzzing 'jawari'
    t = 0.; seq = [SA - 5, SA, SA, SA - 12]; k = 0
    while t < T:
        y = ks(mtof(seq[k % 4] - 12), 2.5, .5, .9995); y = y + .3 * bp(np.tanh(y * 4), 1500, 4500)
        M.add('drone', t, y * vol * .22, pan=(-.3, .3)[k % 2]); t += step; k += 1

def chordtones(name):
    return {'D': [57, 62, 66], 'C': [55, 60, 64], 'G': [55, 59, 62], 'A': [57, 61, 64], 'Em': [55, 59, 64]}[name]

# =====================================================================
# RIVERBANK EVENING — 96 BPM, Baul-folk style
# =====================================================================
def riverbank():
    bpm = 96; st = 60 / bpm / 4; B = 16 * st
    riff = [(0, 62, 2), (2, 66, 1), (3, 67, 1), (4, 69, 2), (6, 67, 1), (7, 66, 1), (8, 64, 2), (10, 62, 2), (12, 60, 2), (14, 62, 2)]
    VERSE = [[(0, 74, 4), (4, 76, 2), (6, 78, 2), (8, 79, 4), (12, 78, 2), (14, 76, 2)], [(0, 74, 6), (6, 72, 2), (8, 71, 4), (12, 69, 4)],
             [(0, 72, 4), (4, 74, 2), (6, 72, 2), (8, 71, 4), (12, 69, 4)], [(0, 67, 4), (4, 69, 4), (8, 72, 8)],
             [(0, 71, 4), (4, 72, 2), (6, 74, 2), (8, 76, 4), (12, 74, 2), (14, 72, 2)], [(0, 71, 6), (6, 69, 2), (8, 67, 8)],
             [(0, 69, 4), (4, 71, 2), (6, 72, 2), (8, 74, 4), (12, 72, 2), (14, 71, 2)], [(0, 74, 16)]]
    REFR = [[(0, 79, 4), (4, 81, 4), (8, 83, 4), (12, 81, 4)], [(0, 81, 6), (6, 79, 2), (8, 78, 4), (12, 76, 4)],
            [(0, 78, 4), (4, 76, 2), (6, 74, 2), (8, 76, 4), (12, 78, 4)], [(0, 74, 16)],
            [(0, 79, 2), (2, 79, 2), (4, 83, 4), (8, 84, 4), (12, 83, 4)], [(0, 81, 4), (4, 79, 4), (8, 78, 4), (12, 76, 4)],
            [(0, 74, 4), (4, 76, 4), (8, 78, 4), (12, 76, 4)], [(0, 74, 16)]]
    VCH = ['D', 'D', 'C', 'C', 'G', 'G', 'D', 'D']; RCH = ['G', 'A', 'D', 'D', 'G', 'A', 'D', 'D']
    secs = [('alap', 4), ('theme', 8), ('verse', 8), ('refrain', 8), ('inter', 8), ('verse', 8), ('refrain', 8), ('tihai', 3)]
    bars = sections_to_bars(secs); T = len(bars) * B + 6; M = Mix(T); prev = [None]
    tanpura(M, T - 2, 1.)
    def fl(t, nn, d, v=1.):
        bansuri(M, t, nn, d, v, prev=prev[0]); prev[0] = nn
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B
        name = RCH[i % 8] if sec == 'refrain' else VCH[i % 8]
        if sec == 'alap':   # free, slow flute over the drone
            for s, nn, L in [[(0, 69, 12)], [(0, 71, 6), (6, 72, 6)], [(0, 74, 8), (8, 72, 4), (12, 71, 4)], [(0, 69, 16)]][i]: fl(t0 + s * st, nn, L * st * .97, .8)
            continue
        if sec == 'tihai':   # the phrase three times, the last note landing on the downbeat (sam)
            phrase = [(0, 74, 2), (2, 76, 2), (4, 78, 2), (6, 76, 2), (8, 74, 4)]
            if i == 0:
                for start in (12, 26, 40):
                    for s, nn, L in phrase:
                        tt = t0 + (start + s) * st
                        fl(tt, nn, L * st * .95, 1.1); dotara(M, tt, nn - 12, L * st, .8)
                        BOL['dha' if s in (0, 8) else 'na'](M, tt, .9)
                harmonium(M, t0, chordtones('D'), 3 * B, .8)
                sam = t0 + 48 * st
                for nn in (50, 57, 62, 66, 69, 74): dotara(M, sam, nn, 2.5, .3)
                harmonium(M, sam, [50, 57, 62, 66], 3., .6)
                bansuri(M, sam, 74, 2.5, .85, prev=76); bayan(M, sam, .6); dayan(M, sam, .6); ektara(M, sam, .55)
            continue
        harmonium(M, t0, chordtones(name), B * .97, .9 if sec in ('refrain', 'inter') else .7)
        tabla_bar(M, t0, st, .9 if sec in ('refrain', 'inter') else .75, fill=(i % 4 == 3))
        for s in (0, 6, 8, 12): ektara(M, t0 + s * st, .8 if s == 0 else .55)
        if sec in ('theme', 'inter', 'refrain'):
            tr = {'D': 0, 'C': -2, 'G': -7, 'A': -5}[name]
            for s, nn, L in riff: dotara(M, t0 + s * st, nn + tr + (12 if sec == 'inter' and i >= 4 else 0), L * st, .7 if sec != 'refrain' else .45)
        if sec == 'verse':
            for s, nn, L in VERSE[i % 8]: fl(t0 + s * st, nn, L * st * .96)
            for k in range(4): dotara(M, t0 + k * 4 * st, chordtones(name)[k % 3], 2 * st, .35)
        if sec == 'refrain':
            for s, nn, L in REFR[i % 8]: fl(t0 + s * st, nn, L * st * .96, 1.1)
        if sec == 'inter' and i >= 4:
            for s, nn, L in VERSE[i % 8]: fl(t0 + s * st, nn - 12, L * st * .96, .7)
    M.buses['flute_d'] = pingpong(M.buses['flute'], 3 * st, .25)
    render(M, 'Riverbank_Evening_96bpm', sends={'flute': .35, 'dotara': .2, 'harm': .25, 'tabla': .12, 'drone': .3},
           levels={'flute': 1.1, 'flute_d': .3, 'dotara': 1., 'harm': .8, 'tabla': 1., 'drone': .6}, duck=(), fade=0.)

# =====================================================================
# MONSOON BREAKS — steady breakcore with Bengali instruments
# =====================================================================
def monsoon_breaks():
    from breakcore_engine import build
    from seasons import FUNK
    def keys(M, t0, st, tones, root, vol, bar):        # harmonium + ektara + a little dotara
        harmonium(M, t0, tones[:3], 16 * st * .97, .8 * vol)
        for s in (0, 6, 8, 12): ektara(M, t0 + s * st, (.7 if s == 0 else .5) * vol)
        for k in range(0, 16, 4): dotara(M, t0 + k * st, tones[(k // 4) % 3] + 12, 2 * st, .35 * vol)
    def flute(M, t, n, dur, vol):
        bansuri(M, t, n, dur * .96, 1.1 * vol)
    def dot(M, t, n, dur, vol):
        dotara(M, t, n, dur, .8 * vol, pan=.2)
    def extra(M, sec, i, t0, st, tones, root):          # tabla rides along: full kaharba in quiet parts, lighter in the drops
        if sec in ('intro', 'half', 'outro'): tabla_bar(M, t0, st, .85, fill=(i % 4 == 3))
        elif sec in ('dropA', 'dropB'):
            for k, b in enumerate(KAHARBA):
                if k % 2 == 0: BOL[b](M, t0 + k * 2 * st, .55)
    cfg = dict(file='Monsoon_Breaks', title='Monsoon Breaks', bpm=172, chords=['D', 'C', 'G', 'D'], keys=keys, pad=.05, mel=flute, melB=flute, layerB=dot, bass='sub',
               kit=dict(FUNK, crunch=1.4, clap=.25), patA='P1', patB='P3', amb=[('rain', .6)], extra=extra, seed=151, verb=2.6, decay=.65,
               melody=[[(0, 74, 4), (4, 76, 2), (6, 78, 2), (8, 79, 4), (12, 78, 2), (14, 76, 2), (16, 74, 6), (22, 72, 2), (24, 71, 4), (28, 69, 4)],
                       [(0, 72, 4), (4, 74, 2), (6, 72, 2), (8, 71, 4), (12, 69, 4), (16, 67, 4), (20, 69, 4), (24, 72, 8)],
                       [(0, 71, 4), (4, 72, 2), (6, 74, 2), (8, 76, 4), (12, 74, 2), (14, 72, 2), (16, 71, 6), (22, 69, 2), (24, 67, 8)],
                       [(0, 69, 4), (4, 71, 2), (6, 72, 2), (8, 74, 4), (12, 72, 2), (14, 71, 2), (16, 74, 16)]],
               levels={'tabla': .9, 'harm': .8, 'dotara': 1., 'flute': 1.1})
    build(cfg)

if __name__ == '__main__':
    {'song': riverbank, 'breaks': monsoon_breaks}[sys.argv[1]]()
