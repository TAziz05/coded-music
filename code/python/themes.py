"""Themed songs: landforms and bodies of water, the Frutiger aesthetics, the planets (tempo from each planet's real orbit),
kinds of space things, film/event-inspired pieces (original music in the style only), JVKE-style piano pop, a
PRETTY4U-style hyperpop track, and DNA Breakcore Squared. All sounds are code.
Every song has its own shape: how it starts, how its parts are ordered, and how it ends.
python themes.py all  (or keys from SONGS, or a group: geo, frutiger, planets, space, film, pop)"""
import sys, re
import numpy as np
from newstyles import *
from popkit import build, LEADS
from songs5 import harp

R = -1
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
MODES = {'major': [0, 2, 4, 5, 7, 9, 11], 'minor': [0, 2, 3, 5, 7, 8, 10], 'dorian': [0, 2, 3, 5, 7, 9, 10], 'lydian': [0, 2, 4, 6, 7, 9, 11],
         'phrygdom': [0, 1, 4, 5, 7, 8, 10], 'mixo': [0, 2, 4, 5, 7, 9, 10], 'penta': [0, 2, 4, 7, 9], 'mpenta': [0, 3, 5, 7, 10]}
EVEN = {'intro': -16., 'verse': -14., 'pre': -14., 'chorus': -13.5, 'drop': -13.5, 'bridge': -14.5, 'break': -14.5, 'outro': -15.}
QUAL = {'m': [0, 3, 7], '': [0, 4, 7], 'dim': [0, 3, 6], 'sus2': [0, 2, 7], 'sus4': [0, 5, 7], '7': [0, 4, 7, 10], 'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10]}
def chord_pcs(c):
    m = re.match(r'([A-G][b#]?)(.*)', c); r = NAMES.index({'Db': 'C#', 'D#': 'Eb', 'Gb': 'F#', 'G#': 'Ab', 'A#': 'Bb'}.get(m.group(1), m.group(1)))
    return [(r + i) % 12 for i in QUAL.get(m.group(2), [0, 4, 7])]

def phrase(chords, key, mode, seed, lo=67, hi=84, rhythm=None, contour='wave'):
    """A 4-bar melody: bar 1 is a motif, bar 2 answers it, bar 3 repeats the motif moved to fit its chord, bar 4 lands on a long chord note."""
    rng = np.random.default_rng(seed); sc = MODES[mode]
    pool = [n for n in range(lo, hi + 1) if (n - key) % 12 in sc]
    RH = [[1, 0, 1, 0, 1, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0, 0], [1, 0, 0, 1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 1, 1, 0]]
    rh = rhythm or RH[rng.integers(len(RH))]
    steps = {'wave': [0, 1, 2, 1, -1, 0, 1, 2], 'rise': [0, 1, 1, 2, 2, 3, 3, 4], 'fall': [0, -1, -1, -2, -2, -3, -3, -4], 'leap': [0, 3, 2, 1, 4, 3, 2, 0]}[contour]
    def near(pcs, x): return min((n for n in pool if n % 12 in pcs), key=lambda n: abs(n - x))
    rows, mid = [], (lo + hi) // 2
    start = near(chord_pcs(chords[0]), mid - 2)
    def bar(ch, base, var):
        out, k = [], 0
        for j, on in enumerate(rh):
            if not on: out.append(R if out and out[-1] != 0 else 0); continue
            i = pool.index(near(chord_pcs(ch), base))
            d = steps[k % len(steps)] + (var if j > 3 else 0); k += 1
            n = pool[int(np.clip(i + d, 0, len(pool) - 1))]
            if j in (0, 4) and n % 12 not in chord_pcs(ch): n = near(chord_pcs(ch), n)
            out.append(n)
        return out
    rows.append(bar(chords[0], start, 0))
    rows.append(bar(chords[1 % len(chords)], start + 2, int(rng.integers(-2, 3))))
    rows.append(bar(chords[2 % len(chords)], start + (3 if contour != 'fall' else -3), 0))
    end = near(chord_pcs(chords[3 % len(chords)]), start)
    rows.append([n if n else 0 for n in bar(chords[3 % len(chords)], start, 0)[:2]] + [end, R, R, R, 0, 0])
    return rows

def chain(*fs):
    def f(*a):
        for g in fs:
            if g: g(*a)
    return f
# ---------------- sound effects ----------------
def waves(vol=.5, every=2):
    def f(M, t0, st, S, i, n, T, r):
        if i % every: return
        N = int(every * 16 * st * SR); tt = tarr(N); sw = np.sin(np.pi * tt / tt[-1]) ** 2
        M.add('fx', t0, lp(noise(N), 400 + 1400 * sw) * sw * vol * .18)
    return f
def bubbles(vol=.5, k=5):
    def f(M, t0, st, S, i, n, T, r):
        rng = np.random.default_rng(i)
        for _ in range(k):
            t = t0 + rng.uniform(0, 16 * st); N = int(.08 * SR); tt = tarr(N); fr = rng.uniform(600, 1400) * (1 + 3 * tt / .08)
            M.add('fx', t, np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / .025) * vol * .2, pan=rng.uniform(-.6, .6))
    return f
def birds(vol=.5):
    def f(M, t0, st, S, i, n, T, r):
        if i % 2: return
        rng = np.random.default_rng(i + 7)
        for _ in range(3):
            t = t0 + rng.uniform(0, 16 * st); N = int(.12 * SR); tt = tarr(N); fr = 2800 + 1500 * np.sin(2 * np.pi * 18 * tt)
            M.add('fx', t, np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * tt / .12) * vol * .08, pan=rng.uniform(-.7, .7))
    return f
def rumble(vol=.5, every=4):
    def f(M, t0, st, S, i, n, T, r):
        if i % every: return
        N = int(every * 16 * st * SR); tt = tarr(N); M.add('fx', t0, lp(noise(N), 120) * np.sin(np.pi * tt / tt[-1]) * vol * 1.2)
    return f
def wind(vol=.5):
    def f(M, t0, st, S, i, n, T, r):
        if i % 4: return
        N = int(64 * st * SR); tt = tarr(N); c = 600 + 500 * np.sin(2 * np.pi * tt / (16 * st))
        M.add('fx', t0, bp(noise(N), 300, 1800) * (.5 + .5 * np.sin(np.pi * tt / tt[-1])) * vol * .12)
    return f
def pings(note=84, every=2, vol=.5):   # sonar / radio pings
    def f(M, t0, st, S, i, n, T, r):
        if i % every == 0: celesta(M, 'glock', t0, note, 2.5, vol); celesta(M, 'glock', t0 + 12 * st, note, 1.5, vol * .3)
    return f
def ticks(period, vol=.5):   # a clock tick every `period` seconds, all song long
    def f(M, t0, st, S, i, n, T, r):
        t = np.ceil(t0 / period) * period
        while t < t0 + 16 * st:
            N = int(.03 * SR); M.add('fx', t, hp(noise(N), 3000) * np.exp(-tarr(N) / .006) * vol * .5); t += period
    return f
def bells_roll(notes, vol=.45):   # cascading bells, like falling water
    def f(M, t0, st, S, i, n, T, r):
        for k, nn in enumerate(notes): celesta(M, 'glock', t0 + S(k), nn, 1., vol * (1 - k / len(notes) * .5))
    return f
def strum_circle(vol=.5):   # harp arpeggios that go round and round (rings)
    def f(M, t0, st, S, i, n, T, r):
        cyc = T[:3] + [T[0] + 12] + T[:3][::-1]
        for k in range(16): harp(M, t0 + S(k), cyc[k % len(cyc)] + 24, vol * .5)
    return f
def triplet_arp(vol=.55, inst='piano', up=12):   # JVKE-style: fast rolling piano arpeggios in triplets
    def f(M, t0, st, S, i, n, T, r):
        cyc = [T[0], T[1], T[2], T[0] + 12, T[2], T[1]]
        for k in range(24): LEADS[inst](M, t0 + k * 16 * st / 24, cyc[k % 6] + up, 16 * st / 24 * 1.5, vol * (.8 + .2 * (k % 6 == 0)))
    return f
def woodblocks(layers):   # Time-Go-Fishing-style finger taps: patterns that add up section by section
    PAT = [[0, 6, 10], [3, 8, 12, 14], [2, 5, 9, 13], list(range(0, 16, 2))]
    def f(M, t0, st, S, i, n, T, r):
        for L in range(layers):
            for s in PAT[L]: woodblock(M, t0 + S(s), L % 2 == 0, .35 + .05 * L)
    return f
def organ_swell(vol=.5):
    def f(M, t0, st, S, i, n, T, r):
        if i % 2 == 0:
            for c in T[:3] + [T[0] - 12]: LEADS['organ'](M, t0, c + 12, 32 * st, vol * .35)
    return f

# ---------------- endings ----------------
def end_ring(M, t0, st, S, i, n, T, r):
    if i: return
    for c in T[:3]: supersaw(M, 'pad', t0, c + 12, 3., .04, cut=2400, a=.05, r=2.5, voices=3)
    celesta(M, 'glock', t0, T[0] + 24, 3., .7)
def end_hit(M, t0, st, S, i, n, T, r):
    if i: return
    kick(M, t0, .8); crash(M, t0, .4)
    for c in T[:3]: LEADS['piano'](M, t0, c + 12, 1.5, .6)
def end_sink(M, t0, st, S, i, n, T, r):   # everything drops in pitch and slows into the deep
    if i: return
    N = int(4 * SR); tt = tarr(N); f = 220 * np.exp(-tt * 1.2)
    M.add('pad', t0, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 1.5) * .35)
def end_collapse(M, t0, st, S, i, n, T, r):   # black hole / The End: a low hum that sucks everything in, then silence
    if i: return
    N = int(6 * SR); tt = tarr(N); hum = (np.sin(2 * np.pi * 55 * tt) + .5 * np.sin(2 * np.pi * 82.5 * tt)) * np.minimum(1, tt / .5) * np.exp(-tt / 2.5)
    M.add('pad', t0, hum * .4)
def end_bang(M, t0, st, S, i, n, T, r):   # supernova: one huge hit that rings and spreads out
    if i: return
    impact(M, t0, .7); kick(M, t0, 1.)
    for c in T[:3] + [T[0] + 12, T[0] + 24]: supersaw(M, 'pad', t0, c + 12, 5., .035, cut=4000, a=.005, r=4., voices=5)

ENDS = {'ring': (end_ring, {}), 'hit': (end_hit, {}), 'sink': (end_sink, {}), 'collapse': (end_collapse, {}), 'bang': (end_bang, {}),
        'echo': (None, {'echo_out': (8, .55, 7)}), 'fade': (None, {'fadeout': 8.}), 'tapestop': (None, {'tapestop': True})}

def theme(file, title, bpm, key, mode, A, B, keys, lead, drums, bass, seed, shape='AB AB', start='keys', end='ring', fx=None, fxB=None,
          leadB=None, keysB=None, drumsB=None, contour='wave', contourB='rise', lo=67, hi=84, lv=1., swing=0., C=None, crush=None, **kw):
    melA = phrase(A, key, mode, seed, lo, hi, contour=contour) + phrase(A, key, mode, seed + 1, lo, hi, contour=contour)
    melB = phrase(B, key, mode, seed + 2, lo + 5, hi + 5, contour=contourB) + phrase(B, key, mode, seed + 3, lo + 5, hi + 5, contour=contourB)
    s = {'A': sec(8, A, keys=keys, drums=drums, bass=bass, lead=lead, mel=melA, lv=lv, extra=fx, kind='verse'),
         'B': sec(8, B, keys=keysB or keys, drums=drumsB or drums, bass=bass, lead=leadB or lead, mel=melB, lv=lv, extra=fxB or fx, impact=True, kind='chorus'),
         'C': sec(4, C or B[::-1], keys=(keysB or keys)[-1:], lead=lead, mel=melA[:4], lv=lv, extra=fx, kind='bridge'),
         'D': sec(4, A, keys=keys, drums=drums, bass=bass, extra=fx, kind='verse')}   # a groove-only part
    order = shape.replace(' ', '')
    order = [c for c in order]
    intro = {'keys': sec(4, A, keys=keys, extra=fx), 'beat': sec(2, A, drums=drums, extra=fx), 'melody': sec(4, A, keys=keys[-1:], lead=lead, mel=melA[:4], lv=lv, extra=fx),
             'swell': sec(4, A, keys=keys[-1:], extra=chain(fx, lambda M, t0, st, S, i, n, T, r: i == 0 and riser(M, t0, 64 * st, .25))), 'cold': None}[start]
    if intro: s['intro'] = intro; order = ['intro'] + order
    cfg = dict(file=file, title=title, bpm=bpm, swing=swing, sections=s, order=order, chorus_keys=True, cont_tol=3., targets=EVEN, ride=1., ride_max=5., verb=2.6)
    fn, extra = ENDS[end]
    if fn: s['end'] = sec(2, [A[0]], extra=fn, fill=False, kind='outro'); order.append('end')
    cfg.update(extra); cfg.update(kw)
    if crush: cfg['crush'] = crush
    return cfg

SONGS = {}
def add(group, key, cfg): cfg['group'] = group; SONGS[key] = cfg

# ================= landforms and bodies of water =================
add('geo', 'mountain', theme('Mountain', 'Mountain', 96, 2, 'major', ['D', 'G', 'Bm', 'A'], ['G', 'A', 'D', 'D'], ['acoustic', 'pad'], 'horn', 'halfpop', 'long', 11,
    shape='A B A B', start='keys', end='ring', contour='rise', contourB='rise', fx=wind(.4), C=None))   # the melody keeps climbing, like a trail to the peak
add('geo', 'volcano', theme('Volcano', 'Volcano', 140, 4, 'phrygdom', ['Em', 'F', 'Em', 'Dm'], ['Em', 'F', 'G', 'F'], ['dark', 'pad'], 'saw80s', 'halfpop', 'heavy808', 21,
    shape='D A B C B', start='swell', end='bang', fx=rumble(.6), drumsB='dubstep', keysB=['glitchheavy'], contour='rise'))   # rumbles, builds, erupts
add('geo', 'canyon', theme('Canyon', 'Canyon', 88, 9, 'dorian', ['Am', 'G', 'D', 'Am'], ['F', 'G', 'Am', 'Am'], ['nylon', 'pad'], 'guitar', 'brush', 'long', 31,
    shape='A B C A', start='melody', end='echo', fx=None, swing=.08))   # big echoes off the walls
add('geo', 'desert', theme('Desert', 'Desert', 104, 4, 'phrygdom', ['E', 'F', 'E', 'Dm'], ['Am', 'F', 'E', 'E'], ['oud', 'pad'], 'oud', 'darbuka', 'long', 41,
    shape='A B A B', start='beat', end='fade', fx=wind(.5), contour='leap'))
add('geo', 'glacier', theme('Glacier', 'Glacier', 70, 11, 'lydian', ['B', 'C#m', 'B', 'F#'], ['E', 'F#', 'B', 'B'], ['celesta', 'pad'], 'fmbell', 'lofi', 'sub', 51,
    shape='A C B', start='swell', end='ring', contour='fall', lo=72, hi=88))   # slow, crystal-clear, a little cracking ice in the drums
add('geo', 'island', theme('Island', 'Island', 112, 7, 'major', ['G', 'C', 'D', 'G'], ['C', 'D', 'Em', 'D'], ['steelcomp', 'uke'], 'marimba', 'calypso', 'finger', 61,
    shape='A B A B', start='beat', end='hit', fx=waves(.35)))
add('geo', 'ocean', theme('Ocean', 'Ocean', 80, 2, 'major', ['D', 'Bm', 'G', 'A'], ['G', 'A', 'Bm', 'G'], ['pad', 'pianoriff'], 'strings', 'lofi', 'long', 71,
    shape='A B C B', start='swell', end='fade', fx=waves(.6), contour='wave'))
add('geo', 'river', theme('River', 'River', 118, 5, 'major', ['F', 'Dm', 'Bb', 'C'], ['Bb', 'C', 'Am', 'Dm'], ['pizzarp', 'pad'], 'flute', 'halfpop', 'octave', 81,
    shape='A B D B', start='keys', end='echo', lv=.75, contour='wave', fx=waves(.25, 1)))   # keeps flowing: arpeggios that never stop
add('geo', 'lake', theme('Lake', 'Lake', 76, 0, 'major', ['C', 'Am', 'F', 'G'], ['F', 'G', 'Em', 'Am'], ['ep', 'pad'], 'celesta', 'brush', 'long', 91,
    shape='A C A', start='keys', end='ring', contour='fall'))
add('geo', 'waterfall', theme('Waterfall', 'Waterfall', 126, 9, 'major', ['A', 'E', 'F#m', 'D'], ['D', 'E', 'C#m', 'F#m'], ['pluck', 'pad'], 'sqbright', 'fourfloor', 'octave', 101,
    shape='A B A B', start='cold', end='tapestop', contour='fall', fxB=bells_roll([93, 90, 88, 85, 81, 78, 76, 73], .35), lv=.8))   # falling bell runs
add('geo', 'reef', theme('Coral_Reef', 'Coral Reef', 108, 4, 'major', ['E', 'C#m', 'A', 'B'], ['A', 'B', 'G#m', 'C#m'], ['marimbaarp', 'pad'], 'xylo', 'dembow', 'sub', 111,
    shape='A B C B', start='melody', end='hit', fx=bubbles(.6)))
add('geo', 'trench', theme('Deep_Trench', 'Deep Trench', 78, 1, 'minor', ['C#m', 'A', 'F#m', 'G#'], ['A', 'G#', 'C#m', 'C#m'], ['dark', 'pad'], 'theremin', 'lofi', 'sub', 121,
    shape='A B A', start='swell', end='sink', fx=pings(73, 2, .4), contour='fall', lo=55, hi=72))   # sinks lower and lower, sonar pings

# ================= the Frutiger family =================
add('frutiger', 'aero', theme('Frutiger_Aero', 'Frutiger Aero', 120, 4, 'major', ['E', 'B', 'C#m', 'A'], ['A', 'B', 'G#m', 'C#m'], ['pianoriff', 'pad'], 'plastic', 'house', 'octave', 201,
    shape='A B A B', start='keys', end='ring', fx=bubbles(.35, 3)))   # glossy, bubbly, sky blue
add('frutiger', 'eco', theme('Frutiger_Eco', 'Frutiger Eco', 104, 7, 'major', ['G', 'D', 'Em', 'C'], ['C', 'D', 'G', 'G'], ['uke', 'pad'], 'flute', 'halfpop', 'finger', 211,
    shape='A B C B', start='melody', end='fade', fx=birds(.6), lv=.75))   # nature and clean energy
add('frutiger', 'metro', theme('Frutiger_Metro', 'Frutiger Metro', 128, 9, 'dorian', ['Am', 'D', 'Am', 'G'], ['F', 'G', 'Am', 'Am'], ['stabs', 'pad'], 'synth', 'boombap', 'funky', 221,
    shape='D A B A B', start='beat', end='hit', swing=.06))   # city, boomboxes, bold shapes
add('frutiger', 'aqua', theme('Helvetica_Aqua', 'Helvetica Aqua', 90, 2, 'lydian', ['D', 'E', 'D', 'A'], ['G', 'A', 'Bm', 'A'], ['ep', 'pad'], 'celesta', 'lofi', 'long', 231,
    shape='A C B', start='swell', end='echo', fx=bubbles(.6)))   # underwater, sea life
add('frutiger', 'aurora', theme('Frutiger_Aurora', 'Frutiger Aurora', 136, 6, 'major', ['F#', 'C#', 'D#m', 'B'], ['B', 'C#', 'A#m', 'D#m'], ['futurebass', 'pad'], 'saw80s', 'fourfloor', 'octave', 241,
    shape='A B C B', start='swell', end='ring', lv=.8))   # flowing light streaks
add('frutiger', 'darkaero', theme('Dark_Aero', 'Dark Aero', 110, 2, 'minor', ['Dm', 'Bb', 'Gm', 'A'], ['Bb', 'C', 'Dm', 'Dm'], ['ep', 'dark'], 'fmbell', 'halfpop', 'sub', 251,
    shape='A B A B', start='keys', end='fade'))   # glassy, deep blue and black
add('frutiger', 'floral', theme('Floral_Metro', 'Floral Metro', 116, 5, 'major', ['F', 'C', 'Dm', 'Bb'], ['Bb', 'C', 'Am', 'Dm'], ['harpsi', 'pad'], 'strings', 'house', 'octave', 261,
    shape='A B C B', start='melody', end='hit', fxB=strum_circle(.5)))   # swirly vector flowers
add('frutiger', 'technozen', theme('Technozen', 'Technozen', 84, 0, 'penta', ['C', 'Am', 'F', 'G'], ['F', 'G', 'C', 'C'], ['celesta', 'pad'], 'fmbell', 'brush', 'long', 271,
    shape='A C A', start='keys', end='ring'))   # calm, minimal, zen tech

# ================= the planets: tempo from each planet's real orbit (faster orbit = faster song) =================
ORBIT = {'Mercury': 88, 'Venus': 224.7, 'Earth': 365.25, 'Mars': 687, 'Jupiter': 4333, 'Saturn': 10759, 'Uranus': 30687, 'Neptune': 60190}
def orbit_bpm(p): return int(round(172 - (np.log10(ORBIT[p]) - np.log10(88)) / (np.log10(60190) - np.log10(88)) * 104))
def reverse_rows(rows): return [r[::-1] for r in rows[::-1]]
add('planets', 'mercury', theme('Mercury', 'Mercury', orbit_bpm('Mercury'), 9, 'minor', ['Am', 'F', 'C', 'G'], ['F', 'G', 'Am', 'Am'], ['pluck', 'pad'], 'sqbright', 'dnb', 'reese', 301,
    shape='A B C A B B', start='cold', end='echo', lv=.75))   # closest to the sun, fastest orbit
VEN = theme('Venus', 'Venus', orbit_bpm('Venus'), 3, 'phrygdom', ['Eb', 'E', 'Eb', 'Db'], ['E', 'Eb', 'Db', 'Eb'], ['darkgtr', 'pad'], 'crunch', 'metal', 'metalbass', 311,
    shape='A B C B', start='swell', end='tapestop', fx=rumble(.5))
for k in ('A', 'B'): VEN['sections'][k]['mel'] = reverse_rows(VEN['sections'][k]['mel'])   # Venus spins backwards, so its melodies play backwards
add('planets', 'venus', VEN)
add('planets', 'earth', theme('Earth', 'Earth', orbit_bpm('Earth'), 7, 'major', ['G', 'Em', 'C', 'D'], ['C', 'D', 'G', 'G'], ['acoustic', 'pad'], 'whistle', 'halfpop', 'finger', 321,
    shape='A B C B', start='keys', end='ring', fx=chain(birds(.5), waves(.3))))
add('planets', 'mars', theme('Mars', 'Mars', orbit_bpm('Mars'), 4, 'minor', ['Em', 'C', 'D', 'B'], ['C', 'D', 'Em', 'Em'], ['dark', 'pad'], 'brass', 'march', 'long', 331,
    shape='D A B A B', start='beat', end='hit', fx=wind(.5)))
add('planets', 'jupiter', theme('Jupiter', 'Jupiter', orbit_bpm('Jupiter'), 10, 'major', ['Bb', 'Eb', 'F', 'Bb'], ['Eb', 'F', 'Gm', 'F'], ['strings', 'horns'], 'brass2', 'rock', 'octave', 341,
    shape='A B C B', start='swell', end='bang', fxB=lambda M, t0, st, S, i, n, T, r: i == 0 and riser(M, t0, 128 * st, .2)))   # the biggest planet, big brass; a storm swirls in the chorus
add('planets', 'saturn', theme('Saturn', 'Saturn', orbit_bpm('Saturn'), 8, 'lydian', ['Ab', 'Bb', 'Ab', 'Eb'], ['Db', 'Eb', 'Fm', 'Eb'], ['pad'], 'celesta', 'lofi', 'long', 351,
    shape='A B A', start='keys', end='ring', fx=strum_circle(.45)))   # rings: harp arpeggios going round and round
URA = theme('Uranus', 'Uranus', orbit_bpm('Uranus'), 11, 'dorian', ['Bm', 'E', 'Bm', 'A'], ['G', 'A', 'Bm', 'Bm'], ['fm', 'pad'], 'theremin', 'swing', 'walking', 361,
    shape='A C B', start='melody', end='fade')
for k in ('A', 'B'): URA['sections'][k]['mel'] = [r[1:] + r[:1] for r in URA['sections'][k]['mel']]   # tipped on its side: every melody is knocked one step off the beat
add('planets', 'uranus', URA)
add('planets', 'neptune', theme('Neptune', 'Neptune', orbit_bpm('Neptune'), 2, 'minor', ['Dm', 'Bb', 'F', 'C'], ['Bb', 'C', 'Dm', 'Dm'], ['pad', 'choir'], 'voice', 'lofi', 'sub', 371,
    shape='A B C B', start='swell', end='fade', fx=wind(.8), lo=62, hi=78))   # the windiest planet, far and deep blue

# ================= space =================
add('space', 'blackhole', theme('Black_Hole', 'Black Hole', 92, 1, 'minor', ['C#m', 'A', 'B', 'G#'], ['A', 'B', 'C#m', 'C#m'], ['dark', 'pad'], 'theremin', 'halfpop', 'heavy808', 401,
    shape='A B A', start='swell', end='collapse', contour='fall'))   # falls in at the end: a low hum, then nothing
add('space', 'nebula', theme('Nebula', 'Nebula', 74, 6, 'lydian', ['F#', 'G#', 'F#', 'C#'], ['B', 'C#', 'D#m', 'C#'], ['pad', 'choir'], 'fmbell', 'lofi', 'long', 411,
    shape='A C B', start='swell', end='fade'))
add('space', 'supernova', theme('Supernova', 'Supernova', 150, 9, 'minor', ['Am', 'F', 'C', 'G'], ['F', 'G', 'Am', 'Am'], ['futurebass', 'pad'], 'saw80s', 'trap', '808', 421,
    shape='A B C B', start='keys', end='bang', lv=.8, fxB=None))   # a star builds, collapses (the quiet part) and explodes
add('space', 'pulsar', theme('Pulsar', 'Pulsar', 84, 7, 'minor', ['Gm', 'Eb', 'Bb', 'F'], ['Eb', 'F', 'Gm', 'Gm'], ['pluck', 'pad'], 'fm', 'fourfloor', 'octave', 431,
    shape='D A B A', start='beat', end='echo', fx=ticks(0.7145, .7)))   # the beat is a real pulsar: PSR B0329+54 spins every 0.7145 s = 84 BPM
add('space', 'comet', theme('Comet', 'Comet', 168, 4, 'major', ['E', 'C#m', 'A', 'B'], ['A', 'B', 'C#m', 'B'], ['eurobeat', 'pad'], 'sqbright', 'eurobeat', 'octave', 441,
    shape='A B A C B B', start='cold', end='echo', lv=.75))   # a fast streak and a long tail
add('space', 'station', theme('Space_Station', 'Space Station', 112, 0, 'dorian', ['Cm', 'F', 'Cm', 'Bb'], ['Ab', 'Bb', 'Cm', 'Cm'], ['glitch', 'pad'], 'gb', 'breakbeat', 'synth8', 451,
    shape='D A B C B', start='beat', end='hit', fx=pings(96, 4, .3)))
add('space', 'aurora', theme('Aurora', 'Aurora', 98, 11, 'major', ['B', 'G#m', 'E', 'F#'], ['E', 'F#', 'D#m', 'G#m'], ['pad', 'celesta'], 'voice', 'halfpop', 'long', 461,
    shape='A B A B', start='melody', end='ring'))

# ================= film / event inspired (original music, only the general style) =================
# "Time Go Fishing" style: starts with fingertip woodblock taps; each part adds a layer until a full, bold climax
TGF = dict(file='Spacewalk_Taps', title='Spacewalk Taps', bpm=120, chorus_keys=True, cont_tol=3., targets=EVEN, ride=1., ride_max=4., verb=2.8, sections={
   't1': sec(4, ['Dm', 'Dm', 'Bb', 'C'], extra=woodblocks(1), kind='intro'),
   't2': sec(4, ['Dm', 'Dm', 'Bb', 'C'], keys=['pizzarp'], extra=woodblocks(2), kind='verse'),
   't3': sec(8, ['Dm', 'Bb', 'F', 'C'], keys=['pizzarp', 'strings'], bass='octave', extra=chain(woodblocks(3), lambda M, t0, st, S, i, n, T, r: [tom(M, t0 + S(s), 45, .5) for s in (0, 6, 10)]), kind='verse'),
   't4': sec(8, ['Dm', 'Bb', 'F', 'C'], keys=['strings', 'horns'], drums='march', bass='octave', lead='horn',
             mel=phrase(['Dm', 'Bb', 'F', 'C'], 2, 'dorian', 501, 64, 80, contour='rise') * 2, extra=woodblocks(4), impact=True, kind='chorus'),
   't5': sec(8, ['Bb', 'C', 'Dm', 'Dm'], keys=['strings', 'horns', 'choir'], drums='rock', bass='octave', lead='brass2+horn',
             mel=phrase(['Bb', 'C', 'Dm', 'Dm'], 2, 'dorian', 503, 69, 86, contour='rise') * 2, extra=woodblocks(4), impact=True, kind='chorus'),
   'end': sec(2, ['D'], extra=chain(woodblocks(1), end_ring), fill=False, kind='outro')},
   order=['t1', 't2', 't3', 't4', 't5', 'end'], group='film')
SONGS['tgf'] = TGF
# Fortnite Chapter 1 "The End"-style: an ominous countdown with choir and low strings, rockets and rifts, then the black hole
def rocket(M, t0, st, S, i, n, T, r):
    if i % 4 == 2: riser(M, t0, 32 * st, .3); M.add('fx', t0, lp(noise(int(2 * SR)), 300) * np.linspace(0, 1, int(2 * SR)) * .6)
END = dict(file='Last_Event', title='The Last Event', bpm=90, chorus_keys=True, cont_tol=3., targets=EVEN, ride=1., ride_max=4., verb=3., sections={
   'count': sec(4, ['Cm', 'Cm', 'Ab', 'G'], keys=['dark'], extra=ticks(60 / 90, .6), kind='intro'),
   'rise': sec(8, ['Cm', 'Ab', 'Fm', 'G'], keys=['strings', 'choir'], bass='long', lead='strings', mel=phrase(['Cm', 'Ab', 'Fm', 'G'], 0, 'minor', 601, 60, 76, contour='rise') * 2, extra=rocket, kind='verse'),
   'rift': sec(8, ['Ab', 'Bb', 'Cm', 'G'], keys=['strings', 'choir', 'churchorgan'], drums='march', bass='long', lead='brass+strings',
               mel=phrase(['Ab', 'Bb', 'Cm', 'G'], 0, 'minor', 603, 65, 82, contour='rise') * 2, extra=chain(rocket, lambda M, t0, st, S, i, n, T, r: i % 2 == 0 and impact(M, t0, .4)), impact=True, kind='chorus'),
   'void': sec(4, ['Cm'], extra=end_collapse, fill=False, kind='outro')},
   order=['count', 'rise', 'rift', 'void'], group='film')
SONGS['theend'] = END
# Interstellar-style: pipe organ, a ticking clock, rolling piano arpeggios, a docking-spin build
INT1 = dict(file='Tidal_Clock', title='Tidal Clock', bpm=96, chorus_keys=True, cont_tol=3., targets=EVEN, ride=1., ride_max=4., verb=3., sections={   # a tick every 1.25 s
   'a': sec(8, ['Am', 'Am', 'F', 'F'], keys=['churchorgan'], extra=ticks(1.25, .7), kind='intro'),
   'b': sec(8, ['Am', 'F', 'C', 'G'], keys=['churchorgan', 'strings'], bass='long', lead='organ', mel=phrase(['Am', 'F', 'C', 'G'], 9, 'minor', 701, 64, 79, contour='rise') * 2, extra=ticks(1.25, .7), kind='verse'),
   'c': sec(8, ['F', 'G', 'Am', 'Am'], keys=['churchorgan', 'strings', 'choir'], bass='long', lead='organ+strings', mel=phrase(['F', 'G', 'Am', 'Am'], 9, 'minor', 703, 69, 86, contour='rise') * 2, extra=ticks(1.25, .8), kind='chorus'),
   'end': sec(4, ['Am'], keys=['churchorgan'], extra=ticks(1.25, .7), kind='outro')},
   order=['a', 'b', 'c', 'end'], fadeout=5., group='film')
INT2 = dict(file='Cornfield_Drive', title='Cornfield Drive', bpm=126, chorus_keys=True, cont_tol=3., targets=EVEN, ride=1., ride_max=4., verb=2.8, sections={
   'a': sec(4, ['Am', 'Am', 'Em', 'Em'], extra=triplet_arp(.5, 'piano', 12), kind='intro'),
   'b': sec(8, ['Am', 'F', 'C', 'Em'], keys=['churchorgan'], bass='long', extra=triplet_arp(.5, 'piano', 12), kind='verse'),
   'c': sec(8, ['F', 'G', 'Am', 'Em'], keys=['churchorgan', 'strings'], drums='halfpop', bass='octave', lead='organ', mel=phrase(['F', 'G', 'Am', 'Em'], 9, 'minor', 711, 69, 84, contour='wave') * 2, extra=triplet_arp(.45, 'piano', 12), kind='chorus'),
   'end': sec(2, ['Am'], extra=end_ring, fill=False, kind='outro')},
   order=['a', 'b', 'c', 'b', 'c', 'end'], group='film')
INT3 = dict(file='Docking_Spin', title='Docking Spin', bpm=138, chorus_keys=True, cont_tol=3., targets=EVEN, ride=1., ride_max=4., verb=3., sections={
   'a': sec(4, ['Em', 'Em', 'C', 'C'], keys=['churchorgan'], kind='intro'),
   'b': sec(8, ['Em', 'C', 'G', 'D'], keys=['churchorgan', 'strings'], drums='march', bass='octave', extra=triplet_arp(.4, 'organ', 0), kind='verse'),
   'c': sec(8, ['C', 'D', 'Em', 'Em'], keys=['churchorgan', 'strings', 'choir'], drums='rock', bass='octave', lead='organ+brass', mel=phrase(['C', 'D', 'Em', 'Em'], 4, 'minor', 721, 67, 84, contour='rise') * 2,
             extra=chain(triplet_arp(.4, 'organ', 0), lambda M, t0, st, S, i, n, T, r: i == 0 and riser(M, t0, 128 * st, .2)), impact=True, kind='chorus')},
   order=['a', 'b', 'c', 'c'], echo_out=(8, .55, 7), group='film')
SONGS['tidal'] = INT1; SONGS['cornfield'] = INT2; SONGS['docking'] = INT3

# ================= JVKE-style piano pop, and a PRETTY4U-style hyperpop track =================
add('pop', 'jvke1', theme('Rolling_Hours', 'Rolling Hours', 94, 4, 'major', ['E', 'C#m', 'A', 'B'], ['A', 'B', 'G#m', 'C#m'], ['strings'], 'voice', 'halfpop', 'long', 801,
    shape='A B C B', start='melody', end='ring', fx=triplet_arp(.45, 'piano', 12), fxB=triplet_arp(.5, 'piano', 12)))
add('pop', 'jvke2', theme('Piano_in_the_Rain', 'Piano in the Rain', 120, 0, 'major', ['C', 'G', 'Am', 'F'], ['F', 'G', 'Em', 'Am'], ['pianoriff', 'strings'], 'voice', 'fourfloor', 'octave', 811,
    shape='A B A B', start='keys', end='hit', fxB=triplet_arp(.4, 'piano', 24)))
add('pop', 'pretty', theme('Glitter_Halo', 'Glitter Halo', 158, 6, 'minor', ['F#m', 'D', 'A', 'E'], ['D', 'E', 'C#m', 'F#m'], ['plastic', 'pad'], 'chipmunk', 'hyper', '808', 821,
    shape='A B C B', start='cold', end='tapestop', keysB=['glitchheavy', 'pad'], drumsB='dubstep', leadB='plastic', lv=.85))   # glossy hyperpop, riddim-style drops

# ================= DNA Breakcore Squared =================
def dna_bc():
    import dna, batch_e
    from batch_d import blocks
    NOTE = {'A': 69, 'C': 72, 'G': 67, 'T': 74}
    seq = dna.HBB
    def rows(a, up=0):
        out, last = [], None
        for k in range(64):
            n = NOTE[seq[a + k]] + up; out.append(R if n == last else n); last = n
        return [out[i:i + 8] for i in range(0, 64, 8)]
    cfg = dict(batch_e.BC['squared'])
    cfg.update(file='DNA_Breakcore_Squared', title='DNA Breakcore Squared', chords=['Am', 'C', 'G', 'Dm'], melody=blocks(rows(0)), melodyB=blocks(rows(64, 12)), seed=909)
    return cfg

if __name__ == '__main__':
    from breakcore_engine import build as bbuild
    arg = sys.argv[1:]
    names = list(SONGS) + ['dnabc'] if arg == ['all'] else [k for k in SONGS if SONGS[k].get('group') in arg] or arg
    for k in names:
        if k == 'dnabc': bbuild(dna_bc()); continue
        cfg = dict(SONGS[k]); cfg.pop('group', None); build(cfg)
