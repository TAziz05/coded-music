"""Extra code-only instruments: plucked strings (Karplus-Strong), fingered bass, synth sax, synth 'voice' lead."""
import numpy as np, scipy.signal as ss
from engine import *

def envN(N, *a):
    e = env(*a); return np.pad(e, (0, max(0, N - len(e))))[:N]

def ks(f, dur, bright=.6, decay=.997, pick=.22):
    """Karplus-Strong plucked string, retuned by resampling so every pitch is exact."""
    Nf = SR / f; N = max(2, int(Nf - .5)); L = int((dur + .25) * SR) + N
    exc = lp(noise(N), 1200 + 8000 * bright); k = max(1, int(N * pick)); exc = exc - .8 * np.roll(exc, k)
    x = np.zeros(L); x[:N] = exc
    a = np.zeros(N + 2); a[0] = 1; a[N] = -decay * .5; a[N + 1] = -decay * .5
    y = ss.lfilter([1.], a, x)
    ratio = (N + .5) / Nf; idx = np.arange(0, len(y) - 1, ratio)
    y = np.interp(idx, np.arange(len(y)), y)
    n = int((dur + .25) * SR); y = y[:n]; t = tarr(len(y))
    y *= np.where(t < dur, 1., np.exp(-(t - dur) / .04))
    return y / (np.abs(y).max() + 1e-9)

def guitar(M, bus, t, n, dur, vol, pan=0., bright=.6, decay=.997):
    y = ks(mtof(n), dur, bright, decay); M.add(bus, t, y * vol, pan=pan)

def strum(M, bus, t, notes, dur, vol, down=True, gap=.012, pan=0., bright=.55):
    seq = notes if down else notes[::-1]
    for j, n in enumerate(seq): guitar(M, bus, t + j * gap, n, dur - j * gap, vol * (1 - .06 * j), pan=pan + (j - 2) * .08, bright=bright)

def fbass(M, t, n, dur, vol, bus='bass'):
    y = lp(ks(mtof(n), dur, .35, .995, .12), 1600) * .8
    e = env(dur, .005, .4, .7, .05); e = np.pad(e, (0, max(0, len(y) - len(e))))[:len(y)]
    y = y + sine(mtof(n), len(y)) * e * .5
    M.add(bus, t, np.tanh(y * 1.3) * vol)

def sax(M, bus, t, n, dur, vol, pan=0.):
    N = int((dur + .18) * SR); tt = tarr(N)
    vib = np.clip((tt - .18) / .25, 0, 1) * .22 * np.sin(2 * np.pi * 5.3 * tt)
    scoop = -.9 * np.exp(-tt / .035)
    f = mtof(n) * 2 ** ((vib + scoop) / 12)
    x = saw(f, N) * .75 + sqr(f, N, .42) * .35
    e = envN(N, dur, .035, .4, .8, .1)
    swell = np.clip(tt / .12, 0, 1) * (.8 + .2 * np.sin(2 * np.pi * .7 * tt))
    lo = lp(x, 900); hi = lp(x, 3400); y = lo + (hi - lo) * np.clip(e * swell, 0, 1)
    y = y + 1.1 * bp(y, 450, 800) + .7 * bp(y, 1300, 2100) + .25 * bp(y, 2600, 3600)
    y += bp(noise(N), 1500, 5000) * .05
    y = np.tanh(y * 1.2) * e
    M.add(bus, t, y * vol * .45, pan=pan)

def voice(M, bus, t, n, dur, vol, prev=None, pan=0.):
    """A singing-ish synth lead: saw through 'ah' formants, vibrato, and a short glide from the previous note."""
    N = int((dur + .15) * SR); tt = tarr(N)
    vib = np.clip((tt - .2) / .2, 0, 1) * .3 * np.sin(2 * np.pi * 5.8 * tt)
    glide = ((prev - n) * np.exp(-tt / .04)) if prev else -.5 * np.exp(-tt / .03)
    f = mtof(n) * 2 ** ((vib + glide) / 12)
    x = saw(f, N) + .5 * sqr(f, N, .3)
    y = .4 * lp(x, 1200) + 1.3 * bp(x, 650, 1000) + 1.0 * bp(x, 1050, 1500) + .35 * bp(x, 2600, 3300)
    e = envN(N, dur, .02, .3, .85, .09)
    M.add(bus, t, y * e * vol * .35, pan=pan)

def chorus(st, depth=.003, rate=.8, mix=.5):
    n = st.shape[1]; t = np.arange(n) / SR; out = st.copy()
    for c, ph in ((0, 0), (1, np.pi)):
        d = (.012 + depth * np.sin(2 * np.pi * rate * t + ph)) * SR
        out[c] = st[c] * (1 - mix) + np.interp(np.arange(n) - d, np.arange(n), st[1 - c]) * mix
    return out
