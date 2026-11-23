"""Batch E: extra breakcore, Infinite Series as breakcore, and songs for gameplay moments the collection was missing.
python batch_e.py all  (or: squared math_bc oops heist countdown comeback endscreen)"""
import sys
import numpy as np
from newstyles import *
from popkit import build as pbuild
from breakcore_engine import build as bbuild, make_kit, PATS, gong, play_mel, play_keys
from seasons import AMEN, FUNK
from batch_d import blocks
import mathsong as ms

# ================= Breakcore Squared: two breaks at once, fixed 32nd rolls, light bass =================
_K2 = {}
def double_breaks(M, sec, i, t0, st, tones, root):
    if sec not in ('dropA', 'dropB'): return
    if 'sl' not in _K2: _K2['sl'], _K2['n'] = make_kit(st, dict(AMEN, crunch=2.2, tone=8000, clap=.3))
    sl = _K2['sl']; bar = i % 2; pat = PATS['P3' if sec == 'dropA' else 'P1']
    for k in range(16):
        x = sl[pat[bar * 16 + k]]; p = (-.45, .45)[k % 2]
        M.add('break', t0 + k * st, x[0] * .5 * (1 - p), x[1] * .5 * (1 + p))
    for base in (6, 14):                       # the same two 32nd-note snare rolls in every bar (steady, not random)
        for j in range(4): snare(M, t0 + (base + j / 2) * st, .18 + .06 * j)
    if i % 4 == 3:                              # a snare rush into every 4th bar
        for j in range(8): snare(M, t0 + (12 + j / 2) * st, .2 + .07 * j)
SOLO = {}
def breaks_solo_end(M, t_out, st, B, nb, ch):   # the breaks play solo for two bars, then the instrumental plays out and ends on its own
    SOLO['t'] = (t_out, t_out + 2 * B); sl, n = make_kit(st, dict(AMEN, crunch=2.4, clap=.35))
    for b in range(2):
        for k in range(16):
            x = sl[PATS['P2'][(b % 2) * 16 + k]]; M.add('break', t_out + b * B + k * st, x[0] * .9, x[1] * .9)
    for j in range(8): snare(M, t_out + B + (12 + j / 2) * st, .25 + .08 * j)
    t = t_out + 2 * B
    for row in SQ:                                # the melody one last time over the piano
        for k, x in enumerate(row):
            if x > 0:
                L = 1
                while k + L < 8 and row[k + L] == -1: L += 1
                play_mel(M, 'lead', t + 2 * k * st, x, 2 * L * st, .8)
        t += B
    tones, root = ch[0]
    for c in [root + 12] + tones: piano(M, 'keys', t_out + nb * B, c + 12, 4., .35)
def sq_keys(M, t0, st, tones, root, vol, bar):
    if not (SOLO and SOLO['t'][0] - 1e-6 <= t0 < SOLO['t'][1] - 1e-6): play_keys(M, 'piano', t0, st, tones, root, vol, bar)
SQ = [[78,-1,81,-1,85,-1,83,81],[81,-1,-1,78,-1,-1,0,0],[76,-1,78,-1,81,-1,80,78],[80,-1,-1,-1,0,0,0,0]]
SQB = [[85,-1,83,81,-1,83,-1,85],[86,-1,-1,85,-1,81,-1,-1],[85,-1,83,81,-1,80,-1,78],[80,-1,-1,-1,-1,-1,0,0]]

# ================= Breakcore Cubed: three breaks at once, each in its own frequency range =================
_K3 = {}
def kit3(st):   # layer 1: full funk break (engine); layer 2: amen break above 2 kHz (hats, snare tops); layer 3: a jungle kick break below 160 Hz
    if not _K3:
        def filtered(kit, fn):
            sl, n = make_kit(st, kit); x = np.concatenate(sl, axis=1); x = np.array([fn(c) for c in x])
            return [x[:, i * n:(i + 1) * n] for i in range(32)]
        _K3['hi'] = filtered(dict(AMEN, crunch=2.4, clap=.4), lambda c: hp(c, 2000) * 1.8)
        _K3['lo'] = filtered({'K': [[0, 3, 6, 10, 13], [0, 3, 8, 11, 14]], 'S': [[], []], 'G': [[], []], 'hat': None, 'punch': 1.6, 'crunch': 2.}, lambda c: lp(c, 160) * 1.6)
    return _K3
def put_layer(M, layer, pat, t0, st, gain, pan=0.):
    for k in range(16):
        x = layer[pat[k]]; M.add('break', t0 + k * st, x[0] * gain * (1 - pan), x[1] * gain * (1 + pan))
def triple_breaks(M, sec, i, t0, st, tones, root):
    if sec not in ('dropA', 'dropB'): return
    K3 = kit3(st); bar = i % 2; pat = PATS['P3' if sec == 'dropA' else 'P1']
    put_layer(M, K3['hi'], pat[bar * 16:(bar + 1) * 16], t0, st, .4, (-.4, .4)[i % 2])   # the extra layers sit lower so they don't smear the main break
    put_layer(M, K3['lo'], list(range(bar * 16, bar * 16 + 16)), t0, st, .5)
CUBE = {}
def cube_end(M, t_out, st, B, nb, ch):   # the layers leave one at a time: three breaks, then two, then one, then the piano alone
    CUBE['t'] = t_out; K3 = kit3(st); main, n = make_kit(st, dict(FUNK, crunch=2.3, punch=1.35, clap=.4))
    for b in range(6):
        t0 = t_out + b * B; seq = PATS['P2'][(b % 2) * 16:(b % 2) * 16 + 16]
        put_layer(M, main, seq, t0, st, .85)
        if b < 4: put_layer(M, K3['hi'], seq, t0, st, .55, (-.35, .35)[b % 2])
        if b < 2: put_layer(M, K3['lo'], list(range((b % 2) * 16, (b % 2) * 16 + 16)), t0, st, .7)
    tones, root = ch[0]
    for c in [root + 12] + tones: piano(M, 'keys', t_out + nb * B, c + 12, 4., .35)
CU = [[76,-1,72,-1,69,-1,72,74],[76,-1,-1,79,-1,76,-1,-1],[77,-1,72,-1,69,-1,72,77],[76,-1,-1,72,-1,-1,0,0],      # chord tones: Am, Am, F, F
      [79,-1,76,-1,72,-1,76,79],[84,-1,-1,79,-1,76,-1,-1],[80,-1,76,-1,71,-1,74,76],[80,-1,-1,-1,-1,-1,0,0]]      # C, C, E, E
CUB = [[81,-1,79,76,-1,72,-1,76],[79,-1,-1,76,-1,72,-1,-1],[81,-1,77,72,-1,77,-1,81],[79,-1,-1,77,-1,-1,0,0],
       [84,-1,79,76,-1,79,-1,84],[83,-1,-1,79,-1,76,-1,-1],[83,-1,80,76,-1,80,-1,83],[80,-1,-1,-1,-1,-1,0,0]]

# ================= Infinite Series Breaks =================
def zeno_end(M, t_out, st, B, nb, ch):
    tones, root = ch[0]; ms.zeno(M, t_out + (nb - 1) * B, st, lambda k: k * st, 0, 1, tones, root)
def math_extra(M, sec, i, t0, st, tones, root):
    if sec == 'half': ms.primes(M, t0, st, lambda k: k * st, i, 8, tones, root)
    if sec == 'intro': ms.harmonics(M, t0, st, lambda k: k * st, i, 8, tones, root)

BC = {
 'squared': dict(file='Breakcore_Squared', title='Breakcore Squared', bpm=186, chords=['F#m', 'D', 'A', 'E'], keys=sq_keys, pad=.05, outro_breaks=False,
   mel='lead', melB='lead', layerB='strings', bass='sub', kit=dict(FUNK, crunch=2.3, punch=1.35, clap=.4), patA='P2', patB='P4',
   melody=blocks(SQ), melodyB=blocks(SQB), seed=301, extra=double_breaks, levels={'sub': .45, 'break': 1.15}, mus_gap=7.,
   ending='custom', ending_fn=breaks_solo_end),
 'cubed': dict(file='Breakcore_Cubed', title='Breakcore Cubed', bpm=190, chords=['Am', 'F', 'C', 'E'], keys='piano', pad=.05, outro_breaks=False,
   mel='piano', melB='lead', layerB='piano', bass='sub', kit=dict(FUNK, crunch=2.1, punch=1.35, clap=.4), patA='P0', patB='P3',
   melody=blocks(CU), melodyB=blocks(CUB), seed=333, extra=triple_breaks, levels={'sub': .35, 'break': 1.1}, mus_gap=7.,
   ending='custom', ending_fn=cube_end),
 'math_bc': dict(file='Infinite_Series_Breaks', title='Infinite Series Breaks', bpm=174, chords=['Am', 'F', 'C', 'G'], keys='piano', pad=.05,
   mel=lambda M, t, n, d, v: play_mel(M, 'vibes', t, n, d, .55 * v), melB=lambda M, t, n, d, v: play_mel(M, 'lead', t, n, d, .7 * v), layerB='vibes', match_drops='A',   # first drop: the melody sits back so the breaks come through
   bass='sub', kit=dict(AMEN, crunch=1.8, tone=10000, clap=.25), patA='P3', patB='P1',
   melody=blocks(ms.digit_mel(ms.PI, 4)), melodyB=blocks(ms.digit_mel(ms.E, 4, 57)), seed=314, extra=math_extra,
   ending='custom', ending_fn=zeno_end),
}

# ================= gameplay-moment songs =================
def slide_whistle(M, t, up=True, dur=.5, vol=1.):
    N = int(dur * SR); tt = tarr(N); f = 600 + 1400 * (tt / dur) ** 1.5 if up else 2000 - 1500 * (tt / dur) ** .7
    M.add('fx', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / dur) ** .5 * vol * .16)
@K('polka')
def _(M, t0, st, S, T, r, v):          # oom-pah: accordion chords on the offbeats
    for s in (4, 12):
        for c in T[:3]: accordion(M, t0 + S(s), c + 12, st * 1.5, .5 * v, bus='keys', pan=.25)
@D('polka')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 8): kick(M, t0 + S(s), .7)
    for s in (4, 12): snare(M, t0 + S(s), .45); hat(M, t0 + S(s), .3, open_=True)
    if i % 4 == 3: woodblock(M, t0 + S(14), True, .8); woodblock(M, t0 + S(15), False, .8)
def oops_fx(M, t0, st, S, i, n, tones, root):
    if i % 4 == 1: slide_whistle(M, t0 + S(12), True, .45)
    if i % 4 == 3: slide_whistle(M, t0 + S(12), False, .5)
def wah_wah(M, t0, st, S, i, n, tones, root):    # the classic 'fail' ending: four sad steps down, the last one wobbling
    if i: return
    for k, nn in enumerate((67, 66, 65)): horn(M, t0 + k * .45, nn, .4, 1.1)
    N = int(1.4 * SR); tt = tarr(N); f = mtof(64 - .5 * np.clip(tt - .3, 0, 1) + .35 * np.sin(2 * np.pi * 6 * tt))
    x = lp(saw(f, N), 900) * envN(N, 1.3, .05, .2, .9, .2); M.add('lead', t0 + 1.35, x * .2)
    tuba(M, t0 + 1.35, 40, 1.3, .8); cymbal(M, t0 + 1.35, .2)

@Bs('walkpizz')
def _(M, t0, st, S, root):            # sneaky walking pizzicato bass
    r = root if root < 44 else root - 12
    for s, o in ((0, 0), (4, 3), (8, 7), (12, 6)): fbass(M, t0 + S(s), r + o, st * 2.5, .55)
def snaps(M, t0, st, S, i, n, tones, root):
    for s in (4, 12): M.add('perc', t0 + S(s), hp(noise(int(.03 * SR)), 1800) * np.exp(-tarr(int(.03 * SR)) / .006) * .35, pan=.3)
def tiptoe_end(M, t0, st, S, i, n, tones, root):   # three tiptoe plucks and a snap
    if i: return
    for k, nn in enumerate((69, 72, 76)): pizz(M, t0 + k * st * 2, nn, 1.)
    pizz(M, t0 + 8 * st, 57, 1.2); M.add('perc', t0 + 8 * st, hp(noise(int(.03 * SR)), 1800) * np.exp(-tarr(int(.03 * SR)) / .006) * .45)

def braam(M, t, n=38, dur=2.5, vol=1.):            # huge low brass 'braam' (trailer hit)
    N = int((dur + .5) * SR); tt = tarr(N); x = 0
    for d in (0, 12, 7 + 12): x = x + saw(mtof(n + d) * (1 + .002 * d), N)
    w = np.exp(-tt / .4); y = np.tanh((lp(x, 500) * (1 - w) + lp(x, 1300) * w) * 2.) * envN(N, dur, .03, .3, .8, .6)
    M.add('fx', t, y * vol * .22); timpani(M, t, n + 12, .9 * vol); impact(M, t, .5 * vol)
def ticking(M, t0, st, S, i, n, tones, root):
    for k in range(0, 16, 2): woodblock(M, t0 + S(k), k % 4 == 0, .55)
def tension(M, t0, st, S, i, n, tones, root):
    ticking(M, t0, st, S, i, n, tones, root)
    if i % 4 == 0: braam(M, t0, (root if root < 44 else root - 12), 2.5, .8)
def climax(M, t0, st, S, i, n, tones, root):
    ticking(M, t0, st, S, i, n, tones, root)
    if i % 2 == 0: braam(M, t0, (root if root < 44 else root - 12), 1.8, .7)
def final_braam(M, t0, st, S, i, n, tones, root):
    if i: return
    braam(M, t0, 33, 4., 1.3); crash(M, t0, .7); gong(M, t0, .6)
@K('ostinato')
def _(M, t0, st, S, T, r, v):          # driving low-string ostinato
    for k in range(16): violins(M, t0 + S(k), (r + 24 if k % 4 else r + 12), st * .8, .3 * v, att=.005, bus='keys')
@D('trailer')
def _(M, t0, st, S, i, n, fill):
    for s in (0, 3, 6, 8, 11, 14): tom(M, t0 + S(s), 41 if s in (0, 8) else 45, .7)
    for s in (4, 12): snare(M, t0 + S(s), .8)
    kick(M, t0, 1.); kick(M, t0 + S(8), .9)

def comeback_end(M, t0, st, S, i, n, tones, root):   # held final chord over a swelling timpani roll
    if i: return
    for k in range(24): timpani(M, t0 + k * st / 2, 33, .15 + .03 * k)
    te = t0 + 12 * st; crash(M, te, .7); kick(M, te, 1.)
    for c in tones[:3] + [tones[0] + 12]: brass(M, 'keys', te, c + 12, 3., .2); violins(M, te, c + 12, 3.5, .4, att=.05)
    fbass(M, te, (tones[0] if tones[0] < 56 else tones[0] - 24) - 12, 3., .7)
def endscreen_hit(M, t0, st, S, i, n, tones, root):
    if i: return
    kick(M, t0, .9); crash(M, t0, .5)
    for c in tones[:3]: brass(M, 'keys', t0, c + 12, .5, .2)
    fbass(M, t0, 41, .5, .7)

POP = {
 # funny fails: a goofy polka with tuba, clarinet, xylophone and slide whistles; ends with a sad 'wah-wah'
 'oops': dict(file='Oops_Again', title='Oops Again', bpm=150, chorus_keys=True, sections={
   'intro': sec(2, ['F', 'C7'], keys=['polka'], bass='tuba', drums='polka', fill=False),
   'A': sec(8, ['F', 'C7', 'C7', 'F'], keys=['polka'], bass='tuba', drums='polka', lead='clarinet', extra=oops_fx, kind='verse',
            mel=[[72,-1,69,-1,72,-1,77,-1],[76,-1,74,72,-1,70,-1,-1],[70,-1,67,-1,70,-1,76,-1],[77,-1,-1,-1,0,0,0,0]]),
   'B': sec(8, ['Bb', 'F', 'C7', 'F'], keys=['polka'], bass='tuba', drums='polka', lead='xylo+clarinet', extra=oops_fx, kind='chorus',
            mel=[[74,-1,74,76,-1,77,-1,-1],[72,-1,-1,69,-1,65,-1,-1],[70,-1,72,74,-1,76,-1,79],[77,-1,-1,-1,0,0,0,0]]),
   'end': sec(1, ['F'], extra=wah_wah, kind='outro')},
   order=['intro', 'A', 'B', 'A', 'B', 'end'], levels={'lead': 1.2}),
 # stealth / sneaking: tiptoe jazz with walking bass, pizzicato, brushes, finger snaps
 'heist': dict(file='Tiptoe_Heist', title='Tiptoe Heist', bpm=104, swing=.22, chorus_keys=True, sections={
   'intro': sec(4, ['Am', 'Am', 'F7', 'E7'], bass='walkpizz', drums='brush', extra=snaps),
   'A': sec(8, ['Am', 'Am', 'F7', 'E7'], keys=['pizzarp'], kv=.6, bass='walkpizz', drums='brush', lead='clarinet', extra=snaps, kind='verse',
            mel=[[69,-1,0,72,0,0,75,76],[0,0,0,0,69,-1,0,0],[72,-1,0,75,0,0,77,78],[76,-1,-1,-1,0,0,0,0]]),
   'B': sec(8, ['Dm', 'Am', 'F7', 'E7'], keys=['pizzarp'], kv=.7, bass='walkpizz', drums='brush', lead='sax', extra=snaps, kind='chorus',
            mel=[[74,-1,0,77,0,76,0,74],[72,-1,-1,0,69,-1,0,0],[77,-1,0,75,0,74,0,72],[71,-1,-1,-1,0,0,0,0]]),
   'end': sec(1, ['Am'], extra=tiptoe_end, kind='outro')},
   order=['intro', 'A', 'B', 'A', 'B', 'end'], levels={'lead': 1.15}),
 # clutch / last zone: ticking clock, low-string ostinato, trailer braams, building to a climax
 'countdown': dict(file='Final_Zone_Countdown', title='Final Zone Countdown', bpm=120, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Dm', 'Dm', 'Bb', 'A'], keys=['dark'], extra=ticking),
   'build1': sec(8, ['Dm', 'Dm', 'Bb', 'A'], keys=['dark', 'ostinato'], extra=tension, kind='verse'),
   'build2': sec(8, ['Dm', 'Bb', 'Gm', 'A'], keys=['dark', 'ostinato', 'tremolo'], drums='trailer', bass='sub', extra=tension, riser=True, kind='pre',
                 lead='horn', mel=[[62,-1,-1,-1,65,-1,-1,-1],[70,-1,-1,-1,69,-1,-1,-1],[67,-1,-1,-1,70,-1,-1,-1],[69,-1,-1,-1,-1,-1,-1,-1]]),
   'climax': sec(8, ['Dm', 'Bb', 'Gm', 'A'], keys=['ostinato', 'choir', 'tremolo'], drums='trailer', bass='sub', extra=climax, impact=True, kind='chorus',
                 lead='brass2+strings', mel=[[74,-1,-1,77,-1,76,74,-1],[70,-1,-1,-1,69,-1,-1,-1],[67,-1,70,74,-1,72,-1,70],[69,-1,-1,-1,-1,-1,-1,-1]]),
   'end': sec(1, ['Dm'], extra=final_braam, kind='outro')},
   order=['intro', 'build1', 'build2', 'climax', 'end'], levels={'fx': 1.}),
 # comeback: starts sad on piano, builds into a triumphant, full-orchestra finish
 'comeback': dict(file='Comeback_Rising', title='Comeback Rising', bpm=128, chorus_keys=True, sections={
   'intro': sec(4, ['Am', 'F', 'C', 'G'], keys=['piano']),
   'verse': sec(8, ['Am', 'F', 'C', 'G'], keys=['piano', 'strings'], drums='halfpop', bass='long', lead='piano', lv=.9,
                mel=[[69,-1,-1,72,-1,71,-1,69],[67,-1,-1,-1,65,-1,-1,-1],[64,-1,67,-1,72,-1,71,-1],[71,-1,-1,-1,-1,-1,0,0]]),
   'pre': sec(4, ['F', 'G', 'Em', 'Am'], keys=['piano', 'strings', 'pad'], drums='march', bass='long', riser=True, lead='strings',
              mel=[[72,-1,74,-1,76,-1,77,-1],[79,-1,-1,-1,74,-1,-1,-1],[76,-1,77,-1,79,-1,81,-1],[83,-1,-1,-1,-1,-1,0,0]]),
   'chorus': sec(8, ['C', 'G', 'Am', 'F'], keys=['pianoriff', 'strings', 'power'], drums='rock', bass='octave', lead='brass2+strings', impact=True,
                 mel=[[84,-1,-1,83,-1,79,-1,76],[79,-1,-1,-1,74,-1,-1,-1],[76,-1,79,81,-1,84,-1,86],[84,-1,-1,-1,-1,-1,0,0]]),
   'chorus2': sec(8, ['D', 'A', 'Bm', 'G'], keys=['pianoriff', 'strings'], drums='rock', bass='octave', lead='brass2+strings', impact=True, up=2, kind='chorus',
                  mel=[[84,-1,-1,83,-1,79,-1,76],[79,-1,-1,-1,74,-1,-1,-1],[76,-1,79,81,-1,84,-1,86],[84,-1,-1,-1,-1,-1,0,0]]),
   'end': sec(1, ['D'], extra=comeback_end, kind='outro')},
   order=['intro', 'verse', 'pre', 'chorus', 'verse', 'pre', 'chorus2', 'end'], cont_tol=0.),
 # end screen: a short, upbeat 30-second piece for the end of a video (subscribe / next video)
 'endscreen': dict(file='See_You_Next_Drop', title='See You Next Drop', bpm=120, chorus_keys=True, sections={
   'intro': sec(2, ['F', 'Dm'], keys=['pluck', 'chick'], drums='funk', bass='funky', fill=False),
   'A': sec(8, ['F', 'Dm', 'Bb', 'C'], keys=['pluck', 'chick'], drums='funk', bass='funky', lead='synth', kind='chorus',
            mel=[[77,-1,0,81,-1,0,84,-1],[81,-1,79,77,-1,0,0,0],[74,-1,0,77,-1,0,82,-1],[81,-1,-1,-1,79,-1,0,0]]),
   'B': sec(4, ['Bb', 'C', 'Am', 'Dm'], keys=['pluck', 'chick', 'brasshits'], drums='funk', bass='funky', lead='synth+brass', kind='chorus',
            mel=[[82,-1,81,79,-1,77,-1,-1],[79,-1,-1,-1,0,0,0,0],[81,-1,79,77,-1,76,-1,-1],[74,-1,-1,-1,0,0,0,0]]),
   'end': sec(1, ['F'], extra=endscreen_hit, kind='outro')},
   order=['intro', 'A', 'B', 'end']),
}

if __name__ == '__main__':
    names = (list(BC) + list(POP)) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names:
        if k in BC: bbuild(BC[k])
        else: pbuild(POP[k])
