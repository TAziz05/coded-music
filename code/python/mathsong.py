"""'Infinite Series': a song built from math. Every part comes from a formula:
  sin(x)        the intro melody rides a sine wave
  pi            the verse melody is the digits of pi (3.14159...) mapped to a pentatonic scale (computed here with Machin's formula)
  e             the chorus melody is the digits of e (2.71828...), computed from the series e = sum 1/k!
  Fibonacci     the bass walks the Fibonacci numbers (1, 1, 2, 3, 5, 8, ...) mod 9
  Euclid        the drums are Euclidean rhythms E(5,16), E(2,8), E(11,16): hits spread as evenly as possible
  logistic map  hi-hat accents follow the chaotic map x -> 3.9 x (1 - x)
  primes        the bridge rings a bell on the prime-numbered steps 2, 3, 5, 7, 11, 13
  harmonics     a drone built from the harmonic series f, 2f, 3f, ... 8f
  Zeno / 1/2^n  the ending: each note lasts half as long as the one before, 1/2 + 1/4 + 1/8 + ... = 1, and the final chord lands on the limit
python mathsong.py"""
import math
from newstyles import *
from popkit import build

def pi_digits(n):        # Machin: pi = 16 arctan(1/5) - 4 arctan(1/239), in big integers
    U = 10 ** (n + 10)
    def arctan_inv(x):
        s, t, k, sign = 0, U // x, 1, 1
        while t: s += sign * (t // k); t //= x * x; k += 2; sign = -sign
        return s
    return str(16 * arctan_inv(5) - 4 * arctan_inv(239))[:n]
def e_digits(n):         # e = sum 1/k!
    U = 10 ** (n + 10); s, t, k = 0, U, 0
    while t: s += t; k += 1; t //= k
    return str(s)[:n]
PI, E = pi_digits(140), e_digits(140)
PENT = [0, 3, 5, 7, 10]                       # A minor pentatonic
def deg(i, base=69): return base + 12 * (i // 5) + PENT[i % 5]
def digit_mel(ds, bars, base=69):   # digit d -> scale step d (0 = rest); 8 eighth notes per bar
    notes = [deg(int(c) - 1, base) if c != '0' else 0 for c in ds[:bars * 8]]
    return [notes[k * 8:(k + 1) * 8] for k in range(bars)]
def sine_mel(bars, phase=0.):       # step = round(4 + 4 sin(2 pi k / 16))
    notes = [deg(round(4 + 4 * math.sin(2 * math.pi * k / 16 + phase)), 57) for k in range(bars * 8)]
    out = []
    for k in range(len(notes)):     # hold repeated notes instead of re-striking them
        out.append(-1 if k % 8 and notes[k] == notes[k - 1] else notes[k])
    return [out[k * 8:(k + 1) * 8] for k in range(bars)]
def euclid(k, n, rot=0):            # Bjorklund / Bresenham: k hits spread evenly over n steps
    return [s for s in range(n) if ((s + rot) * k) // n != ((s + rot - 1) * k) // n]

X = [.5]
@D('euclid')
def _(M, t0, st, S, i, n, fill):
    for s in euclid(5, 16): kick(M, t0 + S(s), .85)
    for s in [x * 2 for x in euclid(2, 8, 2)]: snare(M, t0 + S(s), .75); clap(M, t0 + S(s), .35)
    for s in euclid(11, 16):
        X[0] = 3.9 * X[0] * (1 - X[0]); hat(M, t0 + S(s), .07 + .28 * X[0])
    for s in euclid(7, 16, 3): rim(M, t0 + S(s), .35)

FIB = [1, 1]
while len(FIB) < 80: FIB.append(FIB[-1] + FIB[-2])
BAR = [0]
@Bs('fib')
def _(M, t0, st, S, root):
    k = BAR[0]; BAR[0] += 1
    for h in (0, 1):
        f = FIB[2 * k + h] % 9; fbass(M, t0 + S(8 * h), deg(f, 33), 7 * st, .7)
        fbass(M, t0 + S(8 * h + 6), deg(f, 33) + 12, st * .8, .35)

def harmonics(M, t0, st, S, i, n, tones, root):   # harmonic-series drone: f, 2f, 3f ... 8f, each swelling at its own rate
    if i % 2: return
    f0 = mtof(45); N = int(32 * st * SR) + int(.5 * SR); tt = tarr(N); x = np.zeros(N)
    for h in range(1, 9): x += np.sin(2 * np.pi * f0 * h * tt) / h * (.5 + .5 * np.sin(2 * np.pi * tt * h / (32 * st)))
    M.add('pad', t0, x * np.sin(np.pi * tt / tt[-1]) * .08)
PRIMES = [2, 3, 5, 7, 11, 13]
def primes(M, t0, st, S, i, n, tones, root):      # a bell on every prime-numbered step; pitch = the prime mod 9 up the scale
    for p in PRIMES: celesta(M, 'glock', t0 + S(p), deg((p + i) % 9, 69), st * 2, .55, pan=(-.5, .5)[p % 2])
    harmonics(M, t0, st, S, i, n, tones, root)
def zeno(M, t0, st, S, i, n, tones, root):        # durations 1/2, 1/4, 1/8 ... of a 2-beat span: the notes speed up toward a limit
    if i: return
    T = 8 * st; t = t0; d = T / 2
    for k in range(10):
        plastic(M, 'lead', t, deg(k, 69), max(d, .03), .9); t += d; d /= 2
    lim = t0 + T
    kick(M, lim, 1.); crash(M, lim, .6); fbass(M, lim, 33, 2., .7)
    for c in (57, 64, 69, 72, 76): supersaw(M, 'keys', lim, c, 2.5, .05, cut=3000, a=.003, r=1., voices=4)
    harmonics(M, lim, st, S, 0, 1, tones, root)

CH = ['Am', 'F', 'C', 'G']
CHF = ['Am', 'F', 'C', 'C', 'G', 'G', 'G', 'Am']      # chorus chords last 1, 1, 2, 3, 1 bars (Fibonacci)
s = {'intro': sec(4, CH, keys=['pad'], lead='fmbell', mel=sine_mel(4), lv=.8, extra=harmonics),
     'verse1': sec(8, CH, keys=['marimbaarp'], drums='euclid', bass='fib', lead='marimba', mel=digit_mel(PI, 8), kind='verse', kv=.7),
     'verse2': sec(8, CH, keys=['marimbaarp'], drums='euclid', bass='fib', lead='marimba', mel=digit_mel(PI[64:], 8), kind='verse', kv=.7),
     'chorus1': sec(8, CHF, keys=['synthwave'], drums='euclid', bass='fib', lead='sqbright+fmbell', mel=digit_mel(E, 8, 57), kind='chorus', impact=True),
     'chorus2': sec(8, CHF, keys=['synthwave'], drums='euclid', bass='fib', lead='sqbright+fmbell', mel=digit_mel(E[64:], 8, 57), kind='chorus', impact=True),
     'bridge': sec(4, CH, keys=['pad'], lead='fmbell', mel=sine_mel(4, math.pi), lv=.7, extra=primes, kind='bridge'),
     'end': sec(1, ['Am'], extra=zeno, fill=False, kind='outro')}
SONG = dict(file='Infinite_Series', title='Infinite Series', bpm=120, sections=s, verb=2.4, chorus_keys=True, levels={'lead': 1.15, 'glock': .9},
            order=['intro', 'verse1', 'chorus1', 'verse2', 'chorus2', 'bridge', 'chorus1', 'end'])

if __name__ == '__main__':
    print('pi', PI[:20], '... e', E[:20], '...')
    build(SONG)
