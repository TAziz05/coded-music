"""K-pop-inspired originals (instrumental; melodies are original, only the style is borrowed).
python songs9.py bts     -> Golden Hour Groove (BTS-style disco-pop)
python songs9.py txt     -> Blue Spark Runaway (TXT-style emo pop-punk with dreamy synths)
python songs9.py cortis  -> Off the Lines (CORTIS-style boom-bap with a 60s psychedelic guitar riff)"""
import sys
from songs import render, sections_to_bars, ride, piano
from songs3 import bars8, play
from songs4 import dist_gtr, power, lead_gtr
from songs5 import violins
from instruments2 import *

def chick(M, t, notes, vol, pan=.4):   # muted 'chicken-scratch' funk guitar
    L = int(.12 * SR); y = np.zeros(L)
    for j, n in enumerate(notes):
        k = ks(mtof(n), .08, .7, .97); o = int(j * .003 * SR); y[o:o + len(k)] += k[:L - o]
    M.add('gtr', t, hp(y, 300) * np.exp(-tarr(L) / .03) * vol, pan=pan)
def octbass(M, t, n, dur, vol):
    N = int((dur + .04) * SR); x = saw(mtof(n), N) * .5 + sqr(mtof(n), N, .5) * .3 + sine(mtof(n), N) * .6
    lo = lp(x, 300); y = lo + (lp(x, 1600) - lo) * np.exp(-tarr(N) / .06)
    M.add('bass', t, y * envN(N, dur, .003, .15, .7, .03) * vol)
def organ(M, t, n, dur, vol, pan=0.):
    N = int((dur + .1) * SR); tt = tarr(N); x = sine(mtof(n), N) + .5 * sine(2 * mtof(n), N) + .3 * sqr(mtof(n), N, .5) * .3 + .25 * sine(3 * mtof(n), N)
    x *= 1 + .15 * np.sin(2 * np.pi * 6.5 * tt)   # leslie-ish wobble
    M.add('organ', t, lp(x, 2500) * envN(N, dur, .01, .1, 1., .06) * vol * .25, pan=pan)
def fuzz_riff(M, t, n, dur, vol):
    N = int((dur + .1) * SR); y = ks(mtof(n), dur + .05, .6, .9985)[:N]
    tt = tarr(len(y)); y = np.tanh(y * 4.5) * .5
    y = lp(hp(y, 100), 3800) * (1 + .45 * np.sin(2 * np.pi * 6 * (tt + t)))   # fuzz + tremolo
    M.add('riff', t, y * envN(len(y), dur, .002, .3, .9, .04) * vol, pan=-.15)
def boom_kick(M, t, v=1.):
    N = int(.5 * SR); tt = tarr(N); f = 42 + 90 * np.exp(-tt / .05)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .3) + lp(noise(N), 3000) * np.exp(-tt / .006) * .4
    M.add('drums', t, np.tanh(x * 2) * v * .9); M.kicks.append(t)
def boom_snare(M, t, v=1.):
    N = int(.4 * SR); tt = tarr(N)
    x = bp(noise(N), 900, 7000) * np.exp(-tt / .16) + np.sin(2 * np.pi * np.cumsum(200 + 50 * np.exp(-tt / .02)) / SR) * np.exp(-tt / .08) * .7
    M.add('drums', t, np.tanh(x * 1.6) * v * .8)
def scratch(M, t, vol=1.):
    N = int(.35 * SR); tt = tarr(N); x = noise(N); out = np.zeros(N); c = int(.035 * SR)
    for i in range(0, N, c):
        fc = 600 + 1800 * (.5 + .5 * np.sin(2 * np.pi * i / SR * 11)); seg = bp(x[i:i + c], fc * .6, fc * 1.4); out[i:i + len(seg)] = seg
    M.add('fx', t, out * (np.abs(np.sin(2 * np.pi * 6 * tt)) ** .5) * vol * .5)

# =====================================================================
# GOLDEN HOUR GROOVE — 114 BPM disco-pop (BTS style)
# =====================================================================
def golden_hour():
    bpm = 114; st = 60 / bpm / 4; B = 16 * st
    C = {'Bbmaj7': ([58, 62, 65, 69], 46), 'Dm7': ([57, 60, 62, 65], 38), 'Gm7': ([58, 62, 65, 67], 43), 'F': ([57, 60, 65, 69], 41), 'Cm7': ([58, 60, 63, 67], 48), 'Ebmaj7': ([58, 62, 63, 67], 39)}
    prog = ['Bbmaj7', 'Dm7', 'Gm7', 'F']; bridge = ['Ebmaj7', 'Dm7', 'Cm7', 'F']
    hook = bars8([[74,-1,72,70,-1,74,-1,77],[77,-1,74,72,-1,69,-1,-1],[70,-1,72,74,-1,77,-1,79],[77,-1,-1,-1,72,-1,74,-1],
                  [74,-1,72,70,-1,74,-1,77],[81,-1,79,77,-1,74,-1,-1],[79,-1,77,74,-1,72,-1,70],[72,-1,-1,-1,0,0,0,0]])
    verse = bars8([[65,-1,65,67,-1,69,-1,0],[69,-1,69,70,-1,72,-1,0],[70,-1,69,67,-1,65,-1,62],[65,-1,-1,-1,0,0,0,0]] * 2)
    secs = [('intro', 4), ('verse', 8), ('pre', 4), ('chorus', 8), ('verse', 8), ('chorus', 8), ('bridge', 4), ('chorus', 8), ('outro', 2)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B + 4); nch = 0
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B
        if sec == 'chorus' and i == 0: nch += 1
        up = 1 if nch == 3 and sec in ('chorus', 'outro') else 0
        name = (bridge if sec == 'bridge' else prog)[i % 4]; v, root = C[name]; v = [x + up for x in v]; root += up
        full = sec in ('chorus',)
        # strings: swell in intro/pre, sustained in chorus, a glissando into every chorus
        if sec in ('intro', 'pre', 'chorus', 'bridge'):
            for j, nn in enumerate(v[1:]): violins(M, t0, nn + 12, B * .98, .5 if full else .4, att=.4 if sec != 'chorus' else .15, pan=(j - 1) * .3)
        if sec == 'pre' and i == n - 1:
            for j, nn in enumerate(range(70, 94, 2)): violins(M, t0 + 8 * st + j * .06, nn, .12, .35, att=.01, bus='lead')
        # funk guitar 16th offbeat scratches + piano stabs
        if sec != 'intro' or i >= 2:
            for k in range(16):
                if k % 4 in (1, 2, 3) and (k % 2 == 1 or full): chick(M, t0 + k * st, v[1:] + [v[1] + 12], .16 if k % 2 else .1)
        if sec in ('verse', 'chorus', 'bridge'):
            for s in (0, 6, 10):
                for c in v: piano(M, 'keys', t0 + s * st, c, st * 1.5, .25)
        # drums: four-on-the-floor, claps, open hats on the offbeat
        if sec in ('verse', 'pre', 'chorus') or (sec == 'outro'):
            for k in range(4): kick(M, t0 + k * 4 * st, .85)
            clap(M, t0 + 4 * st, .7); clap(M, t0 + 12 * st, .7); snare(M, t0 + 4 * st, .35); snare(M, t0 + 12 * st, .35)
            for k in range(16):
                if k % 4 == 2: hat(M, t0 + k * st, .45, open_=True)
                elif k % 2 == 0: hat(M, t0 + k * st, .25)
                elif full: hat(M, t0 + k * st, .14)
            if i == 0 and sec == 'chorus': crash(M, t0, .7)
            if i == n - 1 and sec in ('verse', 'pre'):
                for s in (12, 13, 14, 15): snare(M, t0 + s * st, .4)
        if sec == 'bridge':
            for s in (4, 12): clap(M, t0 + s * st, .8)
            for k in range(0, 16, 2): hat(M, t0 + k * st, .2)
        # octave disco bass
        if sec not in ('intro',):
            for k in range(8): octbass(M, t0 + k * 2 * st, root - 12 + (12 if k % 2 else 0), 2 * st * .7, .7)
        # melody: soft lead in verses, brass + lead on the hook
        if sec == 'verse': play(verse, i, t0, st, lambda t, nn, d: leadsq(M, 'lead', t, nn + up, d * .92, .5))
        if sec == 'chorus':
            play(hook, i, t0, st, lambda t, nn, d: brass(M, 'brass', t, nn + up, d * .92, .45))
            play(hook, i, t0, st, lambda t, nn, d: brass(M, 'brass', t, nn + up - 12, d * .92, .3, pan=.2))
            play(hook, i, t0, st, lambda t, nn, d: leadsq(M, 'lead', t, nn + up + 12, d * .9, .18))
        if sec == 'outro' and i == n - 1:
            for c in v: brass(M, 'brass', t0, c + 12, B, .3)
            crash(M, t0, .6)
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .25)
    render(M, 'Golden_Hour_Groove_114bpm', sends={'str': .35, 'lead': .2, 'brass': .25, 'keys': .15, 'gtr': .1, 'drums': .05, 'fx': .25},
           levels={'str': .8, 'lead': .9, 'lead_d': .3, 'brass': 1., 'keys': .7, 'gtr': .9, 'bass': .9, 'drums': .95, 'fx': .7}, duck=('str',), fade=0.)

# =====================================================================
# BLUE SPARK RUNAWAY — 160 BPM emo pop-punk with dreamy synths (TXT style)
# =====================================================================
def blue_spark():
    bpm = 160; st = 60 / bpm / 4; B = 16 * st
    C = [('Bm', [59, 62, 66], 35), ('G', [59, 62, 67], 43), ('D', [57, 62, 66], 38), ('A', [57, 61, 64], 45)]
    ch_m = bars8([[78,-1,78,81,-1,78,76,74],[74,-1,-1,71,-1,74,76,-1],[78,-1,78,81,-1,83,81,78],[76,-1,-1,-1,73,-1,74,76],
                  [78,-1,78,81,-1,83,85,-1],[86,-1,85,83,-1,81,79,-1],[78,-1,81,-1,78,-1,74,76],[76,-1,-1,-1,-1,-1,0,0]])
    vs_m = bars8([[71,-1,71,74,-1,71,69,-1],[67,-1,67,71,-1,74,-1,-1],[69,-1,69,74,-1,78,-1,76],[76,-1,-1,-1,0,0,0,0]] * 2)
    secs = [('intro', 4), ('verse', 8), ('pre', 4), ('chorus', 8), ('verse', 8), ('pre', 4), ('chorus', 8), ('bridge', 8), ('chorus', 8), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B + 4)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; name, v, root = C[i % 4]
        r2 = root if root < 44 else root - 12
        # dreamy layer: shimmering synth arps + pad everywhere
        arp = v + [v[0] + 12, v[1] + 12, v[2] + 12]
        for k in range(16): pluck(M, 'syn', t0 + k * st, arp[[0, 2, 4, 1, 3, 5, 4, 2][k % 8]] + 12, st * .9, .07 if sec == 'chorus' else .1, pan=(-.5, .5)[k % 2], dec=.09)
        for nn in v: supersaw(M, 'pad', t0, nn + 12, B, .05, cut=1600, a=.3, r=.5, voices=3)
        # guitars: clean picking in verses, crunch power chords in pre/chorus
        if sec in ('verse', 'intro', 'bridge'):
            for k in range(8): guitar(M, 'gtr', t0 + k * 2 * st, (v + [v[0] + 12])[[0, 1, 2, 3, 2, 1, 2, 3][k]], 2 * st * 2.5, .35, pan=-.4, bright=.55)
        if sec in ('pre', 'chorus'):
            pc = power(r2 + 12)
            for s, L in ((0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)) if sec == 'chorus' else ((0, 4), (4, 4), (8, 4), (12, 4)):
                dist_gtr(M, 'gtrL', t0 + s * st, pc, L * st * .92, .3, pan=-.65, gain=3.5, warm=True); dist_gtr(M, 'gtrR', t0 + s * st + .007, pc, L * st * .92, .3, pan=.65, gain=3.5, warm=True)
        # drums: half-time verse, punk beat chorus, building pre
        if sec == 'verse':
            kick(M, t0, .8); kick(M, t0 + 10 * st, .6); snare(M, t0 + 8 * st, .75)
            for k in range(0, 16, 2): hat(M, t0 + k * st, .25)
        elif sec == 'pre':
            for s in (0, 8): kick(M, t0 + s * st, .85)
            for s in range(0, 16, 4 if i < 2 else 2 if i < 3 else 1): snare(M, t0 + s * st, .3 + .1 * i)
        elif sec == 'chorus':
            if i == 0: crash(M, t0, .8)
            for s in (0, 6, 8, 10): kick(M, t0 + s * st, .9)
            for s in (4, 12): snare(M, t0 + s * st, .85)
            for k in range(8): ride(M, t0 + k * 2 * st, .5)
            if i == n - 1:
                for s, nn in zip(range(10, 16), (52, 52, 48, 48, 43, 43)): tom(M, t0 + s * st, nn, .6)
        elif sec == 'bridge':
            kick(M, t0, .7)
            if i >= 4: snare(M, t0 + 8 * st, .6)
        # bass
        if sec not in ('intro',):
            for k in range(8 if sec != 'bridge' else 2): fbass(M, t0 + k * (2 if sec != 'bridge' else 8) * st, r2, (2 if sec != 'bridge' else 8) * st * .9, .55)
        # melody: soft synth 'voice' in verses, lead guitar + bright synth in chorus
        if sec == 'verse': play(vs_m, i, t0, st, lambda t, nn, d: voice(M, 'lead', t, nn, d * .92, .7))
        if sec == 'chorus':
            play(ch_m, i, t0, st, lambda t, nn, d: lead_gtr(M, t, nn, d * .95, .4, gain=2.8, warm=True))
            play(ch_m, i, t0, st, lambda t, nn, d: supersaw(M, 'lead', t, nn + 12, d * .9, .07, cut=4000, a=.01, r=.12, voices=5))
        if sec == 'bridge' and i % 2 == 0: voice(M, 'lead', t0, [78, 79, 81, 79][i // 2 % 4], 2 * B * .9, .6)
        if sec == 'outro':
            for k in range(8): guitar(M, 'gtr', t0 + k * 2 * st, (v + [v[0] + 12])[[0, 1, 2, 3, 2, 1, 2, 3][k]], 2 * st * 2.5, .3 * (1 - i / 5), pan=-.4)
            if i == n - 1:
                for j, nn in enumerate([47, 54, 59, 62, 66]): guitar(M, 'gtr', t0 + B + j * .04, nn, 3., .3)
    M.buses['gtr'] = chorus(M.buses['gtr'], mix=.3); M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .3)
    render(M, 'Blue_Spark_Runaway_160bpm', sends={'syn': .35, 'pad': .45, 'gtr': .2, 'lead': .3, 'drums': .05, 'fx': .2},
           levels={'syn': .8, 'pad': .7, 'gtr': .9, 'gtrL': 2.0, 'gtrR': 2.0, 'lead': 1.5, 'lead_d': .4, 'bass': .85, 'drums': .8, 'fx': .6}, duck=('pad', 'syn'), fade=0.)

# =====================================================================
# OFF THE LINES — 92 BPM boom-bap + 60s psychedelic guitar riff (CORTIS style)
# =====================================================================
def off_the_lines():
    bpm = 92; st = 60 / bpm / 4; B = 16 * st; sw = .18 * st
    S = lambda k: k * st + (sw if k % 2 else 0)
    riff = [[(0, 52, 2), (3, 55, 1), (4, 57, 2), (6, 59, 2), (8, 62, 3), (11, 59, 1), (12, 57, 2), (14, 55, 2)],
            [(0, 52, 3), (3, 52, 1), (4, 55, 2), (6, 57, 1), (7, 58, 1), (8, 57, 4), (12, 55, 2), (14, 57, 2)]]
    hookm = bars8([[76,-1,76,79,-1,76,74,-1],[74,-1,74,78,-1,74,72,-1],[71,-1,74,-1,76,-1,79,-1],[76,-1,-1,-1,0,0,0,0]] * 2)
    A_ch = [(40, [52, 55, 59, 62]), (40, [52, 55, 59, 62]), (45, [55, 57, 61, 64]), (45, [55, 57, 61, 64])]   # Em7 Em7 A7 A7
    H_ch = [(36, [55, 60, 64, 67]), (38, [57, 62, 66, 69]), (40, [55, 59, 64, 67]), (40, [55, 59, 64, 67])]   # C D Em Em
    secs = [('intro', 4), ('A', 16), ('hook', 8), ('A', 8), ('hook', 8), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B + 4)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B
        root, v = (H_ch if sec == 'hook' else A_ch)[i % 4]
        tr = 0 if root == 40 else (root - 40) if sec != 'hook' else root - 40
        # the riff: fuzzy, wobbling 60s guitar (moves with the chord)
        rv = .5 if sec in ('intro', 'outro') else .42
        if sec == 'outro': rv *= (1 - i / 5)
        for s, nn, L in riff[i % 2]: fuzz_riff(M, t0 + S(s), nn + tr, L * st * .95, rv)
        # organ bed
        if sec in ('A', 'hook'):
            for nn in v: organ(M, t0, nn, B * .97, .5 if sec == 'hook' else .3, pan=.25)
        # boom-bap drums
        if sec in ('A', 'hook'):
            for s in (0, 7, 10): boom_kick(M, t0 + S(s), 1. if s == 0 else .8)
            if i % 2: boom_kick(M, t0 + S(15), .5)
            for s in (4, 12): boom_snare(M, t0 + S(s), 1.)
            for k in range(0, 16, 2): hat(M, t0 + S(k), .35 if k % 4 == 2 else .22)
            hat(M, t0 + S(14), .3, open_=True)
            if i % 4 == 3: scratch(M, t0 + S(12), .8)
        if sec == 'intro' and i == n - 1: scratch(M, t0 + S(8), .9); scratch(M, t0 + S(12), .7)
        # bass follows the riff's root
        if sec in ('A', 'hook'):
            for s, L in ((0, 3), (3, 1), (6, 2), (8, 4), (14, 2)): fbass(M, t0 + S(s), root - 12 if root > 40 else root, L * st * .9, .7)
        # hook: horn hits + organ melody
        if sec == 'hook':
            if i == 0: crash(M, t0, .6)
            for s in (0, 3, 6):
                for c in v[:3]: brass(M, 'brass', t0 + S(s), c + 12, st * 1.3, .2)
            play(hookm, i, t0, st, lambda t, nn, d: organ(M, t, nn, d * .95, 1.3, pan=-.1))
            play(hookm, i, t0, st, lambda t, nn, d: leadsq(M, 'lead', t, nn, d * .9, .25))
        if sec == 'outro' and i == n - 1: fuzz_riff(M, t0 + B, 52, 3., .45)
    M.buses['riff_d'] = pingpong(M.buses['riff'], 3 * st, .3, taps=3)
    render(M, 'Off_the_Lines_92bpm', sends={'riff': .25, 'organ': .2, 'brass': .2, 'lead': .2, 'drums': .06, 'fx': .2},
           levels={'riff': 1.2, 'riff_d': .3, 'organ': .8, 'brass': .9, 'lead': .8, 'bass': .9, 'drums': 1., 'fx': .8}, duck=(), fade=0.)

if __name__ == '__main__':
    {'bts': golden_hour, 'txt': blue_spark, 'cortis': off_the_lines}[sys.argv[1]]()
