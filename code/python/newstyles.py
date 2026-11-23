"""Extra instruments and styles for popkit (all synthesized in code): Mario-style world instruments, more hyperpop sounds,
and new genres (phonk, synthwave, dubstep, eurobeat, ska, reggae, amapiano, bluegrass, city pop, jersey club).
Importing this file registers the styles with popkit."""
import numpy as np, scipy.signal as ss
import popkit
from popkit import LEADS, EXTRA_KEYS, EXTRA_DRUMS, EXTRA_BASS, chord, b808, subbass, heavy808, gbpulse, glitch
from engine import *
from instruments2 import ks, envN, voice, guitar, fbass
from songs import piano, ride
from songs3 import mallet, glock, flute, timpani, sleigh, tri, choir, rim
from songs5 import pizz, violins, clarinet, oboe, horn, cymbal
from songs9 import organ, chick
from songs4 import dist_gtr, power
from breakcore_engine import QUAL, koto

QUAL.update({'dim': [0, 3, 6], 'm6': [0, 3, 7, 9], '9': [0, 4, 7, 10, 14], 'aug': [0, 4, 8], 'm7b5': [0, 3, 6, 10], '7b9': [0, 4, 7, 10, 13]})

# ======================= instruments =======================
def bah(M, t, n, vol=1.):                 # the bouncy group 'bah!' vocal hit (formant voices + a soft 'b')
    for d, p in ((0, -.2), (7, .2), (12, 0)): voice(M, 'perc', t, n - 12 + d, .14, .55 * vol, pan=p)
    N = int(.02 * SR); M.add('perc', t, lp(noise(N), 900) * np.exp(-tarr(N) / .004) * vol * .25)
def steel(M, bus, t, n, dur, vol, pan=.1):
    N = int((min(dur, 1.2) + .4) * SR); tt = tarr(N); f = mtof(n)
    x = np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt / .15) + .25 * np.sin(2 * np.pi * f * 3.01 * tt) * np.exp(-tt / .08)
    M.add(bus, t, x * np.exp(-tt / .45) * np.clip(tt / .002, 0, 1) * vol * .3, pan=pan)
def marimba(M, bus, t, n, dur, vol, pan=0.): mallet(M, bus, t, n, dur, vol, ratio=4., dec=.3, pan=pan)
def xylo(M, bus, t, n, dur, vol, pan=0.): mallet(M, bus, t, n + 12, dur, vol * .8, ratio=3., dec=.15, pan=pan)
def celesta(M, bus, t, n, dur, vol, pan=0.): mallet(M, bus, t, n + 12, dur, vol * .7, ratio=4., dec=.7, pan=pan)
def bongo(M, t, hi=True, vol=1., pan=.3):
    N = int(.25 * SR); tt = tarr(N); f = (420 if hi else 300) * (1 + .15 * np.exp(-tt / .01))
    M.add('perc', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .07) * vol * .3, pan=pan if hi else -pan)
def conga(M, t, n=50, vol=1., pan=-.25):
    N = int(.35 * SR); tt = tarr(N); f = mtof(n) * (1 + .1 * np.exp(-tt / .015))
    M.add('perc', t, (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .12) + bp(noise(N), 1500, 5000) * np.exp(-tt / .006) * .3) * vol * .35, pan=pan)
def woodblock(M, t, hi=True, vol=1.):
    N = int(.06 * SR); tt = tarr(N); f = 1700 if hi else 1150
    M.add('perc', t, np.sin(2 * np.pi * f * tt) * np.exp(-tt / .015) * vol * .3, pan=.3 if hi else -.3)
def cowbell(M, t, n=None, dur=.25, vol=1., bus='perc'):   # TR-808 cowbell (pitched when n is given)
    N = int((dur + .2) * SR); tt = tarr(N); f1 = mtof(n) if n else 540.; f2 = f1 * 1.48
    x = bp(sqr(f1, N) + sqr(f2, N), f1 * .8, f2 * 2.5) * (np.exp(-tt / .03) * .6 + .4 * np.exp(-tt / max(dur, .05)))
    M.add(bus, t, x * vol * .22, pan=-.1)
def logdrum(M, t, n, dur, vol):           # amapiano log drum: punchy pitched thump with a drop
    N = int((dur + .2) * SR); tt = tarr(N); f = mtof(n) * (1 + .5 * np.exp(-tt / .02))
    x = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 2.2) * np.exp(-tt / max(dur * .6, .08))
    M.add('bass', t, lp(x, 900) * vol * .7)
def wobble(M, t, n, dur, vol, rate=2.):   # dubstep wobble: a filter that opens and closes 'rate' times per second
    N = int((dur + .05) * SR); tt = tarr(N); f = mtof(n)
    x = saw(f, N) + saw(f * 1.006, N) + .6 * sqr(f / 2, N)
    lfo = .5 - .5 * np.cos(2 * np.pi * rate * tt)
    y = lp(x, 250) * (1 - lfo) + (lp(x, 2600) + .6 * bp(x, 700, 1400)) * lfo
    y = np.tanh(y * 1.6) * envN(N, dur, .005, .1, 1., .03)
    M.add('bass', t, y * vol * .3)
def banjo(M, bus, t, n, dur, vol, pan=.25):
    y = ks(mtof(n), min(dur, 1.) + .3, .92, .993, pick=.1); y = hp(y, 180) + .5 * bp(y, 1500, 3500)
    M.add(bus, t, y * vol * .45, pan=pan)
def fiddle(M, t, n, dur, vol, pan=0., bus='lead'):
    N = int((dur + .2) * SR); tt = tarr(N); v = np.clip((tt - .15) / .2, 0, 1) * .15 * np.sin(2 * np.pi * 6 * tt)
    f = mtof(n + v); x = saw(f, N) + .4 * saw(f * 1.003, N)
    y = lp(x, 3200) + .5 * bp(x, 2500, 4000); M.add(bus, t, y * envN(N, dur, .03, .2, .85, .08) * vol * .09, pan=pan)
def theremin(M, t, n, dur, vol, prev=None):
    N = int((dur + .2) * SR); tt = tarr(N); gl = ((prev - n) * np.exp(-tt / .08)) if prev else 0
    f = mtof(n + gl + .35 * np.sin(2 * np.pi * 6 * tt) * np.clip(tt / .3, 0, 1)); x = sine(f, N) + .15 * sine(2 * f, N)
    M.add('lead', t, x * envN(N, dur, .08, .2, .9, .15) * vol * .3)
def harpsi(M, bus, t, n, dur, vol, pan=0.):
    y = ks(mtof(n), min(dur, 1.2) + .3, .95, .996, pick=.06); y2 = ks(mtof(n + 12), min(dur, 1.2) + .3, .9, .995, pick=.08)
    M.add(bus, t, hp(y + .45 * y2, 150) * vol * .3, pan=pan)
def oud(M, bus, t, n, dur, vol, pan=-.15):
    y = ks(mtof(n), min(dur, 1.2) + .3, .65, .996, pick=.15); N = len(y); tt = tarr(N)
    idx = np.clip(np.cumsum(1 - .015 * np.exp(-tt / .04)), 0, N - 1); y = np.interp(idx, np.arange(N), y)
    M.add(bus, t, lp(y, 5000) * vol * .5, pan=pan)
def darbuka(M, t, kind, vol=1.):
    if kind == 'doum':
        N = int(.35 * SR); tt = tarr(N); f = 110 * (1 + .3 * np.exp(-tt / .02))
        M.add('perc', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .15) * vol * .55)
    else:
        N = int(.08 * SR); tt = tarr(N)
        M.add('perc', t, (bp(noise(N), 2500, 8000) * .6 + np.sin(2 * np.pi * 1300 * tt)) * np.exp(-tt / .012) * vol * .25, pan=.2)
def gated_snare(M, t, vol=1.):            # 80s gated-reverb snare
    snare(M, t, vol * .9); N = int(.28 * SR); tt = tarr(N)
    M.add('drums', t, bp(noise(N), 400, 6000) * (tt < .22) * np.exp(-tt / .4) * vol * .3)
def squeak(M, t, vol=1.):                 # jersey-club 'bed squeak'
    N = int(.12 * SR); tt = tarr(N); f = 1800 + 900 * np.sin(np.pi * tt / tt[-1])
    M.add('fx', t, np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * bp(np.ones(N), 1, 2) * 0 + lp(np.sin(2 * np.pi * np.cumsum(f) / SR), 4000) * np.sin(np.pi * tt / tt[-1]) * vol * .12, pan=.3)
def chopv(M, t, n, dur, vol, up=12):     # pitched-up vocal chop
    voice(M, 'lead', t, n + up, min(dur, .25) * .9, .9 * vol)
def ayy(M, t, vol=1.):                    # dark pitched-down 'ay' shout (phonk)
    voice(M, 'perc', t, 50, .25, .9 * vol); M.add('perc', t, lp(noise(int(.03 * SR)), 1200) * .15 * vol)
def gtr_skank(M, t, tones, vol, pan=.3):  # short bright upstroke
    for j, c in enumerate(tones[::-1]): M.add('keys', t + j * .004, hp(ks(mtof(c + 12), .16, .8, .985), 300) * vol * .25, pan=pan)
def accordion(M, t, n, dur, vol, bus='lead', pan=-.1):
    N = int((dur + .1) * SR); tt = tarr(N); f = mtof(n)
    x = (saw(f * 2 ** (-.08 / 12), N) + saw(f * 2 ** (.08 / 12), N)) * .5 + sqr(f * 2, N, .4) * .2
    x = lp(x, 3000) + .4 * bp(x, 1000, 1800); x *= 1 + .1 * np.sin(2 * np.pi * 5.5 * tt)
    M.add(bus, t, x * envN(N, dur, .04, .2, .9, .08) * vol * .16, pan=pan)
def tuba(M, t, n, dur, vol):
    N = int((dur + .15) * SR); tt = tarr(N); f = mtof(n)
    x = tri(f, N) + .6 * lp(saw(f, N), 500); M.add('bass', t, x * envN(N, dur, .02, .2, .8, .08) * vol * .35)
def ocarina(M, t, n, dur, vol, pan=0.):
    N = int((dur + .1) * SR); tt = tarr(N); v = np.clip((tt - .2) / .2, 0, 1) * .15 * np.sin(2 * np.pi * 5 * tt)
    f = mtof(n + v); x = sine(f, N) + .05 * sine(3 * f, N) + bp(noise(N), 1500, 4000) * .03
    M.add('lead', t, x * envN(N, dur, .03, .2, .9, .06) * vol * .35, pan=pan)
def plastic(M, bus, t, n, dur, vol, pan=0.):   # glossy 'plastic' bell-synth (bubblegum hyperpop)
    N = int((min(dur, .8) + .3) * SR); tt = tarr(N); f = mtof(n)
    x = np.sin(2 * np.pi * f * tt + 2.5 * np.exp(-tt / .08) * np.sin(2 * np.pi * f * 5 * tt)) + .4 * sqr(f, N, .25) * np.exp(-tt / .1)
    M.add(bus, t, x * np.exp(-tt / .35) * np.clip(tt / .002, 0, 1) * vol * .25, pan=pan)
def clank(M, t, vol=1.):
    N = int(.25 * SR); tt = tarr(N); x = sum(np.sin(2 * np.pi * f * tt) for f in (523, 1307, 2219, 3511)) * np.exp(-tt / .06)
    M.add('perc', t, x * vol * .08, pan=rng.uniform(-.4, .4))
def stutter(M, t, n, st, vol, k=4):        # hyperpop stutter on one note
    for j in range(k): supersaw(M, 'keys', t + j * st / 2, n, st * .22, .05 * vol, cut=6000, a=.001, r=.01, voices=3)

# ======================= leads =======================
LEADS.update({
 'steel': lambda M, t, n, d, v: steel(M, 'lead', t, n, d, 1.1 * v),
 'marimba': lambda M, t, n, d, v: marimba(M, 'lead', t, n, d, 1.2 * v),
 'xylo': lambda M, t, n, d, v: xylo(M, 'lead', t, n, d, 1.1 * v),
 'celesta': lambda M, t, n, d, v: celesta(M, 'lead', t, n, d, 1.1 * v),
 'banjo': lambda M, t, n, d, v: banjo(M, 'lead', t, n, d, 1.1 * v, pan=0.),
 'fiddle': lambda M, t, n, d, v: fiddle(M, t, n, d * .95, v),
 'theremin': lambda M, t, n, d, v: theremin(M, t, n, d * .97, v),
 'harpsi': lambda M, t, n, d, v: harpsi(M, 'lead', t, n, d, 1.1 * v),
 'oud': lambda M, t, n, d, v: oud(M, 'lead', t, n, d, 1.1 * v, pan=0.),
 'cowbell': lambda M, t, n, d, v: cowbell(M, t, n, min(d, .35), 1.6 * v, bus='lead'),
 'clarinet': lambda M, t, n, d, v: clarinet(M, t, n, d * .93, 1.2 * v),
 'oboe': lambda M, t, n, d, v: oboe(M, t, n, d * .93, 1.1 * v),
 'accordion': lambda M, t, n, d, v: accordion(M, t, n, d * .93, v),
 'ocarina': lambda M, t, n, d, v: ocarina(M, t, n, d * .93, v),
 'plastic': lambda M, t, n, d, v: plastic(M, 'lead', t, n, d, 1.2 * v),
 'chop': lambda M, t, n, d, v: chopv(M, t, n, d, v, 12),
 'chipmunk': lambda M, t, n, d, v: chopv(M, t, n, d, v, 19),
 'horn': lambda M, t, n, d, v: horn(M, t, n, d * .93, 1.1 * v),
 'organ': lambda M, t, n, d, v: organ(M, t, n, d * .95, .9 * v),
 'saw80s': lambda M, t, n, d, v: supersaw(M, 'lead', t, n, d * .93, .2 * v, cut=2600, a=.02, r=.25, voices=4, detune=.1),
 'sqbright': lambda M, t, n, d, v: leadsq(M, 'lead', t, n + 12, d * .9, .4 * v),
 'emogtr': lambda M, t, n, d, v: guitar(M, 'lead', t, n, d * 1.2, .55 * v, bright=.5, decay=.998),
})

# ======================= keys styles =======================
def K(name):
    def deco(f): EXTRA_KEYS[name] = f; return f
    return deco
@K('stride')
def _(M, t0, st, S, T, r, v):            # ragtime/stride piano: bass on 1 and 3, chord on 2 and 4
    for s, low in ((0, True), (4, False), (8, True), (12, False)):
        if low: piano(M, 'keys', t0 + S(s), r + 12 + (7 if s == 8 else 0), st * 3, .45 * v, pan=-.2)
        else:
            for c in T[:3]: piano(M, 'keys', t0 + S(s), c + 12, st * 2.5, .2 * v, pan=.1)
@K('steelcomp')
def _(M, t0, st, S, T, r, v):
    for s in (2, 6, 7, 10, 14):
        for c in T[:3]: steel(M, 'keys', t0 + S(s), c + 12, st * 2, .45 * v, pan=.3)
@K('marimbaarp')
def _(M, t0, st, S, T, r, v):
    arp = T[:3] + [T[0] + 12]
    for k in range(8): marimba(M, 'keys', t0 + S(2 * k), arp[[0, 1, 2, 3, 2, 1, 2, 1][k]] + 12, st * 2, .7 * v, pan=-.3 + .6 * (k % 2))
@K('pizzarp')
def _(M, t0, st, S, T, r, v):
    for k in range(8): pizz(M, t0 + S(2 * k), (T[:3] + [T[0] + 12])[[0, 2, 1, 3, 1, 2, 0, 2][k]] + 12, .8 * v, pan=.3)
@K('skank')
def _(M, t0, st, S, T, r, v):
    for s in (2, 6, 10, 14): gtr_skank(M, t0 + S(s), T[:3], .9 * v)
@K('reggae')
def _(M, t0, st, S, T, r, v):            # skank on 2 and 4 + organ 'bubble'
    for s in (4, 12): gtr_skank(M, t0 + S(s), T[:3], v)
    for s in (2, 3, 6, 7, 10, 11, 14, 15):
        for c in T[:3]: organ(M, t0 + S(s), c + 12, st * .6, .22 * v, pan=-.3)
@K('bluegrass')
def _(M, t0, st, S, T, r, v):            # banjo forward rolls + boom-chuck guitar
    roll = [T[0] + 12, T[1] + 12, T[2] + 24, T[0] + 12, T[1] + 12, T[2] + 24, T[0] + 12, T[1] + 12]
    for k in range(16): banjo(M, 'keys', t0 + S(k), roll[k % 8], st * 2, .5 * v)
    for s in (0, 8): M.add('keys', t0 + S(s), lp(ks(mtof(r + 24 + (7 if s == 8 else 0)), .5, .5, .99), 3000) * .3 * v, pan=-.3)
    for s in (4, 12):
        for j, c in enumerate(T[:3]): M.add('keys', t0 + S(s) + j * .008, lp(ks(mtof(c + 12), .3, .6, .985), 5000) * .18 * v, pan=-.3)
@K('synthwave')
def _(M, t0, st, S, T, r, v):            # 16th arpeggio + lush pad
    arp = [T[0], T[1], T[2], T[0] + 12]
    for k in range(16): pluck(M, 'keys', t0 + S(k), arp[k % 4] + 12, st * .9, .09 * v, pan=(-.35, .35)[k % 2], dec=.12, cut=3500)
    for c in T: supersaw(M, 'pad', t0, c + 12, 16 * st, .05 * v, cut=1800, a=.4, r=.6, voices=4, detune=.12)
@K('eurobeat')
def _(M, t0, st, S, T, r, v):            # offbeat supersaw stabs + 16th arpeggio
    for s in (2, 6, 10, 14):
        for c in T[:3]: supersaw(M, 'keys', t0 + S(s), c + 12, st * 1.4, .06 * v, cut=4500, a=.003, r=.05, voices=5)
    arp = [T[0] + 24, T[2] + 12, T[1] + 12, T[2] + 12]
    for k in range(16): pluck(M, 'keys', t0 + S(k), arp[k % 4], st * .8, .07 * v, pan=.3, dec=.06, cut=4500)
@K('citypop')
def _(M, t0, st, S, T, r, v):
    for s, L in ((0, 3), (3, 3), (6, 2), (10, 2), (12, 4)):
        for j, c in enumerate(T[:4]): epiano(M, 'keys', t0 + S(s) + j * .005, c + 12 if c < 60 else c, st * L * .9, .075 * v, pan=(j - 1.5) * .2)
    for k in range(16):
        if k % 4 in (2, 3) or k in (5, 13): chick(M, t0 + S(k), T + [T[0] + 12], .12 * v)
@K('amapiano')
def _(M, t0, st, S, T, r, v):            # syncopated jazzy piano + airy pad
    for s in (0, 3, 6, 11, 14):
        for c in T[:4]: piano(M, 'keys', t0 + S(s), c + 12, st * 1.5, .18 * v)
    for c in T[:3]: supersaw(M, 'pad', t0, c + 12, 16 * st, .035 * v, cut=1500, a=.5, r=.6, voices=3)
@K('harpsi')
def _(M, t0, st, S, T, r, v):
    arp = T[:3] + [T[0] + 12]
    for k in range(8): harpsi(M, 'keys', t0 + S(2 * k), arp[[0, 2, 1, 3, 2, 1, 0, 2][k]], st * 2, .6 * v, pan=-.25)
@K('churchorgan')
def _(M, t0, st, S, T, r, v):
    for c in T[:3] + [r + 12]: organ(M, t0, c + 12, 16 * st * .97, .4 * v)
@K('oud')
def _(M, t0, st, S, T, r, v):
    for s, o in ((0, 0), (3, 1), (4, 2), (6, 1), (8, 0), (11, 1), (12, 2), (14, 3)):
        oud(M, 'keys', t0 + S(s), (T[:3] + [T[0] + 12])[o] + 12, st * 2, .55 * v)
@K('celesta')
def _(M, t0, st, S, T, r, v):
    arp = T[:3] + [T[0] + 12]
    for k in range(8): celesta(M, 'keys', t0 + S(2 * k), arp[[0, 1, 2, 3, 2, 3, 1, 2][k]] + 12, st * 2, .6 * v, pan=.3)
@K('uke')
def _(M, t0, st, S, T, r, v):
    for s, dn in ((0, True), (3, True), (6, False), (8, True), (10, False), (12, True), (14, False)):
        seq = [c + 12 for c in T[:3]] if dn else [c + 12 for c in T[:3][::-1]]
        for j, c in enumerate(seq): M.add('keys', t0 + S(s) + j * .01, lp(ks(mtof(c), .3, .7, .99), 6000) * .12 * v, pan=.25)
@K('brasshits')
def _(M, t0, st, S, T, r, v):
    for s, L in ((0, 2), (6, 1), (10, 2)):
        for c in T[:3]: brass(M, 'keys', t0 + S(s), c + 12, st * L, .16 * v)
@K('plastic')
def _(M, t0, st, S, T, r, v):            # glossy bell chords that bounce
    for s in (0, 3, 6, 8, 11, 14):
        for c in T[:3]: plastic(M, 'keys', t0 + S(s), c + 24, st * 1.5, .4 * v, pan=.2)
@K('emoacoustic')
def _(M, t0, st, S, T, r, v):
    for s, dn in ((0, True), (4, True), (6, False), (10, False), (12, True), (14, False)):
        seq = ([r + 12] + T) if dn else T[::-1]
        for j, c in enumerate(seq): M.add('keys', t0 + S(s) + j * .012, lp(ks(mtof(c + 12), st * 3.5, .55, .995), 5000) * .16 * v, pan=-.2)
@K('nightcore')
def _(M, t0, st, S, T, r, v):            # trance-style gated supersaw chords on every 16th
    for k in range(16):
        if k % 4 != 3:
            for c in T[:3]: supersaw(M, 'keys', t0 + S(k), c + 12, st * .7, .04 * v, cut=5000, a=.002, r=.02, voices=5)
@K('glitchheavy')
def _(M, t0, st, S, T, r, v):
    glitch(M, t0, st, T, v)
    for s in (4, 12): stutter(M, t0 + S(s), T[-1] + 24, st, v)
@K('dark')
def _(M, t0, st, S, T, r, v):            # dark pad + bell (phonk / lava)
    for c in T[:3]: supersaw(M, 'pad', t0, c, 16 * st, .05 * v, cut=900, a=.4, r=.5, voices=3, detune=.2)
@K('choir')
def _(M, t0, st, S, T, r, v):
    for c in T[:3]: choir(M, t0, c + 12, 16 * st * .97, .5 * v)
@K('sleigh')
def _(M, t0, st, S, T, r, v):
    for k in range(0, 16, 2): sleigh(M, t0 + S(k), .8 * v)

# ======================= drum styles =======================
def D(name):
    def deco(f): EXTRA_DRUMS[name] = f; return f
    return deco
def _fill(M, t0, st, S, i, n, fill):
    if fill and i == n - 1:
        for s, nn in zip(range(12, 16), (52, 48, 45, 41)): tom(M, t0 + S(s), nn, .45)
@D('mario')
def _(M, t0, st, S, i, n, fill):         # light, bouncy kit with bongos
    for s in (0, 6, 8): kick(M, t0 + S(s), .7)
    for s in (4, 12): snare(M, t0 + S(s), .55)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .22)
    for s, h in ((2, True), (3, True), (7, False), (10, True), (11, True), (15, False)): bongo(M, t0 + S(s), h, .7)
    _fill(M, t0, st, S, i, n, fill)
@D('calypso')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 6, 8, 14): kick(M, t0 + S(s), .65)
    for s in (4, 12): rim(M, t0 + S(s), 1.)
    for s, nn in ((2, 55), (3, 55), (7, 50), (10, 55), (11, 55), (15, 50)): conga(M, t0 + S(s), nn, .8)
    for k in range(16): shaker(M, t0 + S(k), .4 if k % 2 else .25)
@D('darbuka')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 6, 8): darbuka(M, t0 + S(s), 'doum', 1.)
    for s in (3, 4, 10, 12, 14): darbuka(M, t0 + S(s), 'tek', .9)
    for s in (5, 13, 15): darbuka(M, t0 + S(s), 'tek', .4)
    for s in (0, 8): kick(M, t0 + S(s), .45)
@D('onedrop')
def _(M, t0, st, S, i, n, fill):
    kick(M, t0 + S(8), .8); rim(M, t0 + S(8), 1.2)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .25 if k % 4 == 0 else .15)
    if i % 4 == 3:
        for s in (12, 13, 14, 15): snare(M, t0 + S(s), .3)
@D('ska')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 8): kick(M, t0 + S(s), .85)
    for s in (4, 12): snare(M, t0 + S(s), .8)
    for k in range(8): hat(M, t0 + S(2 * k), .35 if k % 2 else .2, open_=bool(k % 2))
    _fill(M, t0, st, S, i, n, fill)
@D('brush')
def _(M, t0, st, S, i, n, fill):         # bluegrass / ghost-house brushes
    for s in (0, 8): kick(M, t0 + S(s), .45, punch=.6)
    for k in range(16): M.add('drums', t0 + S(k), bp(noise(int(.08 * SR)), 2000, 7000) * np.exp(-tarr(int(.08 * SR)) / .03) * (.12 if k % 4 in (0,) else .06), pan=.2)
    for s in (4, 12): snare(M, t0 + S(s), .3)
@D('gated')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 8, 10): kick(M, t0 + S(s), .85)
    for s in (4, 12): gated_snare(M, t0 + S(s), .85)
    for k in range(16): hat(M, t0 + S(k), .2 if k % 2 == 0 else .1)
    _fill(M, t0, st, S, i, n, fill)
@D('dubstep')
def _(M, t0, st, S, i, n, fill):
    kick(M, t0, 1., punch=1.4); kick(M, t0 + S(10), .7, punch=1.3)
    snare(M, t0 + S(8), 1.); clap(M, t0 + S(8), .7)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .25)
    if i % 4 == 3:
        for j in range(8): snare(M, t0 + S(12) + j * st / 2, .2 + .06 * j)
@D('eurobeat')
def _(M, t0, st, S, i, n, fill):
    for k in range(4): kick(M, t0 + S(4 * k), .95)
    for s in (4, 12): clap(M, t0 + S(s), .7); snare(M, t0 + S(s), .4)
    for k in range(4): hat(M, t0 + S(4 * k + 2), .45, open_=True)
    for k in range(16): hat(M, t0 + S(k), .12)
@D('amapiano')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 4, 8, 12): kick(M, t0 + S(s), .55, punch=.7)
    for s in (6, 14): clap(M, t0 + S(s), .45)
    for k in range(16): shaker(M, t0 + S(k), .5 if k % 2 else .3)
    for s in (3, 7, 11): woodblock(M, t0 + S(s), s != 7, .6)
@D('jersey')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 4, 7, 10, 12, 14): kick(M, t0 + S(s), .9 if s in (0, 7) else .7, punch=1.2)
    for s in (4, 12): clap(M, t0 + S(s), .65)
    for s in (6, 15): squeak(M, t0 + S(s), .9)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .2)
@D('phonk')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 8): kick(M, t0 + S(s), .9, punch=1.3)
    for s in (4, 12): clap(M, t0 + S(s), .75); snare(M, t0 + S(s), .4)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .25)
    if i % 2 == 1:
        for j in range(6): hat(M, t0 + S(12) + j * st * 2 / 3, .2)
    if i % 4 == 0: ayy(M, t0 + S(14), .7)
@D('dnb')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 10): kick(M, t0 + S(s), .9, punch=1.2)
    for s in (4, 12): snare(M, t0 + S(s), .9)
    for s in (7, 15): snare(M, t0 + S(s), .18)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .3); hat(M, t0 + S(k + 1), .12)
@D('castle')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 6, 8): timpani(M, t0 + S(s), 38 if s != 6 else 33, .6)
    for s in (4, 12): snare(M, t0 + S(s), .7)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .15)
    kick(M, t0, .6)
    if i % 4 == 0: cymbal(M, t0, .4)
@D('hyper')
def _(M, t0, st, S, i, n, fill):         # bouncy hyperpop kit with clanks
    for s in (0, 6, 10): kick(M, t0 + S(s), .9, punch=1.4)
    for s in (4, 12): snare(M, t0 + S(s), .8); clap(M, t0 + S(s), .6)
    for k in range(16): hat(M, t0 + S(k), .25 if k % 2 == 0 else .12)
    for s in (3, 11): clank(M, t0 + S(s), .8)
    if i % 2 == 1:
        for j in range(8): snare(M, t0 + S(14) + j * st / 4, .12 + .04 * j)
@D('swing')
def _(M, t0, st, S, i, n, fill):
    for k in range(4): ride(M, t0 + S(4 * k), .45); ride(M, t0 + S(4 * k) + 2.67 * st, .3)
    for s in (4, 12): hat(M, t0 + S(s), .3)
    kick(M, t0, .35, punch=.6)

# ======================= bass styles =======================
def Bs(name):
    def deco(f): EXTRA_BASS[name] = f; return f
    return deco
def _r(root): return root if root < 44 else root - 12
@Bs('tuba')
def _(M, t0, st, S, root):
    r = _r(root)
    for s, o in ((0, 0), (8, 7)): tuba(M, t0 + S(s), r + 12 + o, st * 3, .9)
@Bs('slap')
def _(M, t0, st, S, root):
    r = _r(root)
    for s, o, L in ((0, 0, 2), (3, 12, 1), (4, 0, 1), (6, 12, 1), (8, 0, 2), (10, 7, 1), (11, 12, 1), (14, 10, 2)): fbass(M, t0 + S(s), r + o, L * st * .8, .65)
@Bs('wobble')
def _(M, t0, st, S, root):
    r = _r(root) + 12; spb = 4 * st
    for s, L, rate in ((0, 6, 2 / spb), (6, 2, 4 / spb), (8, 4, 1 / spb), (12, 4, 3 / spb)): wobble(M, t0 + S(s), r, L * st * .97, .9, rate)
@Bs('logdrum')
def _(M, t0, st, S, root):
    r = _r(root) + 12
    for s, o in ((0, 0), (3, 0), (6, 7), (10, 0), (11, 12), (14, 7)): logdrum(M, t0 + S(s), r + o, st * 2, .8)
@Bs('reggae')
def _(M, t0, st, S, root):
    r = _r(root)
    for s, o, L in ((0, 0, 3), (4, 7, 2), (6, 12, 1), (8, 0, 3), (12, 10, 2), (14, 7, 2)): fbass(M, t0 + S(s), r + o, L * st * .9, .7)
@Bs('phonk808')
def _(M, t0, st, S, root):
    r = _r(root)
    for s, L in ((0, 6), (8, 4), (12, 4)): heavy808(M, t0 + S(s), r, L * st * .95, .65)
@Bs('upright')
def _(M, t0, st, S, root):
    r = _r(root)
    for s, o in ((0, 0), (8, 7)): fbass(M, t0 + S(s), r + o, st * 3, .6)
@Bs('synthwave')
def _(M, t0, st, S, root):
    r = _r(root)
    for k in range(16): bass(M, 'bass', t0 + S(k), r + (12 if k % 2 else 0), st * .85, .45, cut=900)

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d
def bah_at(steps, n=60, every=2, vol=1.):   # a per-bar extra that shouts 'bah' on the given steps
    def f(M, t0, st, S, i, nb, tones, root):
        if i % every == every - 1:
            for s in steps: bah(M, t0 + S(s), tones[-1] + 12 if n is None else n, vol)
    return f
def chain(*fs):
    def f(*a):
        for g in fs:
            if g: g(*a)
    return f
