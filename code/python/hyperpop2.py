"""More hyperpop variations (all sounds are code): bubblegum, glitchcore, hyper-DnB, emo hyperpop and nightcore.
python hyperpop2.py all  (or: bubble glitch dnb emo nightcore)"""
import sys
from newstyles import *
from popkit import build

def button(M, t0, st, S, i, n, tones, root):   # ending: one big hit, then let it ring
    if i: return
    kick(M, t0, 1., punch=1.4); crash(M, t0, .6); impact(M, t0, .3); heavy808(M, t0, (root if root < 44 else root - 12), 1.5, .55)
    for c in tones[:3]: supersaw(M, 'keys', t0, c + 12, 1.6, .07, cut=4000, a=.003, r=.8, voices=5)
    chopv(M, t0, tones[-1] + 12, .4, .9)

def hp_song(file, title, bpm, ch, chB, V, C, P, kv, kc, drums, bass, lv, lc, swing=0., crush=None, levels=None, intro=None, bridge=None, verb=2.2, dV=None):
    s = {'intro': sec(4, ch, keys=intro or kv, riser=True, lead=lc, mel=[C[0], C[1], [0] * 8, [0] * 8], lv=.6),
         'verse': sec(8, ch, keys=kv, drums=dV or drums, bass=bass, lead=lv, mel=V),
         'pre': sec(4, chB, keys=kv + ['pad'], drums='halfpop', bass='long', lead=lv, mel=P, riser=True),
         'chorus': sec(8, ch, keys=kc, drums=drums, bass=bass, lead=lc, mel=C, impact=True),
         'bridge': sec(4, chB, **(bridge or dict(keys=['pad'], lead=lv, mel=P, kind='bridge'))),
         'tag': sec(1, [ch[0]], keys=kc, drums=drums, bass=bass, fill=False, kind='chorus'),
         'end': sec(1, [ch[0]], extra=button, fill=False, kind='outro')}
    return dict(file=file, title=title, bpm=bpm, swing=swing, crush=crush, sections=s, verb=verb,
                order=['intro', 'verse', 'pre', 'chorus', 'verse', 'pre', 'chorus', 'bridge', 'chorus', 'tag', 'end'], levels=dict({'lead': 1.2}, **(levels or {})))

SONGS = {
 # bubblegum: glossy plastic bells, bouncy beat with metal clanks, chipmunk hooks
 'bubble': hp_song('Glitter_Overload', 'Glitter Overload', 136, ['Ab', 'Eb', 'Fm', 'Db'], ['Db', 'Eb', 'Cm', 'Fm'],
   [[72,-1,0,75,-1,0,77,-1],[75,-1,0,72,70,-1,0,0],[68,-1,0,72,-1,75,-1,77],[75,-1,-1,-1,0,0,0,0]],
   [[84,-1,82,80,-1,0,80,82],[84,-1,-1,87,-1,0,84,-1],[80,-1,82,84,-1,80,-1,77],[80,-1,-1,-1,0,0,0,0]],
   [[73,-1,75,-1,77,-1,80,-1],[79,-1,77,75,-1,0,0,0],[72,-1,75,-1,77,-1,79,-1],[80,-1,-1,-1,-1,-1,0,0]],
   ['plastic'], ['plastic', 'futurebass'], 'hyper', 'synth8', 'chop', 'chipmunk+plastic', levels={'fx': 1.}),
 # glitchcore: crushed, stuttering, distorted 808, emo guitar in the verses
 'glitch': hp_song('Bitcrushed_Daydream', 'Bitcrushed Daydream', 150, ['Em', 'C', 'G', 'D'], ['C', 'D', 'Bm', 'Em'],
   [[71,-1,71,74,-1,71,69,-1],[67,-1,-1,0,69,71,-1,0],[71,-1,74,76,-1,74,71,-1],[69,-1,-1,-1,0,0,0,0]],
   [[83,-1,83,-1,81,79,-1,81],[83,-1,0,86,-1,83,0,0],[79,-1,81,83,-1,81,79,76],[78,-1,-1,-1,0,0,0,0]],
   [[72,-1,74,-1,76,-1,79,-1],[78,-1,76,74,-1,0,0,0],[71,-1,74,-1,76,-1,78,-1],[79,-1,-1,-1,-1,-1,0,0]],
   ['emoacoustic'], ['glitchheavy', 'pad'], 'trap', 'heavy808', 'emogtr', 'chipmunk+synth', crush=(24000, 11),
   bridge=dict(keys=['glitchheavy'], bass='heavy808', lead='chop', mel=[[83,0,83,0,83,0,86,-1]] * 4, kind='bridge')),
 # hyper-DnB: 174 bpm drum & bass with chipmunk hooks and supersaw chords
 'dnb': hp_song('Pixel_Heart_DnB', 'Pixel Heart DnB', 174, ['F', 'C', 'Dm', 'Bb'], ['Bb', 'C', 'Am', 'Dm'],
   [[72,-1,-1,74,-1,77,-1,-1],[76,-1,-1,72,-1,-1,0,0],[74,-1,-1,77,-1,81,-1,-1],[79,-1,-1,-1,0,0,0,0]],
   [[81,-1,79,77,-1,79,-1,81],[84,-1,-1,81,-1,79,-1,-1],[77,-1,79,81,-1,82,-1,84],[81,-1,-1,-1,0,0,0,0]],
   [[70,-1,72,-1,74,-1,77,-1],[76,-1,-1,-1,72,-1,-1,-1],[69,-1,72,-1,76,-1,77,-1],[79,-1,-1,-1,-1,-1,0,0]],
   ['pluck', 'pad'], ['futurebass', 'pluck'], 'dnb', 'reese', 'voice', 'chipmunk+synth', dV='breakbeat'),
 # emo hyperpop: sad acoustic verses that blow up into a huge distorted chorus
 'emo': hp_song('Static_Tears', 'Static Tears', 140, ['Bm', 'G', 'D', 'A'], ['G', 'A', 'F#m', 'Bm'],
   [[74,-1,73,71,-1,-1,0,0],[71,-1,73,74,-1,76,-1,-1],[74,-1,73,71,-1,69,-1,-1],[66,-1,-1,-1,0,0,0,0]],
   [[78,-1,78,76,-1,74,-1,76],[78,-1,-1,81,-1,78,-1,-1],[76,-1,74,73,-1,74,-1,71],[73,-1,-1,-1,0,0,0,0]],
   [[67,-1,69,-1,71,-1,74,-1],[73,-1,-1,-1,69,-1,-1,-1],[66,-1,69,-1,73,-1,74,-1],[76,-1,-1,-1,-1,-1,0,0]],
   ['emoacoustic'], ['emoacoustic', 'glitch', 'power'], 'trap', 'heavy808', 'voice', 'chipmunk+voice', dV='halfpop', intro=['emoacoustic'],
   levels={'gtrL': 1.1, 'gtrR': 1.1}),
 # nightcore: sped-up trance energy, gated supersaws, four-on-the-floor
 'nightcore': hp_song('Nightcore_Rush', 'Nightcore Rush', 172, ['C#m', 'A', 'E', 'B'], ['A', 'B', 'G#m', 'C#m'],
   [[73,-1,76,-1,80,-1,78,76],[78,-1,-1,76,-1,73,-1,-1],[73,-1,76,-1,81,-1,80,78],[80,-1,-1,-1,0,0,0,0]],
   [[85,-1,83,81,-1,80,-1,81],[83,-1,-1,80,-1,76,-1,-1],[81,-1,83,85,-1,88,-1,87],[85,-1,-1,-1,0,0,0,0]],
   [[76,-1,78,-1,80,-1,81,-1],[83,-1,-1,-1,80,-1,-1,-1],[76,-1,80,-1,83,-1,85,-1],[87,-1,-1,-1,-1,-1,0,0]],
   ['synthwave'], ['nightcore', 'pad'], 'eurobeat', 'octave', 'chipmunk', 'chipmunk+saw80s'),
}

SONGS['emo']['mus_gap'] = 2.5
SONGS['dnb'].update(ride=.5, cont_tol=-1., targets={'intro': -19., 'verse': -12.8, 'pre': -12.8, 'chorus': -12.3, 'bridge': -13.5})   # no dip after the chorus

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
