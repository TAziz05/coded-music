"""Original songs for each album era of CORTIS and TOMORROW X TOGETHER (TXT): each one borrows the general sound of
that album's era (genre, tempo, instruments), with new melodies and chords. All sounds are code.
python kpop_albums.py all  (or keys from SONGS)"""
import sys
import numpy as np
from newstyles import *
from popkit import build
from songs5 import harp
from popkit import hey
from songs4 import dist_gtr, power

def chain(*fs):
    def f(*a):
        for g in fs:
            if g: g(*a)
    return f

def boom_tail(M, t, n, dur, vol):   # an 808 that dies away instead of stopping
    N = int(dur * SR); tt = tarr(N); f = mtof(n) * (1 + 1.2 * np.exp(-tt / .015))
    M.add('sub', t, np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 1.8) * np.exp(-tt / (dur / 4)) * np.minimum(1, tt / .003) * vol * .5)
# ---------------- endings (each song ends its own way) ----------------
def end_stab(M, t0, st, S, i, n, tones, root):      # one short band hit
    if i: return
    kick(M, t0, .8); crash(M, t0, .4)
    for c in tones[:3]: supersaw(M, 'keys', t0, c + 12, .35, .06, cut=3000, a=.003, r=.25, voices=4)
def end_chant(M, t0, st, S, i, n, tones, root):     # a group 'hey!' and a bass drop
    if i: return
    hey(M, t0, .7); boom_tail(M, t0, root, 2.5, .8)
def end_ring(M, t0, st, S, i, n, tones, root):      # a bright chord that rings out with bells
    if i: return
    for c in tones[:3]: supersaw(M, 'pad', t0, c + 12, 3., .04, cut=2500, a=.02, r=2.5, voices=3); celesta(M, 'glock', t0 + .1 * (c % 3), c + 24, 2.5, .5)
def end_guitar(M, t0, st, S, i, n, tones, root):    # a last strummed chord, let ring
    if i: return
    kick(M, t0, .8); crash(M, t0, .5)
    for b, pn in (('gtrL', -.6), ('gtrR', .6)): dist_gtr(M, b, t0, power(root + 24 if root < 44 else root + 12), 2.5, .25, pan=pn, gain=4., warm=True)
def end_music_box(M, t0, st, S, i, n, tones, root):  # the beat stops; a music box plays the chord slowly
    if i: return
    for k, c in enumerate(tones[:3] + [tones[0] + 12]): celesta(M, 'glock', t0 + k * 4 * st, c + 12, 2., .6)
def end_drop_out(M, t0, st, S, i, n, tones, root):  # just the bass and a kick, then nothing
    if i: return
    kick(M, t0, .7); boom_tail(M, t0, root, 3., .8)

def song(file, title, bpm, chA, chB, A, B, keys, drums, bass, lead, ending, keysB=None, leadB=None, drumsB=None, bassB=None,
         intro_keys=None, swing=0., extra=None, extraB=None, bridge=None, levels=None, **cfg):
    s = {'intro': sec(4, chA, keys=intro_keys or keys[-1:], extra=extra),
         'verse': sec(8, chA, keys=keys, drums=drums, bass=bass, lead=lead, mel=A, extra=extra, kind='verse'),
         'chorus': sec(8, chB, keys=keysB or keys, drums=drumsB or drums, bass=bassB or bass, lead=leadB or lead, mel=B, extra=extraB or extra, impact=True, kind='chorus'),
         'end': sec(1, chA[:1], extra=ending, fill=False, kind='outro')}
    order = ['intro', 'verse', 'chorus', 'verse', 'chorus', 'end']
    if bridge:
        s['bridge'] = sec(4, bridge, keys=keys[-1:], lead=lead, mel=A[:2] + A[:2], kind='bridge'); order = ['intro', 'verse', 'chorus', 'bridge', 'chorus', 'end']
    d = dict(file=file, title=title, bpm=bpm, swing=swing, sections=s, order=order, chorus_keys=True, cont_tol=0., levels=levels or {})
    d.update(cfg); return d

R = -1
SONGS = {
 # ---- CORTIS ----
 'cortis1': song('Outside_the_Lines', 'Outside the Lines', 98, ['Dm', 'Bb', 'C', 'Am'], ['Bb', 'C', 'Dm', 'Dm'],
   [[74,R,0,72,R,69,0,0],[72,R,R,69,R,67,0,0],[74,R,0,72,R,74,77,R],[76,R,R,R,0,0,0,0]],
   [[81,R,81,79,R,77,R,0],[79,R,R,77,R,74,0,0],[77,R,79,81,R,84,R,81],[81,R,R,R,0,0,0,0]],
   ['guitar', 'pad'], 'boombap', '808', 'whistle', end_chant, leadB='whistle+synth', extraB=lambda M, t0, st, S, i, n, T, r: i % 2 == 1 and hey(M, t0 + S(12), .7),
   swing=.08),
 'cortis2': song('Green_Light_Crew', 'Green Light Crew', 146, ['Gm', 'Eb', 'Cm', 'D'], ['Eb', 'F', 'Gm', 'D'],
   [[67,R,70,R,0,67,72,R],[70,R,R,67,R,65,0,0],[67,R,70,R,72,R,74,R],[74,R,R,R,0,0,0,0]],
   [[79,R,79,R,77,R,74,R],[77,R,R,74,R,72,R,R],[74,R,77,R,79,R,82,R],[81,R,R,R,0,0,0,0]],
   ['glitchheavy', 'pad'], 'trap', 'heavy808', 'saw80s', end_drop_out, leadB='saw80s+sqbright', keysB=['brasshits', 'pad']),
 # ---- TXT ----
 'star': song('First_Crown', 'First Crown', 118, ['A', 'E', 'F#m', 'D'], ['D', 'E', 'C#m', 'F#m'],
   [[76,R,78,R,81,R,78,76],[78,R,R,76,R,73,0,0],[73,R,76,R,78,R,81,R],[80,R,R,R,0,0,0,0]],
   [[85,R,83,81,R,83,R,85],[86,R,R,85,R,81,R,R],[81,R,83,R,85,R,88,R],[85,R,R,R,0,0,0,0]],
   ['pluck', 'pad'], 'fourfloor', 'octave', 'sqbright', end_ring, keysB=['futurebass', 'pad'], leadB='sqbright+celesta'),
 'magic': song('Platform_Nine', 'Platform Nine', 124, ['C', 'G', 'Am', 'F'], ['F', 'G', 'Em', 'Am'],
   [[72,R,74,76,R,79,R,0],[76,R,74,72,R,R,0,0],[69,R,72,74,R,76,R,79],[76,R,R,R,0,0,0,0]],
   [[84,R,83,R,79,R,76,R],[77,R,79,R,R,76,0,0],[76,R,77,79,R,84,R,83],[81,R,R,R,0,0,0,0]],
   ['marimbaarp', 'pad'], 'house', 'octave', 'whistle', end_music_box, leadB='marimba+whistle'),
 'eternity': song('Eternity_Glass', 'Eternity Glass', 102, ['Am', 'F', 'G', 'Em'], ['F', 'G', 'Am', 'Am'],
   [[69,R,0,72,R,71,69,R],[67,R,R,64,R,R,0,0],[69,R,0,72,R,74,76,R],[74,R,R,R,0,0,0,0]],
   [[81,R,79,R,76,R,79,81],[79,R,R,76,R,74,R,R],[72,R,74,R,76,R,79,R],[76,R,R,R,0,0,0,0]],
   ['nylon', 'pad'], 'dembow', 'sub', 'flute', end_stab, leadB='flute+synth', keysB=['dembowpluck', 'pad']),
 'bluehour': song('Blue_Hour_Disco', 'Blue Hour Disco', 120, ['Fmaj7', 'Em7', 'Dm7', 'C'], ['Dm7', 'Em7', 'Fmaj7', 'G'],
   [[72,R,74,R,76,R,77,76],[74,R,R,72,R,69,0,0],[72,R,74,R,76,R,79,R],[77,R,R,R,0,0,0,0]],
   [[81,R,79,R,77,R,76,R],[77,R,79,R,R,76,R,74],[76,R,77,R,79,R,81,R],[79,R,R,R,0,0,0,0]],
   ['funk', 'strings'], 'funk', 'funky', 'synth', end_stab, leadB='synth+strings', fadeout=6.),
 'freeze': song('Frozen_Clock', 'Frozen Clock', 162, ['E', 'B', 'C#m', 'A'], ['A', 'B', 'C#m', 'B'],
   [[76,R,76,R,78,R,80,R],[78,R,R,76,R,73,0,0],[73,R,76,R,78,R,80,R],[78,R,R,R,0,0,0,0]],
   [[83,R,R,81,R,80,R,R],[80,R,81,R,80,R,76,R],[78,R,80,R,81,R,83,R],[83,R,R,R,0,0,0,0]],
   ['power'], 'punk', 'octave', 'crunch', end_guitar, levels={'gtrL': .9, 'gtrR': .9}),
 'fight': song('Escape_Route', 'Escape Route', 170, ['Bm', 'G', 'D', 'A'], ['G', 'A', 'Bm', 'Bm'],
   [[71,R,74,R,R,71,74,R],[76,R,R,74,R,71,0,0],[71,R,74,R,76,R,78,R],[76,R,R,R,0,0,0,0]],
   [[83,R,81,R,78,R,81,83],[86,R,R,83,R,81,R,R],[78,R,81,R,83,R,86,R],[83,R,R,R,0,0,0,0]],
   ['power', 'organ'], 'rock', 'octave', 'crunch', end_stab, leadB='crunch+organ', levels={'gtrL': .9, 'gtrR': .9}, tapestop=True),
 'thursday': song('Thursday_Child', "Thursday's Child", 112, ['Em', 'C', 'Am', 'B'], ['C', 'D', 'Em', 'B'],
   [[64,R,67,R,71,R,R,0],[69,R,67,R,66,R,0,0],[64,R,67,R,71,R,72,R],[71,R,R,R,0,0,0,0]],
   [[76,R,R,74,R,72,R,71],[72,R,R,71,R,69,R,R],[71,R,72,R,74,R,76,R],[75,R,R,R,0,0,0,0]],
   ['darkgtr', 'pad'], 'rock', 'metalbass', 'emogtr', end_drop_out, keysB=['power', 'pad']),
 'temptation': song('Neverland_Rush', 'Neverland Rush', 100, ['Db', 'Ab', 'Bbm', 'Gb'], ['Gb', 'Ab', 'Fm', 'Bbm'],
   [[73,R,75,R,77,R,80,R],[77,R,R,75,R,73,0,0],[70,R,73,R,75,R,77,R],[75,R,R,R,0,0,0,0]],
   [[85,R,84,R,80,R,77,R],[80,R,R,77,R,75,R,R],[77,R,80,R,82,R,85,R],[84,R,R,R,0,0,0,0]],
   ['dembowpluck', 'pad'], 'dembow', 'sub', 'flute', end_music_box, leadB='flute+celesta', keysB=['plastic', 'pad']),
 'freefall': song('Freefall_Chase', 'Freefall Chase', 150, ['F#m', 'D', 'A', 'E'], ['D', 'E', 'F#m', 'F#m'],
   [[73,R,R,76,R,78,R,R],[76,R,73,R,71,R,0,0],[73,R,R,76,R,78,R,81],[80,R,R,R,0,0,0,0]],
   [[85,R,R,83,R,81,R,R],[83,R,81,R,78,R,R,R],[81,R,83,R,85,R,88,R],[85,R,R,R,0,0,0,0]],
   ['synthwave', 'pad'], 'gated', 'synth8', 'saw80s', end_ring, leadB='saw80s+sqbright', echo_out=(8, .5, 6)),
 'tomorrow': song('Tomorrow_Again', 'Tomorrow Again', 134, ['G', 'D', 'Em', 'C'], ['C', 'D', 'Em', 'C'],
   [[74,R,76,R,79,R,R,76],[74,R,R,71,R,R,0,0],[71,R,74,R,76,R,79,R],[78,R,R,R,0,0,0,0]],
   [[83,R,R,81,R,79,R,R],[81,R,79,R,76,R,R,R],[79,R,81,R,83,R,86,R],[83,R,R,R,0,0,0,0]],
   ['emoacoustic', 'pad'], 'rock', 'octave', 'emogtr', end_guitar, keysB=['power', 'pad'], intro_keys=['emoacoustic']),
 'sanctuary': song('Moonward', 'Moonward', 128, ['D', 'A', 'Bm', 'G'], ['G', 'A', 'D', 'D'],
   [[74,R,76,R,78,R,81,R],[78,R,R,76,R,74,0,0],[71,R,74,R,76,R,78,R],[76,R,R,R,0,0,0,0]],
   [[86,R,85,R,81,R,78,R],[81,R,R,83,R,85,R,R],[83,R,85,R,86,R,88,R],[86,R,R,R,0,0,0,0]],
   ['guitar', 'celesta'], 'fourfloor', 'octave', 'synth', end_ring, leadB='synth+celesta'),
 'together': song('Strangers_Together', 'Strangers Together', 156, ['C', 'G', 'Am', 'F'], ['F', 'G', 'C', 'Am'],
   [[72,R,72,R,74,R,76,R],[74,R,R,72,R,69,0,0],[69,R,72,R,74,R,76,R],[74,R,R,R,0,0,0,0]],
   [[79,R,R,77,R,76,R,R],[77,R,76,R,72,R,R,R],[76,R,77,R,79,R,84,R],[79,R,R,R,0,0,0,0]],
   ['uke', 'pad'], 'punk', 'octave', 'guitar', end_chant, keysB=['power', 'pad'], levels={'gtrL': .8, 'gtrR': .8}),
 'thorns': song('Stillness_in_the_Thorns', 'Stillness in the Thorns', 122, ['Cm', 'Ab', 'Eb', 'Bb'], ['Ab', 'Bb', 'Cm', 'Cm'],
   [[72,R,0,75,R,72,70,R],[72,R,R,0,0,67,0,0],[72,R,0,75,R,77,79,R],[77,R,R,R,0,0,0,0]],
   [[79,R,79,R,77,R,75,R],[77,R,R,75,R,72,R,R],[75,R,77,R,79,R,82,R],[79,R,R,R,0,0,0,0]],
   ['ep', 'pad'], 'house', 'funky', 'vocoder', end_stab, leadB='vocoder+synth', keysB=['stabs', 'pad'], bridge=['Fm', 'Gm', 'Ab', 'Bb']),
}
for k in SONGS: SONGS[k].setdefault('gain_like', {'end': 'chorus'})

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
