"""Tiny code-only synth engine: every sound is built from math (oscillators, noise, filters).
No samples, no AI audio models."""
import numpy as np, scipy.signal as ss
from functools import lru_cache

SR = 44100
rng = np.random.default_rng(322)

def mtof(n): return 440.0 * 2 ** ((n - 69) / 12)

@lru_cache(None)
def _sos(kind, fc, order):
    if isinstance(fc, tuple): fc = tuple(min(f, SR * .45) for f in fc)
    else: fc = min(fc, SR * .45)
    return ss.butter(order, fc, btype=kind, fs=SR, output='sos')
def lp(x, fc, o=2): return ss.sosfilt(_sos('lowpass', int(fc), o), x)
def hp(x, fc, o=2): return ss.sosfilt(_sos('highpass', int(fc), o), x)
def bp(x, lo, hi, o=2): return ss.sosfilt(_sos('bandpass', (int(lo), int(hi)), o), x)
def noise(n): return rng.uniform(-1, 1, n)

# ---------- oscillators (band-limited with PolyBLEP) ----------
def _phase(f, n, ph0=None):
    f = np.broadcast_to(np.asarray(f, float), (n,)); dt = f / SR
    ph0 = rng.random() if ph0 is None else ph0
    return (ph0 + np.cumsum(dt) - dt) % 1.0, dt
def _blep(t, dt):
    o = np.zeros_like(t)
    m = t < dt; x = t[m] / dt[m]; o[m] = 2 * x - x * x - 1
    m = t > 1 - dt; x = (t[m] - 1) / dt[m]; o[m] = x * x + 2 * x + 1
    return o
def saw(f, n, ph0=None):
    t, dt = _phase(f, n, ph0); return 2 * t - 1 - _blep(t, dt)
def sqr(f, n, pw=.5, ph0=None):
    t, dt = _phase(f, n, ph0)
    return np.where(t < pw, 1., -1.) + _blep(t, dt) - _blep((t + 1 - pw) % 1, dt)
def sine(f, n, ph0=0.):
    t, _ = _phase(f, n, ph0); return np.sin(2 * np.pi * t)

def env(dur, a=.005, d=.1, s=.7, r=.1):
    n = int((dur + r) * SR); t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-5), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-5)))
    k = min(int(dur * SR), n)
    if k < n:
        lvl = e[k - 1] if k > 0 else 0
        e[k:] = lvl * (1 - np.clip((t[k:] - dur) / r, 0, 1)) ** 2
    return e
def tarr(n): return np.arange(n) / SR

# ---------- mixer ----------
class Mix:
    def __init__(s, secs):
        s.n = int((secs + 4) * SR); s.buses = {}; s.kicks = []
    def add(s, bus, t, L, R=None, gain=1., pan=0.):
        if R is None:
            a = (pan + 1) * np.pi / 4; R = L * np.sin(a) * 1.414; L = L * np.cos(a) * 1.414
        if bus not in s.buses: s.buses[bus] = np.zeros((2, s.n))
        i = int(t * SR); j = min(i + len(L), s.n)
        if j <= i: return
        s.buses[bus][0, i:j] += L[:j - i] * gain; s.buses[bus][1, i:j] += R[:j - i] * gain
    def duck_curve(s, depth=.6, rel=.14):
        g = np.ones(s.n); w = int(rel * 5 * SR); c = 1 - depth * np.exp(-tarr(w) / rel)
        for k in s.kicks:
            i = int(k * SR); j = min(i + w, s.n); g[i:j] = np.minimum(g[i:j], c[:j - i])
        return lp(g, 60)

def reverb_ir(secs=2.2, decay=.55, bright=6500):
    n = int(secs * SR); t = tarr(n); pre = int(.02 * SR)
    ir = [np.concatenate([np.zeros(pre), lp(noise(n) * np.exp(-t / decay), bright)]) for _ in range(2)]
    ir = np.array(ir); return ir / np.sqrt((ir ** 2).sum() / 2) * .9

def pingpong(st, delay, fb=.4, taps=5):
    L = np.zeros_like(st[0]); R = np.zeros_like(st[1]); d = int(delay * SR); src = (st[0] + st[1]) / 2
    for k in range(1, taps + 1):
        sh = d * k; g = fb ** k; tgt = L if k % 2 else R
        tgt[sh:] += src[:-sh] * g
    return np.array([lp(L, 5000), lp(R, 5000)])

def master(M, sends, levels, duck_buses, fade_out=6., rev=None):
    duck = M.duck_curve()
    out = np.zeros((2, M.n)); send = np.zeros((2, M.n))
    for b, x in M.buses.items():
        if b in duck_buses: x = x * duck
        out += x * levels.get(b, 1.); send += x * levels.get(b, 1.) * sends.get(b, 0.)
    ir = reverb_ir() if rev is None else rev
    wet = np.array([ss.fftconvolve(send[c], ir[c])[:M.n] for c in range(2)])
    out = out + wet
    out = np.array([hp(c, 28) for c in out])
    nz = np.nonzero(np.abs(out).max(0) > 1e-4)[0]; end = nz[-1] + int(.3 * SR); out = out[:, :end]
    if fade_out:
        f = int(fade_out * SR); out[:, -f:] *= np.linspace(1, 0, f) ** 2
    out = out / np.abs(out).max() * 1.15
    out = np.tanh(out) / np.tanh(1.15)
    return out / np.abs(out).max() * .89

# ---------- instruments ----------
def supersaw(M, bus, t, n, dur, vol, cut=2200, cut_lo=None, fdec=.25, a=.01, d=.3, s=.85, r=.3,
             voices=5, detune=.16, width=.8):
    e = env(dur, a, d, s, r); N = len(e); f = mtof(n); L = np.zeros(N); R = np.zeros(N)
    for i in range(voices):
        off = (i - (voices - 1) / 2) / ((voices - 1) / 2) if voices > 1 else 0
        x = saw(f * 2 ** (off * detune / 12), N); p = off * width
        L += x * np.cos((p + 1) * np.pi / 4); R += x * np.sin((p + 1) * np.pi / 4)
    def F(x):
        if cut_lo is None: return lp(x, cut)
        lo = lp(x, cut_lo); return lo + (lp(x, cut) - lo) * np.exp(-tarr(N) / fdec)
    M.add(bus, t, F(L) * e * vol / voices * 1.6, F(R) * e * vol / voices * 1.6)

def brass(M, bus, t, n, dur, vol, pan=0., bright=1.):
    N = int((dur + .25) * SR); tt = tarr(N)
    vib = np.clip((tt - .22) / .3, 0, 1) * .18 * np.sin(2 * np.pi * 5.6 * tt)
    scoop = -.35 * np.exp(-tt / .025)
    f = mtof(n) * 2 ** ((vib + scoop) / 12)
    x = saw(f * 2 ** (-.07 / 12), N) + saw(f * 2 ** (.07 / 12), N) + .6 * saw(f / 2, N) + .3 * sqr(f, N, .3)
    fe = np.clip(tt / .05, 0, 1) * (.45 + .55 * np.exp(-tt / .3))
    lo = lp(x, 650); y = lo + (lp(x, 4200 * bright) - lo) * fe
    e = env(dur, .03, .25, .85, .2)[:N]
    M.add(bus, t, y[:len(e)] * e * vol * .4, pan=pan)

def pluck(M, bus, t, n, dur, vol, pan=0., dec=.09, cut=5500):
    N = int((dur + .1) * SR); f = mtof(n)
    x = sqr(f, N, .3) * .6 + saw(f * 1.004, N) * .5
    lo = lp(x, 450); y = lo + (lp(x, cut) - lo) * np.exp(-tarr(N) / dec)
    e = env(dur, .002, .18, .25, .08)[:N]
    M.add(bus, t, y[:len(e)] * e * vol, pan=pan)

def bass(M, bus, t, n, dur, vol, cut=1100, growl=0.):
    N = int((dur + .06) * SR); f = mtof(n)
    x = saw(f, N) * .6 + sine(f / 2 if growl < 0 else f, N) * .9 + growl * sqr(f, N, .25)
    lo = lp(x, 220); y = lo + (lp(x, cut) - lo) * np.exp(-tarr(N) / .09)
    e = env(dur, .004, .2, .75, .05)[:N]
    M.add(bus, t, y[:len(e)] * e * vol)

def epiano(M, bus, t, n, dur, vol, pan=0.):
    N = int((dur + .6) * SR); tt = tarr(N); f = mtof(n)
    idx = 2.2 * np.exp(-tt / .35) + .25
    mod = np.sin(2 * np.pi * f * tt) * idx
    x = np.sin(2 * np.pi * f * tt + mod) + .15 * np.sin(2 * np.pi * f * 4.0 * tt) * np.exp(-tt / .08)
    x2 = np.sin(2 * np.pi * f * 1.003 * tt + mod)
    trem = 1 + .12 * np.sin(2 * np.pi * 4.5 * tt)
    e = env(dur, .003, .9, .35, .5)[:N]
    M.add(bus, t, x[:len(e)] * e * vol * trem[:len(e)], x2[:len(e)] * e * vol * (2 - trem[:len(e)]))

def leadsq(M, bus, t, n, dur, vol, pan=0.):
    N = int((dur + .15) * SR); tt = tarr(N)
    vib = np.clip((tt - .2) / .2, 0, 1) * .12 * np.sin(2 * np.pi * 5.2 * tt)
    x = sqr(mtof(n) * 2 ** (vib / 12), N, .28) + .4 * saw(mtof(n + 12), N)
    y = lp(lp(x, 3200), 3200)
    e = env(dur, .008, .2, .7, .12)[:N]
    M.add(bus, t, y[:len(e)] * e * vol * .45, pan=pan)

# ---------- drums ----------
def kick(M, t, vol=1., bus='drums', punch=1.):
    N = int(.45 * SR); tt = tarr(N); f = 46 + 120 * punch * np.exp(-tt / .035)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .26)
    x += lp(noise(N), 4000) * np.exp(-tt / .004) * .35
    M.add(bus, t, np.tanh(x * 1.6) * vol); M.kicks.append(t)
def snare(M, t, vol=1., bus='drums', pan=0.):
    N = int(.35 * SR); tt = tarr(N)
    x = bp(noise(N), 1200, 9000) * np.exp(-tt / .13) * .8
    x += np.sin(2 * np.pi * np.cumsum(190 + 60 * np.exp(-tt / .02)) / SR) * np.exp(-tt / .07) * .6
    M.add(bus, t, x * vol, pan=pan)
def clap(M, t, vol=1., bus='drums'):
    N = int(.4 * SR); tt = tarr(N); e = np.zeros(N)
    for o in (0, .011, .022): e += (tt >= o) * np.exp(-np.clip(tt - o, 0, None) / .006)
    e += (tt >= .03) * np.exp(-np.clip(tt - .03, 0, None) / .12) * .7
    M.add(bus, t, bp(noise(N), 900, 3800) * e * vol * .9)
def hat(M, t, vol=1., open_=False, bus='drums', pan=.25):
    N = int((.35 if open_ else .08) * SR); tt = tarr(N)
    x = hp(noise(N), 7500, 4) * np.exp(-tt / (.22 if open_ else .03))
    M.add(bus, t, x * vol * .5, pan=pan)
def shaker(M, t, vol=1., bus='drums'):
    N = int(.1 * SR); tt = tarr(N)
    e = np.clip(tt / .012, 0, 1) * np.exp(-tt / .04)
    M.add(bus, t, bp(noise(N), 5000, 12000) * e * vol * .35, pan=-.3)
def crash(M, t, vol=1., bus='fx'):
    N = int(2.5 * SR); tt = tarr(N)
    L = lp(hp(noise(N), 4000), 13000) * np.exp(-tt / 1.0); R = lp(hp(noise(N), 4000), 13000) * np.exp(-tt / 1.0)
    M.add(bus, t, L * vol * .45, R * vol * .45)
def tom(M, t, n, vol=1., bus='drums', pan=0.):
    N = int(.4 * SR); tt = tarr(N); f0 = mtof(n)
    x = np.sin(2 * np.pi * np.cumsum(f0 * (1 + .7 * np.exp(-tt / .03))) / SR) * np.exp(-tt / .18)
    M.add(bus, t, np.tanh(x * 1.3) * vol * .8, pan=pan)
def riser(M, t, dur, vol=1., bus='fx'):
    N = int(dur * SR); x = noise(N); out = np.zeros(N); k = 24; c = N // k
    for i in range(k):
        fc = 400 * (30 ** (i / k)); seg = bp(x[max(0, i * c - 2000):(i + 1) * c], fc * .7, min(fc * 1.6, 18000))
        out[i * c:(i + 1) * c] = seg[-c:]
    e = (tarr(N) / dur) ** 2.2
    M.add(bus, t, lp(out, 16000) * e * vol * .7)
def impact(M, t, vol=1.):
    N = int(1.8 * SR); tt = tarr(N)
    x = np.sin(2 * np.pi * np.cumsum(38 + 80 * np.exp(-tt / .06)) / SR) * np.exp(-tt / .7)
    M.add('fx', t, np.tanh(x * 1.5) * vol * .8)

def melody(bars):
    flat = [x for b in bars for x in b]; ev = []
    for i, x in enumerate(flat):
        if x > 0:
            L = 1
            while i + L < len(flat) and flat[i + L] == -1: L += 1
            ev.append((i, x, L))
    return ev
