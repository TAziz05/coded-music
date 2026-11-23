"""Sports songs (all sounds are code, including the whistles, balls, crowds and footsteps).
python sports.py all  (or: soccer basketball football baseball hockey tennis volleyball skiing badminton frisbee running jogging walking)
Running, jogging and walking are set to step cadences (about 176, 160 and 112 steps a minute), with a footstep on every beat."""
import sys
import numpy as np
from newstyles import *
from popkit import build, keys_bar, hey

# ---------------- sports sound effects ----------------
def whistle(M, t, dur=.35, vol=1.):        # referee's pea whistle: a trill around 3 kHz
    N = int(dur * SR); tt = tarr(N); f = 3000 + 120 * np.sign(np.sin(2 * np.pi * 28 * tt))
    M.add('fx', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * envN(N, dur, .01, .05, .9, .05) * vol * .1)
def crowd(M, t, dur=2., vol=1., swell=True):
    N = int(dur * SR); tt = tarr(N); x = bp(noise(N), 300, 3000) + .5 * bp(noise(N), 800, 1600) * (1 + .3 * np.sin(2 * np.pi * 3 * tt))
    e = np.sin(np.pi * tt / dur) if swell else np.exp(-tt / (dur * .5)); M.add('fx', t, x * e * vol * .12)
def claps(M, t, vol=1.):                    # a crowd clap: many hands slightly apart
    for k in range(8): clap(M, t + rng.uniform(0, .025), .12 * vol)
def ball_bounce(M, t, vol=1.):              # basketball on hardwood
    N = int(.18 * SR); tt = tarr(N); f = 110 * (1 + .6 * np.exp(-tt / .01))
    M.add('perc', t, (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .05) + bp(noise(N), 1500, 4000) * np.exp(-tt / .004) * .4) * vol * .5)
def squeak(M, t, vol=1.):                   # sneaker squeak
    N = int(.09 * SR); tt = tarr(N); f = 2200 + 900 * np.sin(np.pi * tt / tt[-1])
    M.add('fx', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) * vol * .07, pan=rng.uniform(-.5, .5))
def buzzer(M, t, dur=1.2, vol=1.):          # scoreboard buzzer / goal horn
    N = int(dur * SR); x = sqr(220, N) + sqr(277, N) * .7; M.add('fx', t, lp(x, 1800) * envN(N, dur, .01, .1, .9, .1) * vol * .1)
def goal_horn(M, t, dur=2.2, vol=1.):
    N = int(dur * SR); x = sum(saw(f, N) for f in (98, 123.5, 147)); M.add('fx', t, np.tanh(lp(x, 900) * 1.5) * envN(N, dur, .05, .2, .9, .4) * vol * .12)
def bat_crack(M, t, vol=1.):
    N = int(.12 * SR); tt = tarr(N); M.add('perc', t, (bp(noise(N), 1500, 7000) * np.exp(-tt / .01) + np.sin(2 * np.pi * 900 * tt) * np.exp(-tt / .02) * .5) * vol * .6)
def pok(M, t, pan=0., vol=1., light=False):  # racket hitting a ball (light=True: a shuttlecock)
    N = int(.08 * SR); tt = tarr(N); f = 1500 if light else 700
    M.add('perc', t, (np.sin(2 * np.pi * f * tt) * np.exp(-tt / (.008 if light else .015)) + bp(noise(N), 2000, 6000) * np.exp(-tt / .003) * .5) * vol * .4, pan=pan)
def swoosh(M, t, dur=.6, vol=1., up=True):  # skis carving / a frisbee flying past
    N = int(dur * SR); tt = tarr(N); c = (800 + 3500 * tt / dur) if up else (4000 - 3000 * tt / dur)
    x = np.zeros(N); w = noise(N); lo, hi = lp(w, 1500), lp(w, 5000); m = np.clip((c - 800) / 4000, 0, 1); x = lo * (1 - m) + (hi - lo * .5) * m
    M.add('fx', t, x * np.sin(np.pi * tt / dur) * vol * .25, pan=(-.6 if up else .6))
def footstep(M, t, vol=1., soft=False):     # a step: heel thud + a bit of grit
    N = int(.1 * SR); tt = tarr(N); f = 70 * (1 + .5 * np.exp(-tt / .01))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .03) + bp(noise(N), 1000, 5000) * np.exp(-tt / .01) * (.15 if soft else .3)
    M.add('perc', t, x * vol * .45, pan=rng.uniform(-.15, .15))
def organ_charge(M, t, st, vol=1.):         # the stadium organ 'charge!' run: G C E G . E G
    for k, (s, n) in enumerate(((0, 67), (2, 72), (4, 76), (6, 79), (10, 76), (12, 79))): organ(M, t + s * st, n, st * (1.8 if k < 5 else 6), .55 * vol)
def oh_chant(M, t, st, tones, vol=1.):      # stadium 'oh-oh-oh' chant
    for s, d in ((0, 3), (4, 3), (8, 2), (10, 6)):
        for c in tones[:3]: voice(M, 'perc', t + s * st, c + 12, st * d * .95, .35 * vol)
def surdo(M, t, low=True, vol=1.):          # samba bass drum
    N = int(.4 * SR); tt = tarr(N); f = (60 if low else 80) * (1 + .3 * np.exp(-tt / .02))
    M.add('perc', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .18) * vol * .7)
def agogo(M, t, hi=True, vol=1.): cowbell(M, t, 84 if hi else 79, .12, .9 * vol)

# ---------------- drum styles ----------------
@D('samba')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 8): surdo(M, t0 + S(s), s == 8)
    for k in range(16): shaker(M, t0 + S(k), .45 if k % 4 == 2 else .25)
    for s, h in ((0, True), (3, False), (6, True), (8, False), (10, True), (13, False)): agogo(M, t0 + S(s), h, .6)
    for s in (4, 12): snare(M, t0 + S(s), .4)
    for s in (2, 7, 11, 15): rim(M, t0 + S(s), .5)
@D('drumline')
def _(M, t0, st, S, i, n, fill):            # marching-band snare line
    kick(M, t0, .9); kick(M, t0 + S(8), .8)
    for k in range(16): snare(M, t0 + S(k), .5 if k % 4 == 0 else (.25 if k % 2 == 0 else .12))
    for s in (4, 12): snare(M, t0 + S(s), .8)
    if i % 4 == 3:
        for j in range(8): snare(M, t0 + S(12) + j * st / 2, .2 + .06 * j)
@D('steps')                                 # light kit with a footstep on every beat (cadence songs)
def _(M, t0, st, S, i, n, fill):
    for s in (0, 4, 8, 12): footstep(M, t0 + S(s), .9)
    for s in (4, 12): snare(M, t0 + S(s), .5)
    for k in range(0, 16, 2): hat(M, t0 + S(k), .2)
@D('steps_dnb')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 4, 8, 12): footstep(M, t0 + S(s), .8)
    for s in (0, 10): kick(M, t0 + S(s), .9)
    for s in (4, 12): snare(M, t0 + S(s), .85)
    for k in range(16): hat(M, t0 + S(k), .25 if k % 2 == 0 else .12)
@D('steps_soft')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 4, 8, 12): footstep(M, t0 + S(s), .8, soft=True)
    for s in (4, 12): M.add('drums', t0 + S(s), hp(noise(int(.03 * SR)), 1800) * np.exp(-tarr(int(.03 * SR)) / .006) * .3, pan=.3)   # finger snaps
    shaker(M, t0 + S(6), .3); shaker(M, t0 + S(14), .3)

# ---------------- per-sport extras ----------------
def ex_soccer(M, t0, st, S, i, n, tones, root):
    if i % 4 == 3: oh_chant(M, t0, st, tones, .8)
    if i % 8 == 0: crowd(M, t0, 4 * 4 * st, .6)
def ex_basketball(M, t0, st, S, i, n, tones, root):
    for s in (0, 4, 8, 12): ball_bounce(M, t0 + S(s), .7)
    if i % 2 == 1: squeak(M, t0 + S(7)); squeak(M, t0 + S(14), .8)
def ex_football(M, t0, st, S, i, n, tones, root):
    if i % 4 == 3: hey(M, t0 + S(12), .9)
def ex_baseball(M, t0, st, S, i, n, tones, root):
    if i % 8 == 7: organ_charge(M, t0, st, .8)
    if i % 4 == 1: claps(M, t0 + S(0)); claps(M, t0 + S(4)); claps(M, t0 + S(8))
def ex_hockey(M, t0, st, S, i, n, tones, root):
    if i % 4 == 0: swoosh(M, t0 + S(2), .4, .6)
def ex_tennis(M, t0, st, S, i, n, tones, root):
    for s, p in ((0, -.6), (8, .6)): pok(M, t0 + S(s), p, .8)
def ex_volley(M, t0, st, S, i, n, tones, root):
    if i % 4 == 3: pok(M, t0 + S(12), 0., 1.2); kick(M, t0 + S(12), .5)
def ex_ski(M, t0, st, S, i, n, tones, root):
    for k in range(0, 16, 2): sleigh(M, t0 + S(k), .5)
    if i % 2 == 0: swoosh(M, t0, 8 * st, .7, up=(i % 4 == 0))
def ex_badminton(M, t0, st, S, i, n, tones, root):
    for s, p in ((0, -.6), (6, .6), (8, -.6), (14, .6)): pok(M, t0 + S(s), p, .7, light=True)
    if i % 4 == 2: squeak(M, t0 + S(10), .8)
def ex_frisbee(M, t0, st, S, i, n, tones, root):
    if i % 2 == 1: swoosh(M, t0 + S(4), 8 * st, .7, up=(i % 4 == 1))
    if i % 8 == 7: hey(M, t0 + S(12), .8)
def ex_birds(M, t0, st, S, i, n, tones, root):
    if i % 4 == 2:
        for k in range(3):
            N = int(.08 * SR); tt = tarr(N); f = 3500 + 900 * np.sin(np.pi * tt / tt[-1])
            M.add('fx', t0 + S(10) + k * .1, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) * .04, pan=.5)

# ---------------- endings (each sport ends its own way) ----------------
def end_soccer(M, t0, st, S, i, n, tones, root):      # three final whistles, then the crowd roars
    if i: return
    for k, d in ((0, .25), (.4, .25), (.8, .9)): whistle(M, t0 + k, d, 1.)
    crowd(M, t0 + .8, 3.5, 1.3); crash(M, t0 + .8, .5)
    for c in tones[:3]: brass(M, 'keys', t0 + .8, c + 12, 2., .2)
def end_basketball(M, t0, st, S, i, n, tones, root):  # buzzer beater
    if i: return
    for k in range(3): ball_bounce(M, t0 + k * st * 2, .8)
    buzzer(M, t0 + 6 * st, 1.3, 1.2); crowd(M, t0 + 6 * st, 3., 1.2); kick(M, t0 + 6 * st, .9); heavy808(M, t0 + 6 * st, root if root < 44 else root - 12, 1.5, .5)
def end_football(M, t0, st, S, i, n, tones, root):    # drumline roll into a fight-song hit
    if i: return
    for j in range(16): snare(M, t0 + j * st / 2, .2 + .04 * j)
    te = t0 + 8 * st; kick(M, te, 1.); crash(M, te, .7); tuba(M, te, (root if root < 44 else root - 12) + 12, 1.5, 1.)
    for c in tones[:3]: brass(M, 'keys', te, c + 12, 1.5, .22)
    crowd(M, te, 3., 1.)
def end_baseball(M, t0, st, S, i, n, tones, root):    # organ 'charge!' and the crowd answers
    if i: return
    organ_charge(M, t0, st, 1.); claps(M, t0 + 14 * st); crowd(M, t0 + 14 * st, 2.5, 1.)
def end_hockey(M, t0, st, S, i, n, tones, root):      # goal horn
    if i: return
    goal_horn(M, t0, 2.4, 1.2); crowd(M, t0, 3., 1.2); crash(M, t0, .6)
    for c in tones[:3]: organ(M, t0, c + 12, 2., .5)
def end_tennis(M, t0, st, S, i, n, tones, root):      # one last rally, a quiet chord, polite applause
    if i: return
    for k, p in enumerate((-.6, .6, -.6, .6)): pok(M, t0 + k * st * 2, p, .8)
    for c in tones[:3]: violins(M, t0 + 8 * st, c + 12, 2.5, .35, att=.1)
    for k in range(10): claps(M, t0 + 8 * st + .3 + k * .13, .5 * (1 - k / 12))
def end_volley(M, t0, st, S, i, n, tones, root):      # the spike, then the whistle
    if i: return
    pok(M, t0, 0., 1.4); kick(M, t0, .8); whistle(M, t0 + .5, .6, 1.)
    for c in tones[:3]: steel(M, 'keys', t0 + .5, c + 12, 1.5, .6)
def end_ski(M, t0, st, S, i, n, tones, root):         # hockey-stop spray of snow, bells ring out
    if i: return
    swoosh(M, t0, .9, 1.2, up=False)
    for k in range(6): sleigh(M, t0 + .9 + k * .12, .6 * (1 - k / 7))
    for c in tones[:3]: celesta(M, 'keys', t0 + .9, c + 12, 2., .6)
def end_badminton(M, t0, st, S, i, n, tones, root):   # a smash and a squeak, then a bright chord
    if i: return
    pok(M, t0, 0., 1.5, light=True); squeak(M, t0 + .15, 1.); kick(M, t0, .6)
    for c in tones[:3]: marimba(M, 'keys', t0 + 2 * st, c + 12, 1.5, .8)
def end_frisbee(M, t0, st, S, i, n, tones, root):     # the long throw... caught
    if i: return
    swoosh(M, t0, 1.2, 1., up=True); clap(M, t0 + 1.2, .8); hey(M, t0 + 1.25, 1.); crowd(M, t0 + 1.2, 2., .8)
    for j, c in enumerate(tones[:3]): M.add('keys', t0 + 1.2 + j * .01, lp(ks(mtof(c + 12), 1.8, .7, .996), 5000) * .25)
def end_running(M, t0, st, S, i, n, tones, root):     # sprint finish: steps speed up, then the finish line
    if i: return
    for k in range(12): footstep(M, t0 + k * st, .9)
    te = t0 + 12 * st; crowd(M, te, 2.5, 1.); kick(M, te, 1.); crash(M, te, .6)
    for c in tones[:3]: supersaw(M, 'keys', te, c + 12, 1.6, .06, cut=3500, a=.003, r=.8, voices=4)
def end_jogging(M, t0, st, S, i, n, tones, root):     # slowing down: the last few steps spread out, a soft chord
    if i: return
    t = t0
    for d in (1, 1, 1.3, 1.7, 2.3): footstep(M, t, .7); t += d * 4 * st / 2
    for c in tones[:3]: epiano(M, 'keys', t, c + 12, 2.5, .1)
def end_walking(M, t0, st, S, i, n, tones, root):     # stopping at the door: two steps, a whistle, a strum
    if i: return
    footstep(M, t0, .7, soft=True); footstep(M, t0 + 4 * st, .7, soft=True)
    ocarina(M, t0 + 8 * st, tones[0] + 24, 1.2, .8)
    for j, c in enumerate(tones[:3]): M.add('keys', t0 + 8 * st + j * .02, lp(ks(mtof(c + 12), 2., .6, .997), 5000) * .25)

def sport(file, title, bpm, A, B, chA, chB, keys, lead, drums, bass, extra, ending, leadB=None, keysB=None, swing=0., levels=None, intro_drums=None, verb=2.2, kv=1.):
    s = {'intro': sec(4, chA, keys=keys, drums=intro_drums, extra=extra, kv=kv),
         'A': sec(8, chA, keys=keys, drums=drums, bass=bass, lead=lead, mel=A, extra=extra, kind='verse', kv=kv),
         'B': sec(8, chB, keys=keysB or keys, drums=drums, bass=bass, lead=leadB or lead, mel=B, extra=extra, kind='chorus', impact=True, kv=kv),
         'end': sec(1, [chA[0]], extra=ending, fill=False, kind='outro')}
    return dict(file=file, title=title, bpm=bpm, swing=swing, sections=s, order=['intro', 'A', 'B', 'A', 'B', 'end'], verb=verb,
                levels=levels or {}, chorus_keys=True, cont_tol=0.)

SONGS = {
 'soccer': sport('Golazo_Anthem', 'Golazo Anthem', 128,
   [[72,-1,74,76,-1,74,72,-1],[69,-1,-1,72,-1,74,-1,-1],[76,-1,77,79,-1,77,76,-1],[74,-1,-1,-1,0,0,0,0]],
   [[79,-1,79,81,-1,79,77,-1],[76,-1,-1,72,-1,74,-1,-1],[77,-1,77,79,-1,77,76,74],[72,-1,-1,-1,0,0,0,0]],
   ['C', 'Am', 'F', 'G'], ['F', 'G', 'Em', 'Am'], ['brasshits'], 'brass2', 'samba', 'octave', ex_soccer, end_soccer, leadB='brass2+voice', intro_drums='samba'),
 'basketball': sport('Full_Court_Press', 'Full Court Press', 94,
   [[67,-1,0,70,-1,72,0,0],[70,-1,67,-1,65,-1,0,0],[67,-1,0,70,-1,72,74,-1],[72,-1,-1,-1,0,0,0,0]],
   [[79,-1,79,-1,77,74,-1,72],[74,-1,-1,72,-1,70,-1,-1],[72,-1,74,77,-1,79,-1,82],[79,-1,-1,-1,0,0,0,0]],
   ['Gm', 'Eb', 'Bb', 'F'], ['Eb', 'F', 'Dm', 'Gm'], ['stabs', 'pianoriff'], 'brass2', 'boombap', '808', ex_basketball, end_basketball, leadB='brass2+synth'),
 'football': sport('Fourth_and_Goal', 'Fourth and Goal', 112,
   [[70,-1,-1,74,-1,77,-1,-1],[82,-1,-1,81,-1,79,-1,-1],[79,-1,77,75,-1,74,-1,72],[70,-1,-1,-1,0,0,0,0]],
   [[77,-1,77,79,-1,81,-1,82],[84,-1,-1,82,-1,81,-1,-1],[79,-1,81,82,-1,79,-1,77],[82,-1,-1,-1,0,0,0,0]],
   ['Bb', 'Eb', 'F', 'Bb'], ['Eb', 'F', 'Gm', 'F'], ['brasshits'], 'brass2', 'drumline', 'tuba', ex_football, end_football, leadB='brass2+horn', intro_drums='drumline'),
 'baseball': sport('Seventh_Inning_Swing', 'Seventh Inning Swing', 120,
   [[72,-1,76,-1,79,-1,76,-1],[77,-1,76,74,-1,-1,0,0],[71,-1,74,-1,77,-1,74,-1],[76,-1,74,72,-1,-1,0,0]],
   [[79,-1,79,81,-1,79,76,-1],[77,-1,77,79,-1,77,74,-1],[76,-1,76,77,-1,79,-1,81],[79,-1,-1,-1,0,0,0,0]],
   ['C', 'F', 'G', 'C'], ['F', 'C', 'D7', 'G'], ['stride'], 'organ', 'swing', 'walking', ex_baseball, end_baseball, swing=.2),
 'hockey': sport('Ice_Time', 'Ice Time', 140,
   [[76,-1,0,76,-1,74,76,-1],[79,-1,-1,76,-1,-1,0,0],[74,-1,0,74,-1,72,74,-1],[71,-1,-1,-1,0,0,0,0]],
   [[83,-1,83,-1,81,79,-1,81],[83,-1,-1,79,-1,76,-1,-1],[81,-1,79,76,-1,79,-1,81],[76,-1,-1,-1,0,0,0,0]],
   ['Em', 'C', 'D', 'B7'], ['C', 'D', 'Em', 'B7'], ['power'], 'organ+crunch', 'rock', 'octave', ex_hockey, end_hockey, levels={'gtrL': .9, 'gtrR': .9}),
 'tennis': sport('Match_Point', 'Match Point', 118,
   [[74,-1,-1,78,-1,81,-1,-1],[79,-1,-1,78,-1,76,-1,-1],[74,-1,-1,76,-1,78,-1,79],[81,-1,-1,-1,0,0,0,0]],
   [[83,-1,81,79,-1,78,-1,79],[81,-1,-1,78,-1,74,-1,-1],[79,-1,78,76,-1,74,-1,73],[74,-1,-1,-1,0,0,0,0]],
   ['D', 'G', 'A', 'D'], ['G', 'A', 'F#m', 'Bm'], ['pizzarp', 'strings'], 'flute', 'halfpop', 'finger', ex_tennis, end_tennis, leadB='strings+flute', verb=2.6),
 'volleyball': sport('Beach_Spike', 'Beach Spike', 116,
   [[76,-1,79,-1,81,-1,79,76],[74,-1,-1,76,-1,-1,0,0],[72,-1,76,-1,79,-1,76,74],[72,-1,-1,-1,0,0,0,0]],
   [[81,-1,81,79,-1,76,-1,79],[81,-1,-1,84,-1,81,-1,-1],[79,-1,79,76,-1,74,-1,76],[72,-1,-1,-1,0,0,0,0]],
   ['C', 'Em', 'Am', 'F'], ['F', 'G', 'Em', 'Am'], ['uke', 'steelcomp'], 'steel', 'house', 'synth8', ex_volley, end_volley, leadB='steel+chop'),
 'skiing': sport('Powder_Run', 'Powder Run', 132,
   [[78,-1,81,-1,85,-1,83,81],[83,-1,-1,81,-1,78,-1,-1],[76,-1,78,-1,81,-1,80,78],[80,-1,-1,-1,0,0,0,0]],
   [[85,-1,83,81,-1,83,-1,85],[86,-1,-1,85,-1,81,-1,-1],[83,-1,81,80,-1,81,-1,83],[81,-1,-1,-1,0,0,0,0]],
   ['F#m', 'D', 'A', 'E'], ['D', 'E', 'C#m', 'F#m'], ['eurobeat', 'celesta'], 'saw80s', 'eurobeat', 'octave', ex_ski, end_ski, leadB='saw80s+celesta', verb=2.8),
 'badminton': sport('Shuttle_Rally', 'Shuttle Rally', 150,
   [[79,-1,76,-1,79,-1,84,-1],[83,-1,81,79,-1,-1,0,0],[77,-1,74,-1,77,-1,81,-1],[79,-1,-1,-1,0,0,0,0]],
   [[84,-1,83,81,-1,79,-1,81],[83,-1,-1,79,-1,76,-1,-1],[81,-1,79,77,-1,76,-1,74],[72,-1,-1,-1,0,0,0,0]],
   ['C', 'G', 'F', 'C'], ['Am', 'F', 'G', 'C'], ['marimbaarp'], 'xylo', 'ska', 'synth8', ex_badminton, end_badminton, leadB='xylo+sqbright', kv=.8),
 'frisbee': sport('Huck_It', 'Huck It', 160,
   [[74,-1,76,-1,78,-1,-1,81],[79,-1,-1,78,-1,76,-1,-1],[74,-1,76,-1,78,-1,-1,79],[78,-1,-1,-1,0,0,0,0]],
   [[81,-1,81,-1,79,-1,78,-1],[76,-1,-1,78,-1,79,-1,-1],[81,-1,83,-1,81,-1,79,-1],[78,-1,-1,-1,0,0,0,0]],
   ['D', 'Bm', 'G', 'A'], ['G', 'A', 'Bm', 'D'], ['uke', 'guitar'], 'guitar', 'punk', 'octave', ex_frisbee, end_frisbee, leadB='guitar+whistle'),
 'running': sport('Stride_176', 'Stride 176', 176,
   [[69,-1,-1,72,-1,76,-1,-1],[74,-1,-1,72,-1,71,-1,-1],[69,-1,-1,72,-1,76,-1,79],[77,-1,-1,-1,0,0,0,0]],
   [[81,-1,79,77,-1,76,-1,77],[79,-1,-1,76,-1,72,-1,-1],[77,-1,76,74,-1,72,-1,71],[69,-1,-1,-1,0,0,0,0]],
   ['Am', 'F', 'C', 'G'], ['F', 'G', 'Am', 'Am'], ['pluck', 'pad'], 'synth', 'steps_dnb', 'reese', None, end_running, leadB='synth+chop', intro_drums='steps'),
 'jogging': sport('Easy_Pace', 'Easy Pace', 160,
   [[76,-1,-1,-1,74,-1,72,-1],[74,-1,-1,-1,71,-1,-1,-1],[72,-1,-1,-1,74,-1,76,-1],[79,-1,-1,-1,-1,-1,0,0]],
   [[79,-1,-1,-1,77,-1,76,-1],[77,-1,-1,-1,74,-1,-1,-1],[76,-1,-1,-1,74,-1,72,-1],[72,-1,-1,-1,-1,-1,0,0]],
   ['C', 'G', 'Am', 'F'], ['F', 'G', 'Em', 'Am'], ['acoustic', 'pad'], 'voice', 'steps', 'long', None, end_jogging, leadB='voice+flute', intro_drums='steps_soft'),
 'walking': sport('Sunday_Stroll', 'Sunday Stroll', 112,
   [[79,-1,-1,76,-1,74,-1,76],[79,-1,-1,-1,74,-1,-1,-1],[72,-1,-1,74,-1,76,-1,79],[81,-1,-1,-1,-1,-1,0,0]],
   [[84,-1,-1,83,-1,81,-1,79],[81,-1,-1,-1,79,-1,-1,-1],[77,-1,-1,76,-1,74,-1,72],[74,-1,-1,-1,-1,-1,0,0]],
   ['G', 'C', 'D', 'G'], ['C', 'G', 'Am', 'D'], ['uke'], 'ocarina', 'steps_soft', 'upright', ex_birds, end_walking, leadB='ocarina+celesta', swing=.15),
}

SONGS['tennis']['targets'] = {'outro': -21.}      # a quieter ending, so it doesn't jump up
SONGS['walking']['levels'] = {'keys': 3.5}         # the ukulele up front, so the intro isn't faint
SONGS['walking']['gain_like'] = {'A': 'intro', 'B': 'intro', 'end': 'intro'}   # one level for the whole song: the band joins the intro instead of the intro being turned down

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
