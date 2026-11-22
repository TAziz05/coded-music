"""Orchestral -> breakcore -> orchestral.
python songs6.py 16  -> Shattered Overture (90 BPM orchestra, switches to 180 BPM breakcore, ends back with the orchestra)
The breakcore runs at exactly double the orchestra's tempo, so the chords keep the same pace through the switch."""
import sys
from songs import make_break, slice_fx, piano
from songs3 import timpani, glock
from songs5 import violins, harp, horn, oboe, cymbal, roll, render_hall
from instruments2 import *

def shattered_overture():
    q = 60 / 90; OB = 4 * q          # orchestral beat and bar (90 BPM, 4/4)
    st = 60 / 180 / 4                # breakcore 16th (180 BPM): 32 of them per orchestral bar
    R = np.random.default_rng(2026)
    slices, n = make_break(st)
    CH = {'Dm': [50, 57, 62, 65], 'Bb': [46, 58, 62, 65], 'F': [41, 57, 60, 65], 'C': [48, 55, 60, 64],
          'Gm': [43, 55, 58, 62], 'A': [45, 57, 61, 64], 'D': [50, 57, 62, 66]}
    prog = ['Dm', 'Bb', 'F', 'C', 'Dm', 'Bb', 'Gm', 'A']
    theme = [[(0, 69, 2), (2, 74, 1), (3, 72, 1)], [(0, 70, 3), (3, 69, 1)], [(0, 72, 2), (2, 77, 1), (3, 76, 1)], [(0, 76, 4)],
             [(0, 74, 2), (2, 77, 1), (3, 81, 1)], [(0, 82, 3), (3, 81, 1)], [(0, 79, 2), (2, 77, 1), (3, 74, 1)], [(0, 73, 4)]]
    plan = [('intro', i) for i in range(8)] + [('rise', i) for i in range(2)] + [('breakA', i) for i in range(8)] + \
           [('breakB', i) for i in range(8)] + [('return', i) for i in range(4)] + [('end', i) for i in range(4)]
    M = Mix(len(plan) * OB + 8)
    put = lambda t, sl, g=1.: M.add('break', t, sl[0] * g, sl[1] * g)
    for b, (sec, i) in enumerate(plan):
        t0 = b * OB
        name = prog[i % 8] if sec != 'end' else ['Gm', 'A', 'Dm', 'D'][i]
        if sec == 'rise': name = ['Gm', 'A'][i]
        v = CH[name]; root = v[0]
        orch = sec in ('intro', 'rise', 'return', 'end')
        # ---------------- orchestra ----------------
        sv = {'intro': .75, 'rise': .8, 'breakA': .55, 'breakB': .6, 'return': 1., 'end': 1.}[sec]
        for j, nn in enumerate(v[1:]): violins(M, t0, nn + (12 if sec.startswith('break') else 0), OB * .98, sv, att=.35 if orch else .15, pan=(j - 1) * .35)
        violins(M, t0, root, OB * .98, .55 * sv, att=.3, bus='low')
        if sec in ('intro', 'return', 'end'):   # harp: flowing eighths across the chord
            arp = [root + 12, v[1], v[2], v[3], v[2] + 12, v[3] + 12, v[2] + 12, v[3]]
            for k in range(8): harp(M, t0 + k * q / 2, arp[k], .8 if sec == 'intro' else 1.1, pan=-.35 + k * .08)
        if sec == 'intro':
            mel = theme[i]
            for s, nn, L in mel:
                if i < 4: horn(M, t0 + s * q, nn - 12, L * q * .97, .8)
                else: horn(M, t0 + s * q, nn - 12, L * q * .97, .8); oboe(M, t0 + s * q, nn, L * q * .97, .6, pan=.2)
            if i in (0, 4): timpani(M, t0, 38, .6)
            if i == 4: cymbal(M, t0, .4)
        if sec == 'rise':    # strings tremolo + timpani roll + the breakbeat creeping in underneath
            for k in range(16): violins(M, t0 + k * q / 4, v[1] + 12, q / 4 * .9, .25 + .03 * k + .25 * i, att=.01, bus='lead')
            roll(M, t0, 45 if i else 43, OB, .45 + .2 * i)
            if i == 0: riser(M, t0, 2 * OB, .7)
            for k in range(32):
                if i == 1 and k >= 28: continue          # a moment of silence right before the drop
                if (i == 0 and k % 4) or (i == 1 and k % 2 and k < 16): continue
                sl = slices[k % 32]
                if i == 1 and k >= 16: sl = slice_fx(slices[4], n, 'roll', 2 if k < 24 else 4)
                put(t0 + k * st, sl, .15 + .3 * i + .01 * k)
        # ---------------- breakcore ----------------
        if sec.startswith('break'):
            if i == 0: crash(M, t0, .9); impact(M, t0, .8); timpani(M, t0, 38, .9)
            # a fixed chop pattern, so the beat stays steady and readable; it repeats every orchestral bar
            if sec == 'breakA':
                pat = list(range(16)) + [16, 17, 18, 19, 20, 21, 22, 23, 8, 9, 10, 11, 12, 13, 12, 15]
            else:   # B: a bit busier, same idea (re-ordered kicks and snares, still a steady groove)
                pat = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 2, 3, 4, 5, 22, 23, 8, 9, 26, 27, 12, 29, 12, 15]
            for k in range(32):
                sl = slices[pat[k]]
                # small variations only on the last beat of a bar, never more than a stutter
                if k >= 28 and R.random() < (.25 if sec == 'breakA' else .45):
                    sl = slice_fx(slices[pat[k]], n, 'roll', 2)
                put(t0 + k * st, sl)
            if i % 4 == 3 and not (sec == 'breakA' and i == 7):   # short snare roll ends each 4-bar phrase (not the bar before part B)
                for k2, div in ((30, 2), (31, 4)): put(t0 + k2 * st, slice_fx(slices[12], n, 'roll', div), .75)
            # distorted sub on the chord root, half-time pattern
            for s16, L in ((0, 12), (12, 4), (20, 12)):
                N = int(L * st * .97 * SR); e = env(L * st * .97, .004, .3, .9, .03)[:N]
                x = np.tanh(sine(mtof(root - 12 if root > 43 else root), len(e)) * (2.5 if sec == 'breakA' else 4.)) * e
                M.add('sub', t0 + s16 * st, lp(x, 900) * .5)
            # the theme rides on top: strings in A, horns join in B
            for s, nn, L in theme[i]:
                violins(M, t0 + s * q, nn, L * q * .97, .6, att=.06, bus='lead')
                if sec == 'breakB': horn(M, t0 + s * q, nn - 12, L * q * .97, .75); violins(M, t0 + s * q, nn + 12, L * q * .97, .3, att=.06, bus='lead')
            if sec == 'breakB' and i == 0: cymbal(M, t0, .6)
            if sec == 'breakB' and i == 7:   # tape stop: the breaks slow down and sink away
                for j, k2 in enumerate(range(16, 32)): put(t0 + k2 * st, slice_fx(slices[k2], n, 'pitch', max(.25, .85 - .04 * j)), .8 * (1 - j / 18))
        # ---------------- the way home ----------------
        if sec == 'return':
            if i == 0: cymbal(M, t0, .35); timpani(M, t0, 38, .5)
            for s, nn, L in theme[i]: oboe(M, t0 + s * q, nn, L * q * .97, 1.1, pan=.15); violins(M, t0 + s * q, nn, L * q * .97, .35, att=.15, bus='lead')
            if i < 2:   # a last echo of the breaks, far away
                for k in (0, 8, 16, 24): put(t0 + k * st, slice_fx(slices[k], n, None), .12 * (1 - i * .5))
        if sec == 'end':
            mel = [[(0, 79, 2), (2, 77, 1), (3, 74, 1)], [(0, 73, 4)], [(0, 74, 4)], [(0, 78, 4)]][i]   # ends on F#: D major
            for s, nn, L in mel:
                violins(M, t0 + s * q, nn, L * q * (1.6 if i == 3 else .97), .8, att=.15, bus='lead')
                horn(M, t0 + s * q, nn - 12, L * q * (1.6 if i == 3 else .97), .85)
            if i == 1: roll(M, t0, 45, OB, .3)
            if i == 3:
                for nn in (38, 50, 57, 62, 66, 69, 74): violins(M, t0, nn, OB * 2.2, .7, att=.5)
                timpani(M, t0, 38, .5); cymbal(M, t0, .3); glock(M, t0 + q, 86, .25); harp(M, t0, 50, .6); harp(M, t0 + .08, 57, .5); harp(M, t0 + .16, 62, .5); harp(M, t0 + .24, 66, .5)
    render_hall(M, 'Shattered_Overture',
                sends={'str': .45, 'low': .3, 'lead': .4, 'wind': .45, 'horn': .45, 'harp': .4, 'drums': .3, 'perc': .4, 'glock': .5, 'break': .06, 'fx': .25},
                levels={'str': .9, 'low': .8, 'lead': .85, 'wind': 1., 'horn': .9, 'harp': .8, 'drums': .9, 'perc': .7, 'glock': .7, 'break': .9, 'sub': .85, 'fx': .7})

if __name__ == '__main__':
    {'16': shattered_overture}[sys.argv[1]]()
