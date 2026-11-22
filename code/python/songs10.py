"""python songs10.py cortis -> Off the Lines (hype rage/trap, in the style of CORTIS' REDRED / GO! / FaSHioN)
python songs10.py kaze   -> Breeze in the Alley (piano-led J-pop soul with trap touches, in the style of Fujii Kaze)"""
import sys
from songs import render, sections_to_bars, piano
from songs5 import violins
from breakcore_engine import chord, b808
from songs9 import organ
from instruments2 import *

# ---------------- hype instruments ----------------
def rage_lead(M, t, n, dur, vol, bus='lead'):
    N = int((dur + .05) * SR); tt = tarr(N); x = np.zeros(N)
    bend = -1. * np.exp(-tt / .03)                         # quick scoop up into each note
    for d in (-.32, -.2, -.08, .08, .2, .32, 0): x += saw(mtof(n + d + bend), N)
    x = np.tanh(x * 1.1); x = lp(hp(x, 200), 6500)
    M.add(bus, t, x * envN(N, dur, .002, .2, .85, .03) * vol * .22)
def heavy808(M, t, n, dur, vol, glide=None):
    N = int((dur + .05) * SR); tt = tarr(N); f = mtof(n) * (1 + 1.4 * np.exp(-tt / .012))
    if glide is not None: f = f * 2 ** (((glide - n) * np.exp(-tt / .07)) / 12)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR); x = np.tanh(x * 3.2) * envN(N, dur, .002, .6, .9, .04)
    M.add('sub', t, lp(x, 1500) * vol)
def trap_hats(M, t0, st, roll=False, v=1.):
    for k in range(0, 16, 2): hat(M, t0 + k * st, (.35 if k % 4 == 0 else .25) * v)
    if roll:   # hi-hat roll: triplets then 32nds on the last beat
        for j in range(3): hat(M, t0 + 12 * st + j * (4 * st / 3) / 2, .22 * v)
        for j in range(8): hat(M, t0 + 14 * st + j * st / 4, (.15 + .02 * j) * v)
def hey(M, t, vol=1.):   # crowd-style 'hey!' shout, made from noise + vowel formants
    N = int(.22 * SR); tt = tarr(N); env_ = np.clip(tt / .01, 0, 1) * np.exp(-tt / .07)
    src = saw(180 * (1 - .15 * tt / tt[-1]), N) * .6 + noise(N) * .5
    y = 1.4 * bp(src, 500, 800) + 1.0 * bp(src, 1600, 2200) + .4 * bp(src, 2600, 3200)
    M.add('fx', t, y * env_ * vol * .8, pan=-.25); M.add('fx', t + .012, y * env_ * vol * .6, pan=.25)
def chant(M, t, n, vol=1.):   # short sung 'go' syllable
    voice(M, 'chant', t, n, .12, vol)

# =====================================================================
# OFF THE LINES (hype) — 150 BPM half-time trap / rage
# =====================================================================
def cortis_hype():
    bpm = 150; st = 60 / bpm / 4; B = 16 * st
    riff = [[(0, 78, 2), (2, 78, 1), (3, 81, 2), (6, 78, 2), (8, 85, 3), (11, 83, 1), (12, 81, 2), (14, 78, 2)],
            [(0, 76, 2), (2, 76, 1), (3, 78, 2), (6, 81, 2), (8, 83, 4), (12, 81, 2), (14, 76, 2)]]
    roots = [42, 42, 38, 40]   # F#, F#, D, E (bass)
    secs = [('intro', 4), ('build', 4), ('drop', 16), ('switch', 8), ('build2', 2), ('drop2', 16), ('outro', 2)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B + 4); prev = None
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; root = roots[i % 4]
        # the riff
        if sec in ('intro', 'build', 'drop', 'drop2', 'build2', 'outro'):
            lv = {'intro': .5, 'build': .7, 'build2': .8, 'drop': 1., 'drop2': 1., 'outro': .6}[sec]
            for s, nn, L in riff[i % 2]:
                rage_lead(M, t0 + s * st, nn, L * st * .95, lv, bus='lead' if sec not in ('intro', 'build') else 'leadf')
                if sec == 'drop2': rage_lead(M, t0 + s * st, nn - 12, L * st * .95, .55)
        # drums + 808
        if sec in ('drop', 'drop2'):
            if i == 0: crash(M, t0, .9); impact(M, t0, 1.)
            for s in ((0, 7, 10) if i % 2 == 0 else (0, 3, 10, 14)): kick(M, t0 + s * st, .9, punch=1.3)
            snare(M, t0 + 8 * st, .9); clap(M, t0 + 8 * st, .8)
            trap_hats(M, t0, st, roll=(i % 2 == 1))
            if i % 4 == 2: hey(M, t0 + 8 * st, 1.)
            for s, L, gl in ((0, 6, prev), (6, 2, None), (10, 4, None), (14, 2, root + 12)):
                heavy808(M, t0 + s * st, root if s != 14 else root + 12, L * st * .95, .75, glide=gl if s in (0, 14) else None)
            prev = root
            if sec == 'drop2' and i % 4 == 3:
                for s in (12, 13, 14, 15): snare(M, t0 + s * st, .5)
        if sec in ('build', 'build2'):
            kick(M, t0, .7)
            div = [4, 2, 1, .5][min(i, 3)] if sec == 'build' else [1, .5][i]
            for s in np.arange(0, 16, div): snare(M, t0 + s * st, .3 + .08 * i + .015 * s)
            trap_hats(M, t0, st, roll=True, v=.8)
            if i == 0: riser(M, t0, (4 if sec == 'build' else 2) * B, .7)
        if sec == 'switch':   # beat switch: lighter, bouncier lo-fi trap with a 'go, go, go' chant
            ch_ = [chord('F#m7'), chord('Dmaj7'), chord('Bm7'), chord('C#m7')][i % 4]
            for s in (0, 3, 6, 10):
                for j, c in enumerate(ch_[0]): epiano(M, 'keys', t0 + s * st + j * .005, c + 12, st * 2.2, .08, pan=(j - 1.5) * .2)
            for s in (0, 10): kick(M, t0 + s * st, .75)
            snare(M, t0 + 8 * st, .7); trap_hats(M, t0, st, roll=(i % 2 == 1), v=.8)
            b808(M, t0, ch_[1], 6 * st, .55); b808(M, t0 + 10 * st, ch_[1], 4 * st, .45)
            for k, nn in enumerate([73, 73, 73, 76, 73, 73, 78, 76]): chant(M, t0 + k * 2 * st, nn, .55 if k % 2 == 0 else .4)
            if i == n - 1: hey(M, t0 + 12 * st, 1.); hey(M, t0 + 14 * st, 1.)
        if sec == 'intro':
            N = int(B * SR); d = np.zeros(N); pos = rng.integers(0, N, 8); d[pos] = rng.uniform(-.5, .5, 8); M.add('fx', t0, lp(d, 5000) * .3)
        if sec == 'outro' and i == n - 1:
            heavy808(M, t0, 42, 2.5, .7); hey(M, t0, 1.)
    # intro/build riff is muffled, then opens at the drop
    if 'leadf' in M.buses: M.buses['leadf'] = np.array([lp(c, 1200) for c in M.buses['leadf']])
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .2, taps=3)
    render(M, 'Off_the_Lines_hype_150bpm', sends={'lead': .15, 'leadf': .2, 'keys': .3, 'chant': .3, 'fx': .2, 'drums': .05},
           levels={'lead': 1., 'leadf': 1.3, 'lead_d': .25, 'keys': 1., 'chant': 1., 'sub': 1., 'drums': 1., 'fx': .9}, duck=('lead',), fade=0.)

# =====================================================================
# BREEZE IN THE ALLEY — 98 BPM piano-led J-pop soul (Fujii Kaze style)
# =====================================================================
def kaze_style():
    bpm = 98; st = 60 / bpm / 4; B = 16 * st; sw = .12 * st
    S = lambda k: k * st + (sw if k % 2 else 0)
    V = ['Amaj9', 'G#m7', 'C#m9', 'F#m7', 'Dmaj9', 'C#m7', 'Bm7', 'E7sus']
    PRE = ['Bm7', 'C#m7', 'Dmaj9', 'E7sus']
    CH = ['Dmaj9', 'E7', 'C#m7', 'F#m7', 'Bm7', 'E7', 'Amaj9', 'Amaj9']
    vm = [[(0, 76, 4), (4, 76, 2), (6, 78, 2), (8, 80, 6), (14, 78, 2)], [(0, 75, 4), (4, 71, 4), (8, 75, 2), (10, 78, 2), (12, 80, 4)],
          [(0, 80, 6), (6, 78, 2), (8, 76, 4), (12, 73, 4)], [(0, 73, 6), (8, 76, 2), (10, 78, 2), (12, 81, 4)],
          [(0, 81, 6), (6, 80, 2), (8, 78, 4), (12, 76, 4)], [(0, 76, 4), (4, 73, 4), (8, 76, 2), (10, 80, 2), (12, 83, 4)],
          [(0, 81, 4), (4, 78, 4), (8, 74, 4), (12, 76, 4)], [(0, 76, 12)]]
    pm = [[(0, 74, 4), (4, 76, 4), (8, 78, 8)], [(0, 76, 4), (4, 78, 4), (8, 80, 8)], [(0, 78, 4), (4, 80, 4), (8, 81, 8)], [(0, 83, 16)]]
    cm = [[(0, 81, 2), (2, 81, 2), (4, 83, 4), (8, 85, 6), (14, 83, 2)], [(0, 83, 4), (4, 80, 4), (8, 78, 4), (12, 80, 4)],
          [(0, 80, 2), (2, 80, 2), (4, 81, 4), (8, 83, 4), (12, 85, 4)], [(0, 85, 8), (8, 83, 4), (12, 81, 4)],
          [(0, 81, 2), (2, 81, 2), (4, 83, 4), (8, 85, 6), (14, 86, 2)], [(0, 88, 6), (6, 86, 2), (8, 83, 4), (12, 80, 4)],
          [(0, 81, 12)], []]
    secs = [('intro', 4), ('verse', 8), ('pre', 4), ('chorus', 8), ('verse', 8), ('pre', 4), ('chorus', 8), ('bridge', 4), ('chorus', 8), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B + 6)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B
        name = {'intro': V, 'verse': V, 'pre': PRE, 'chorus': CH, 'bridge': PRE, 'outro': ['Amaj9'] * 4}[sec][i % (8 if sec in ('verse', 'chorus', 'intro') else 4)]
        tones, root = chord(name)
        # piano: the heart of it. Soulful pushes on the 'and', left-hand bass notes
        if sec in ('intro', 'outro', 'bridge'):
            piano(M, 'piano', t0, root, B * 1.1, .6, pan=-.2)
            for k, ix in enumerate([0, 1, 2, 3, 2, 1, 2, len(tones) - 1]): piano(M, 'piano', t0 + S(k * 2), tones[ix % len(tones)] + 12, 2 * st * 3, .4, pan=.1)
        else:
            piano(M, 'piano', t0, root, 7 * st, .6, pan=-.2); piano(M, 'piano', t0 + S(10), root + 12, 5 * st, .4, pan=-.2)
            for s in (0, 3, 6, 10, 14):
                for j, c in enumerate(tones): piano(M, 'piano', t0 + S(s) + j * .006, c + 12 if c < 60 else c, st * (2.5 if s in (0, 6) else 1.4), .26, pan=(j - 1.5) * .15)
        # groove: soft trap-ish hats + half-time kick/snare in verses, fuller in chorus
        if sec in ('verse', 'pre', 'chorus', 'bridge'):
            full = sec == 'chorus'
            for s in ((0, 7, 10) if full else (0, 10)): kick(M, t0 + S(s), .75 if full else .6, punch=.9)
            snare(M, t0 + S(8 if not full else 4), .55); snare(M, t0 + S(12), .55) if full else None
            if full: clap(M, t0 + S(4), .45); clap(M, t0 + S(12), .45)
            for k in range(16): hat(M, t0 + S(k), (.22 if k % 2 == 0 else .12) * (1 if full else .8))
            if sec == 'verse' and i % 2 == 1:
                for j in range(6): hat(M, t0 + 14 * st + j * st / 3, .12)
        # bass (warm, follows the left hand)
        if sec not in ('intro', 'outro'):
            for s, o, L in ((0, 0, 6), (6, 12, 2), (8, 7, 2), (10, 0, 4), (14, 12, 2)): fbass(M, t0 + S(s), (root if root < 44 else root - 12) + o, L * st * .9, .6)
        # electric piano + gospel organ in the chorus, strings swell in pre and chorus
        if sec in ('verse',):
            for s in (2, 9):
                for c in tones[1:]: epiano(M, 'keys', t0 + S(s), c + 12, st * 1.5, .05)
        if sec == 'chorus':
            for c in tones: organ(M, t0, c + 12, B * .97, .45, pan=.25)
        if sec in ('pre', 'chorus'):
            for j, c in enumerate(tones[1:]): violins(M, t0, c + 12, B * .98, .35, att=.3 if sec == 'pre' else .15, pan=(j - 1) * .3)
        # the vocal line (singing synth), doubled by piano in the chorus
        mel = {'verse': vm, 'pre': pm, 'chorus': cm}.get(sec)
        if mel:
            for s, nn, L in mel[i % len(mel)]:
                voice(M, 'vox', t0 + S(s), nn, L * st * .95, .75)
                if sec == 'chorus': piano(M, 'piano', t0 + S(s), nn + 12, L * st, .25, pan=.2)
        if sec == 'bridge':   # piano takes a flowing run up the scale
            for k, nn in enumerate([69, 71, 73, 76, 78, 80, 81, 83, 85, 88, 85, 83, 81, 80, 78, 76]): piano(M, 'piano', t0 + S(k), nn + (i % 2) * 2, st * 2, .32, pan=.2)
        if sec == 'outro' and i == n - 1:
            for j, nn in enumerate([45, 57, 64, 68, 71, 73, 76, 80]): piano(M, 'piano', t0 + B + j * .05, nn, 4., .45)
    M.buses['vox_d'] = pingpong(M.buses['vox'], 3 * st, .25)
    render(M, 'Breeze_in_the_Alley_98bpm', sends={'piano': .25, 'keys': .3, 'organ': .3, 'str': .4, 'vox': .3, 'drums': .05},
           levels={'piano': 1., 'keys': .8, 'organ': .6, 'str': .7, 'vox': 1.1, 'vox_d': .3, 'bass': .85, 'drums': .8}, duck=(), fade=0.)

if __name__ == '__main__':
    {'cortis': cortis_hype, 'kaze': kaze_style}[sys.argv[1]]()
