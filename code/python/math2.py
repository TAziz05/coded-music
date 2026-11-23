"""More songs built from math (all sounds are code).
  Collatz Climb      the 3n+1 problem: halve even numbers, triple-plus-one odd ones; every number becomes a note, and every song ends at 4, 2, 1
  Prime Time         each instrument repeats on a prime number of steps (2, 3, 5, 7, 11, 13), so the layers drift and rarely line up
  Sierpinski Steps   Pascal's triangle with odd numbers marked: each row is a drum pattern (a fractal), and the melody follows the Thue-Morse sequence
  Fourier Rise       the lead is built from sine waves: 1, then 3, 5, 9, 15 harmonics, turning a pure tone into a square wave; it ends by taking them away
python math2.py all  (or: collatz primes sierpinski fourier)"""
import sys, math
import numpy as np
from newstyles import *
from popkit import build
import mathsong as ms                       # registers the 'euclid' drums; pentatonic helpers
from math import comb

PENT = [0, 3, 5, 7, 10]
def deg(i, base=69): return base + 12 * (i // 5) + PENT[i % 5]
def rows_from(notes):                       # list of eighth notes (0 rest) -> rows of 8
    notes = notes + [0] * (-len(notes) % 8); return [notes[k:k + 8] for k in range(0, len(notes), 8)]

# ---------------- Collatz ----------------
def collatz(n):
    out = [n]
    while n != 1: n = n // 2 if n % 2 == 0 else 3 * n + 1; out.append(n)
    return out
def collatz_notes(starts, count):           # value -> pitch by its size (log2), odd steps marked for an accent
    seq = []
    for s in starts: seq += collatz(s)
    seq = seq[:count]
    notes = [deg(int(round(math.log2(v) * 1.2)) % 10, 69) for v in seq]
    odd = [v % 2 == 1 and v != 1 for v in seq]
    return notes, odd
CN, CODD = collatz_notes([27], 64)          # 27 takes 111 steps to reach 1: the verse plays its first 64
CN2, CODD2 = collatz_notes([97], 64)
def accents(odd, notes):
    def f(M, t0, st, S, i, n, tones, root):    # a brass hit on every odd number (where 3n + 1 kicks the number up)
        for k in range(8):
            j = (i % (len(notes) // 8)) * 8 + k
            if odd[j]: brass(M, 'keys', t0 + S(2 * k), notes[j], st * 1.6, .14)
    return f
def end_421(M, t0, st, S, i, n, tones, root):  # every Collatz path ends 4 -> 2 -> 1: three times, all the same length, then the 1 echoes away
    if i: return
    t = t0; note = lambda v: deg(int(round(math.log2(v) * 1.2)) % 10, 69)
    for r in range(3):
        for v in (4, 2, 1): marimba(M, 'lead', t, note(v), st * 2, 1.); t += st * 2
    for k in range(1, 7): marimba(M, 'lead', t - st * 2 + k * st * 3, note(1), st * 2, .8 * .6 ** k)   # echo

# ---------------- Prime Time ----------------
G = [0]                                      # global 16th-note counter, so the prime cycles run through the whole song
PLAYERS = [(2, lambda M, t, T: hat(M, t, .18)), (3, lambda M, t, T: celesta(M, 'glock', t, T[0] + 24, .2, .45)),
           (5, lambda M, t, T: marimba(M, 'keys', t, T[1] + 12, .3, .6, pan=-.4))]   # 2, 3 and 5 count in 8th notes
SLOW = [(7, lambda M, t, T: conga(M, t, 50, .55, pan=-.3)), (11, lambda M, t, T: woodblock(M, t, False, .35)),
        (13, lambda M, t, T: cowbell(M, t, T[2] + 12, .2, .22))]   # 7, 11 and 13 count in quarter notes, so they always land on a beat
def prime_drums(layers):
    def f(M, t0, st, S, i, n, fill):
        for s in (0, 8): kick(M, t0 + S(s), .8)
        for s in (4, 12): snare(M, t0 + S(s), .6)
        for k in range(8):   # counted in 8th notes, and every 2 bars all the cycles start again together on the downbeat
            g = G[0] % 16 + k
            for p, fn in PLAYERS[:layers]:
                if g % p == 0: fn(M, t0 + S(2 * k), PT[0])
        if layers > 3:   # every 4 bars (16 beats) all the slow cycles start together on the downbeat
            for q in range(4):
                g = (G[0] // 2) % 16 + q
                for p, fn in SLOW:
                    if g % p == 0: fn(M, t0 + S(4 * q), PT[0])
        G[0] += 8
    return f
PT = [[57, 60, 64]]
def keep_tones(M, t0, st, S, i, n, tones, root): PT[0] = tones
for L in (2, 3, 6): EXTRA_DRUMS[f'primes{L}'] = prime_drums(L)
def gap_melody(bars, start=0):               # prime gaps (1, 2, 2, 4, 2, 4, ...) become note lengths and steps up the scale
    pr = [p for p in range(2, 2000) if all(p % q for q in range(2, int(p ** .5) + 1))]
    gaps = [b - a for a, b in zip(pr, pr[1:])][start:]
    out, pos, idx = [], 0, 4
    for gp in gaps:
        L = min(gp, 6); idx = (idx + (gp % 5) - 2) % 10
        out += [deg(idx, 69)] + [-1] * (L - 1)
        if len(out) >= bars * 8: break
    return rows_from(out[:bars * 8])
def end_primes(M, t0, st, S, i, n, tones, root):   # a natural ending: the pad holds the last chord while the 2-3-5 players thin out and stop
    if i: return
    for c in tones[:3]: supersaw(M, 'pad', t0, c + 12, 32 * st, .03, cut=1500, a=.05, r=2.5, voices=3)
    for k in range(16):
        for j, (p, fn) in enumerate(PLAYERS):
            if k % p == 0 and k < 16 - 4 * j: fn(M, t0 + S(k), tones)

# ---------------- Sierpinski ----------------
def pascal_row(r): return [comb(r, k) % 2 if k <= r else 0 for k in range(16)]
SB = [0]
@D('sierpinski')
def _(M, t0, st, S, i, n, fill):
    row = pascal_row(SB[0] % 16); SB[0] += 1
    for s in (0, 4, 8, 12): kick(M, t0 + S(s), .75)
    for s in (4, 12): snare(M, t0 + S(s), .6)
    for k, on in enumerate(row):
        if on: rim(M, t0 + S(k), .5); woodblock(M, t0 + S(k), k % 2 == 0, .35)
def thue_morse(n): return bin(n).count('1') % 2
MOTIF = {0: [0, 2, 4, 2], 1: [4, 3, 1, 3]}       # 0 = a rising figure, 1 = a falling one
def tm_melody(bars, offset=0, base=69):
    out = []
    for b in range(bars):
        for j, d in enumerate(MOTIF[thue_morse(b + offset)]):
            out += [deg(d + 2 * thue_morse(4 * (b + offset) + j), base), -1]
    return rows_from(out)
def end_sierpinski(M, t0, st, S, i, n, tones, root):   # row 15 of the triangle is all odd: 16 hits in a row, then the last chord
    if i: return
    for k in range(16): rim(M, t0 + S(k), .42 + .012 * k); woodblock(M, t0 + S(k), k % 2 == 0, .4)
    te = t0 + 16 * st; kick(M, te, .35); crash(M, te, .12)
    for c in tones[:3]: plastic(M, 'keys', te, c + 24, 1.5, .25)

# ---------------- Fourier ----------------
def fourier_lead(nh, saw_=False):
    def f(M, t, n, d, v):                     # square wave from its Fourier series: sum of odd harmonics k with strength 1/k (all harmonics for saw)
        N = int((d + .2) * SR); tt = tarr(N); fq = mtof(n); x = np.zeros(N)
        ks_ = range(1, 2 * nh, 1 if saw_ else 2)
        for k in list(ks_)[:nh]:
            if fq * k < 9000: x += np.sin(2 * np.pi * fq * k * tt) / k
        M.add('lead', t, x * envN(N, d * .95, .01, .2, .85, .08) * v * .22)
    return f
for nh in (1, 3, 5, 9, 15): LEADS[f'fourier{nh}'] = fourier_lead(nh)
LEADS['fouriersaw'] = fourier_lead(30, True)
def end_fourier(M, t0, st, S, i, n, tones, root):   # the harmonics leave one at a time until only the pure sine is left
    if i: return
    for j, nh in enumerate((15, 9, 5, 3, 2, 1)):
        fourier_lead(nh)(M, t0 + j * 2 * st, tones[0] + 12, 2 * st, .9)
    fourier_lead(1)(M, t0 + 12 * st, tones[0] + 12, 3., .9)
    for c in tones[:3]: supersaw(M, 'pad', t0 + 12 * st, c + 12, 3., .03, cut=1200, a=.05, r=1.5, voices=3)
FA = [[69,-1,72,-1,76,-1,74,72],[71,-1,-1,67,-1,-1,0,0],[69,-1,72,-1,76,-1,79,77],[76,-1,-1,-1,0,0,0,0]]
FB = [[81,-1,79,76,-1,74,-1,76],[79,-1,-1,76,-1,72,-1,-1],[77,-1,76,74,-1,72,-1,71],[69,-1,-1,-1,0,0,0,0]]

SONGS = {
 'collatz': dict(file='Collatz_Climb', title='Collatz Climb', bpm=128, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Am', 'F', 'C', 'G'], keys=['pad'], kv=1.6, lead='fmbell', mel=rows_from(CN[:32]), lv=1.2),
   'verse': sec(8, ['Am', 'F', 'C', 'G'], keys=['marimbaarp'], kv=.6, drums='euclid', bass='octave', lead='marimba', mel=rows_from(CN), extra=accents(CODD, CN), kind='verse'),
   'chorus': sec(8, ['F', 'G', 'Am', 'Am'], keys=['synthwave'], drums='euclid', bass='octave', lead='sqbright+marimba', mel=rows_from(CN2), extra=accents(CODD2, CN2), impact=True, kind='chorus'),
   'end': sec(1, ['Am'], extra=end_421, kind='outro')},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'end']),
 'primes': dict(file='Prime_Time', title='Prime Time', bpm=120, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Dm', 'Bb', 'F', 'C'], keys=['pad'], drums='primes2', extra=keep_tones),
   'verse': sec(8, ['Dm', 'Bb', 'F', 'C'], keys=['pad'], drums='primes3', bass='long', lead='plastic', mel=gap_melody(8), extra=keep_tones, kind='verse'),
   'chorus': sec(8, ['Bb', 'C', 'Dm', 'Dm'], keys=['pad', 'pluck'], drums='primes6', bass='octave', lead='sqbright+plastic', mel=gap_melody(8, 40), extra=keep_tones, impact=True, kind='chorus'),
   'end': sec(2, ['Dm'], extra=end_primes, kind='outro')},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'end'], levels={'glock': .9}),
 'sierpinski': dict(file='Sierpinski_Steps', title='Sierpinski Steps', bpm=136, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Em', 'C', 'G', 'D'], keys=['celesta']),
   'verse': sec(8, ['Em', 'C', 'G', 'D'], keys=['celesta'], drums='sierpinski', bass='synth8', lead='plastic', mel=tm_melody(8), kind='verse'),
   'chorus': sec(8, ['C', 'D', 'Em', 'Em'], keys=['plastic', 'pad'], drums='sierpinski', bass='octave', lead='sqbright+plastic', mel=tm_melody(8, 8, 76), impact=True, kind='chorus'),
   'end': sec(1, ['Em'], extra=end_sierpinski, kind='outro')},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'end']),
 'fourier': dict(file='Fourier_Rise', title='Fourier Rise', bpm=110, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Am', 'F', 'C', 'G'], keys=['pad'], lead='fourier1', mel=FA),
   'verse1': sec(8, ['Am', 'F', 'C', 'G'], keys=['pad'], drums='halfpop', bass='long', lead='fourier3', mel=FA, kind='verse'),
   'verse2': sec(8, ['Am', 'F', 'C', 'G'], keys=['pad', 'pluck'], drums='halfpop', bass='octave', lead='fourier5', mel=FA, kind='verse'),
   'chorus1': sec(8, ['F', 'G', 'Am', 'Am'], keys=['pad', 'synthwave'], drums='fourfloor', bass='octave', lead='fourier9', mel=FB, impact=True, kind='chorus'),
   'chorus2': sec(8, ['F', 'G', 'Am', 'Am'], keys=['pad', 'synthwave'], drums='fourfloor', bass='octave', lead='fourier15+fouriersaw', mel=FB, impact=True, kind='chorus'),
   'end': sec(1, ['Am'], extra=end_fourier, kind='outro')},
   order=['intro', 'verse1', 'verse2', 'chorus1', 'chorus2', 'end']),
}

SONGS['collatz']['gain_like'] = {'verse': 'intro', 'chorus': 'intro', 'end': 'intro'}   # one level for the whole song, so nothing drops when the drums come in
SONGS['primes']['fadeout'] = 3.   # the last bars fade out naturally
SONGS['sierpinski']['targets'] = {'outro': -22.}         # a softer last hit

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: G[0] = 0; SB[0] = 0; build(SONGS[k])
