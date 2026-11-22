"""Steady, bright breakcore.
python songs7.py 17  -> Paper Sky (170 BPM, E major: shimmering guitars, glockenspiel, 808 bass, a new breakbeat, half-time breakdown)"""
import sys
from songs import render, sections_to_bars, slice_fx
from songs3 import glock
from instruments2 import *

def make_break2(st):
    """A different two-bar breakbeat (lighter, funkier, more hats), cut into 16th slices."""
    BM = Mix(32 * st)
    K = {0: [0, 7, 10], 1: [0, 3, 10, 11]}; Sn = {0: [4, 12], 1: [4, 12, 15]}; G = {0: [6, 9, 14], 1: [7, 13]}
    for bar in (0, 1):
        o = bar * 16 * st
        for k in K[bar]: kick(BM, o + k * st, .95, punch=1.)
        for k in Sn[bar]: snare(BM, o + k * st, .9); clap(BM, o + k * st, .3)
        for k in G[bar]: snare(BM, o + k * st, .18)
        for k in range(16): hat(BM, o + k * st, .5 if k % 2 == 0 else .28, open_=(k == 14))
        for k in range(16): shaker(BM, o + k * st, .5 if k % 2 else .25)
    x = np.tanh(BM.buses['drums'] * 1.4) / 1.1
    n = int(st * SR); return [x[:, i * n:(i + 1) * n].copy() for i in range(32)], n

def stretch2(sl, n):   # play one slice at half speed over two slots (lower and slower)
    idx = np.linspace(0, sl.shape[1] - 1, 2 * n); y = np.array([np.interp(idx, np.arange(sl.shape[1]), c) for c in sl])
    f = 80; r = np.linspace(0, 1, f); y[:, :f] *= r; y[:, -f:] *= r[::-1]; return y

def b808(M, t, n, dur, vol, glide_from=None):
    N = int((dur + .05) * SR); tt = tarr(N); f0 = mtof(n)
    f = f0 * (1 + 1.5 * np.exp(-tt / .015))
    if glide_from: f = f * 2 ** (((glide_from - n) * np.exp(-tt / .06)) / 12)
    x = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 1.8) * envN(N, dur, .003, .5, .85, .05)
    M.add('sub', t, lp(x, 1200) * vol)

def paper_sky():
    bpm = 170; st = 60 / bpm / 4; B = 16 * st
    slices, n = make_break2(st)
    C = [('E', [52, 59, 64, 66, 68], 40), ('B/D#', [51, 59, 63, 66, 71], 39), ('C#m', [49, 56, 61, 63, 64], 37), ('A', [45, 57, 61, 64, 71], 45)]   # 2 bars each
    MEL = [[(0, 83, 4), (4, 80, 4), (8, 78, 4), (12, 76, 8), (24, 78, 4), (28, 80, 4)], [(0, 83, 6), (6, 85, 2), (8, 83, 4), (12, 78, 12), (28, 76, 4)],
           [(0, 80, 4), (4, 78, 4), (8, 76, 4), (12, 73, 8), (24, 76, 4), (28, 78, 4)], [(0, 80, 8), (8, 78, 4), (12, 76, 4), (16, 71, 16)]]
    PAT_A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9, 10, 11, 28, 29, 28, 31]
    PAT_B = [0, 1, 16, 17, 4, 5, 6, 7, 0, 1, 10, 11, 12, 13, 4, 15, 16, 17, 18, 19, 20, 21, 4, 23, 24, 25, 10, 11, 28, 29, 12, 12]
    PAT_H = [0, 2, 4, 6, 8, 10, 12, 14, 16, 3, 20, 22, 24, 26, 28, 31]   # half-time picks (each fills two slots)
    secs = [('intro', 8), ('build', 4), ('dropA', 24), ('half', 8), ('dropB', 24), ('outro', 8)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B + 4)
    put = lambda t, sl, g=1.: M.add('break', t, sl[0] * g, sl[1] * g)
    prev_root = None
    for b, (sec, i, nb) in enumerate(bars):
        t0 = b * B; name, v, root = C[(b // 2) % 4]; half = b % 2
        # shimmering picked guitar: steady 8ths up and down the chord
        arp = [v[0] + 12, v[1], v[2], v[3], v[4], v[3], v[2], v[1]]
        gv = 1.1 if sec in ('intro', 'outro') else .7 if sec == 'build' else .45 if sec == 'half' else .22
        for k in range(8): guitar(M, 'gtr', t0 + k * 2 * st, arp[k] + 12, 2 * st * 3, gv, pan=(-.4 if k % 2 else .4), bright=.6, decay=.998)
        # pad
        if half == 0:
            for nn in v[1:4]: supersaw(M, 'pad', t0, nn + 12, 2 * B, (.07 if sec.startswith('drop') else .35 if sec in ('intro', 'outro') else .16), cut=1400, a=.5, r=.8, voices=3)
        # vinyl dust in the quiet parts
        if sec in ('intro', 'half', 'outro'):
            N = int(B * SR); d = np.zeros(N); pos = rng.integers(0, N, 10); d[pos] = rng.uniform(-.5, .5, 10)
            M.add('fx', t0, lp(d, 5000) * .25 + hp(noise(N), 3000) * .005)
        # melody (glockenspiel), with a supersaw lead underneath in drop B
        if (sec in ('dropA', 'dropB', 'half') or (sec == 'intro' and i >= 4)) and half == 0:
            for s, nn, L in MEL[(b // 2) % 4]:
                glock(M, t0 + s * st, nn, .8 if sec.startswith('drop') else .6, pan=.15)
                if sec == 'dropB': supersaw(M, 'lead', t0 + s * st, nn - 12, L * st * .95, .12, cut=3000, a=.01, r=.15, voices=5)
                if sec == 'half': guitar(M, 'gtr', t0 + s * st, nn - 12, L * st * 1.5, .2, pan=0, bright=.7, decay=.999)
        # ---------- breaks ----------
        if sec == 'build':
            fc = 400 * (12 ** ((i + .5) / 4))
            for k in range(16):
                sl = slices[(b % 2) * 16 + k]
                if i == 3 and k >= 12: sl = slice_fx(slices[4], n, 'roll', 2 if k < 14 else 4)
                put(t0 + k * st, np.array([lp(c, fc) for c in sl]), .5 + .12 * i)
            if i == 0: riser(M, t0, 4 * B, .55)
        if sec in ('dropA', 'dropB'):
            if i == 0: crash(M, t0, .85); impact(M, t0, .7)
            if i % 8 == 0 and i: crash(M, t0, .5)
            pat = PAT_A if sec == 'dropA' else PAT_B
            for k in range(16):
                idx = pat[(b % 2) * 16 + k]; sl = slices[idx]
                if half == 1 and k >= 14 and i % 4 == 3: sl = slice_fx(slices[12], n, 'roll', 2 if k == 14 else 4)   # tiny fill every 4 bars
                put(t0 + k * st, sl)
            # 808: root on 1, a pickup, then the root again; glides into each new chord
            for s, L in ((0, 7), (7, 3), (10, 6)):
                b808(M, t0 + s * st, root, L * st * .95, .55, glide_from=prev_root if (s == 0 and half == 0 and prev_root and prev_root != root) else None)
            prev_root = root
        if sec == 'half':
            for k in range(0, 16, 2): put(t0 + k * st, stretch2(slices[PAT_H[(b % 2) * 8 + k // 2]], n), .85)
            b808(M, t0, root, B * .95, .5)
            if i == nb - 1: riser(M, t0, B, .5)
        if sec == 'outro' and i < 4:
            for k in range(0, 16, 4): put(t0 + k * st, np.array([lp(c, 1500 - 300 * i) for c in slices[(b % 2) * 16 + k]]), .45 - .08 * i)
        if sec == 'outro' and i == nb - 1:
            for j, nn in enumerate([52, 59, 64, 68, 71, 76]): guitar(M, 'gtr', t0 + j * .05, nn, 3., .16)
            glock(M, t0 + .3, 88, .35)
    M.buses['gtr'] = chorus(M.buses['gtr'], mix=.35)
    M.buses['glock_d'] = pingpong(M.buses['glock'], 3 * st, .35)
    render(M, 'Paper_Sky_170bpm',
           sends={'gtr': .3, 'pad': .5, 'glock': .4, 'lead': .3, 'break': .05, 'fx': .1},
           levels={'gtr': 1., 'pad': .8, 'glock': 1.2, 'glock_d': .45, 'lead': .9, 'break': .7, 'sub': .7, 'fx': .8}, duck=(), fade=0.)

if __name__ == '__main__':
    {'17': paper_sky}[sys.argv[1]]()
