"""Platformer world songs in the style of New Super Mario Bros. Wii (original melodies; the style is the inspiration):
one for each world, plus underground, underwater (a waltz), haunted house and castle. Built with popkit.py + newstyles.py.
python mario_worlds.py all  (or: w1 w2 w3 w4 w5 w6 w7 w8 w9 under water ghost castle)"""
import sys
import numpy as np
from newstyles import *
from popkit import build
from songs import render
from songs5 import harp

def button(M, t0, st, S, i, n, tones, root):   # the ending: one hit with the whole band and a 'bah!'
    if i: return
    kick(M, t0, .9); crash(M, t0, .6); bah(M, t0, tones[-1] + 12, 1.1); fbass(M, t0, (root if root < 44 else root - 12), 1.2, .7)
    for c in tones[:3]: brass(M, 'keys', t0, c + 12, 1.1, .2); piano(M, 'keys', t0, c + 12, 1.5, .25)

def world(file, title, bpm, A, B, chA, chB, keys, lead, drums, bass, leadB=None, keysB=None, extra=None, extraB=None, swing=0., levels=None, introkeys=None, introlead=False, verb=2.2):
    s = {'intro': sec(4, chA, keys=introkeys or keys, drums=drums, bass=bass, extra=extra, crash=False,
                      **(dict(lead=lead, mel=[A[0], A[1], [0] * 8, [0] * 8], lv=.8) if introlead else {})),
         'A': sec(8, chA, keys=keys, drums=drums, bass=bass, lead=lead, mel=A, extra=extra, kind='verse'),
         'B': sec(8, chB, keys=keysB or keys, drums=drums, bass=bass, lead=leadB or lead, mel=B, extra=extraB or extra, kind='chorus'),
         'tag': sec(1, [chA[0]], keys=keys, drums=drums, bass=bass, fill=False, kind='chorus'),
         'end': sec(1, [chA[0]], extra=button, fill=False, kind='outro')}
    return dict(file=file, title=title, bpm=bpm, swing=swing, sections=s, order=['intro', 'A', 'B', 'A', 'B', 'tag', 'end'],
                levels=levels or {}, verb=verb, chorus_keys=True)

SONGS = {
 'w1': world('Grassland_Hop', 'Grassland Hop', 150,
   [[72,-1,76,79,-1,76,77,-1],[79,-1,-1,76,-1,72,-1,-1],[74,-1,77,81,-1,79,77,-1],[76,-1,-1,74,-1,0,0,0]],
   [[77,-1,77,76,-1,74,-1,72],[74,-1,-1,79,-1,-1,0,0],[76,-1,76,74,-1,72,-1,71],[72,-1,-1,-1,0,0,0,0]],
   ['C', 'Am', 'F', 'G'], ['F', 'G', 'Em', 'Am'], ['stride', 'steelcomp'], 'steel', 'mario', 'slap', leadB='brass2+xylo',
   extra=bah_at((8, 12), None, 4), swing=.18),
 'w2': world('Desert_Dunes', 'Desert Dunes', 120,
   [[76,-1,77,-1,80,-1,77,76],[77,-1,-1,76,-1,-1,0,0],[80,-1,81,83,-1,81,80,77],[76,-1,-1,-1,0,0,0,0]],
   [[81,-1,83,84,-1,83,81,80],[81,-1,-1,77,-1,-1,0,0],[80,-1,77,76,-1,74,72,-1],[71,-1,-1,-1,-1,-1,0,0]],
   ['E', 'F', 'E', 'Dm'], ['Am', 'Dm', 'E', 'E'], ['oud'], 'oboe', 'darbuka', 'upright', leadB='oboe+oud', keysB=['oud', 'strings'],
   extra=bah_at((12,), None, 4)),
 'w3': world('Snowcap_Slide', 'Snowcap Slide', 112,
   [[77,-1,81,-1,84,-1,81,-1],[82,-1,-1,79,-1,-1,0,0],[79,-1,82,-1,86,-1,84,82],[81,-1,-1,-1,0,0,0,0]],
   [[82,-1,81,79,-1,77,-1,79],[81,-1,-1,77,-1,-1,0,0],[76,-1,77,79,-1,81,-1,82],[84,-1,-1,-1,-1,-1,0,0]],
   ['F', 'Dm', 'Bb', 'C'], ['Bb', 'C', 'Am', 'Dm'], ['celesta', 'pizzarp', 'sleigh'], 'flute', 'brush', 'upright', leadB='strings+celesta',
   extra=bah_at((0,), None, 8, .8), introkeys=['celesta', 'sleigh'], verb=2.8),
 'w4': world('Coconut_Cove', 'Coconut Cove', 124,
   [[79,-1,83,-1,81,79,-1,76],[79,-1,-1,-1,74,-1,-1,-1],[76,-1,79,-1,78,76,-1,74],[74,-1,-1,-1,0,0,0,0]],
   [[84,-1,84,83,-1,81,-1,83],[81,-1,-1,78,-1,74,-1,-1],[83,-1,83,81,-1,79,-1,78],[79,-1,-1,-1,-1,-1,0,0]],
   ['G', 'C', 'D', 'G'], ['C', 'D', 'Bm', 'Em'], ['uke', 'steelcomp'], 'steel', 'calypso', 'slap', leadB='marimba+steel',
   extra=bah_at((6,), None, 2, .8), swing=.12),
 'w5': world('Mushroom_Woods', 'Mushroom Woods', 116,
   [[74,-1,77,-1,76,74,-1,73],[74,-1,-1,69,-1,-1,0,0],[70,-1,74,-1,72,70,-1,69],[73,-1,-1,-1,0,0,0,0]],
   [[77,-1,79,81,-1,79,77,-1],[76,-1,77,79,-1,-1,0,0],[76,-1,74,73,-1,74,76,-1],[74,-1,-1,-1,0,0,0,0]],
   ['Dm', 'Gm', 'A7', 'Dm'], ['Bb', 'C', 'A7', 'Dm'], ['marimbaarp', 'pizzarp'], 'clarinet', 'mario', 'upright', leadB='clarinet+xylo',
   extra=bah_at((10, 14), None, 4, .9), swing=.15),
 'w6': world('Cliffside_Climb', 'Cliffside Climb', 132,
   [[77,-1,-1,82,-1,81,79,-1],[77,-1,-1,74,-1,-1,0,0],[75,-1,79,82,-1,84,82,-1],[81,-1,-1,-1,0,0,0,0]],
   [[82,-1,84,86,-1,84,82,-1],[81,-1,-1,77,-1,-1,0,0],[79,-1,81,82,-1,86,-1,84],[82,-1,-1,-1,-1,-1,0,0]],
   ['Bb', 'F', 'Gm', 'Eb'], ['Eb', 'F', 'Dm', 'Gm'], ['brasshits', 'strings'], 'brass2', 'breakbeat', 'octave', leadB='brass2+strings',
   extra=bah_at((14,), None, 4)),
 'w7': world('Cloudtop_Athletic', 'Cloudtop Athletic', 160,
   [[78,-1,81,-1,-1,78,-1,76],[74,-1,-1,76,-1,78,-1,-1],[79,-1,78,76,-1,74,-1,73],[74,-1,-1,-1,0,0,0,0]],
   [[83,-1,-1,81,-1,79,-1,78],[76,-1,-1,78,-1,81,-1,-1],[81,-1,79,78,-1,76,-1,74],[73,-1,-1,-1,-1,-1,0,0]],
   ['D', 'A', 'Bm', 'G'], ['G', 'A', 'F#m', 'Bm'], ['pizzarp', 'strings'], 'flute', 'mario', 'tuba', leadB='whistle+strings',
   extra=bah_at((12, 14), None, 2), swing=.15, verb=2.6),
 'w8': world('Magma_Fortress', 'Magma Fortress', 132,
   [[72,-1,-1,75,-1,74,72,-1],[68,-1,-1,-1,67,-1,-1,-1],[65,-1,68,72,-1,71,-1,68],[67,-1,-1,-1,0,0,0,0]],
   [[75,-1,77,-1,79,-1,80,-1],[79,-1,-1,77,75,-1,-1,-1],[74,-1,75,77,-1,74,-1,71],[72,-1,-1,-1,-1,-1,0,0]],
   ['Cm', 'Ab', 'Fm', 'G'], ['Ab', 'Bb', 'G', 'Cm'], ['churchorgan', 'dark'], 'brass2', 'castle', 'octave', leadB='brass2+organ', keysB=['churchorgan', 'choir', 'dark'],
   extra=bah_at((8,), None, 4, .9), levels={'organ': .8}),
 'w9': world('Starry_Road', 'Starry Road', 140,
   [[76,-1,80,-1,83,-1,80,81],[83,-1,-1,80,-1,76,-1,-1],[78,-1,81,-1,85,-1,83,81],[80,-1,-1,-1,0,0,0,0]],
   [[85,-1,83,81,-1,80,-1,81],[83,-1,-1,80,-1,78,-1,-1],[81,-1,83,85,-1,88,-1,87],[88,-1,-1,-1,-1,-1,0,0]],
   ['E', 'C#m', 'A', 'B'], ['A', 'B', 'G#m', 'C#m'], ['celesta', 'pad'], 'sqbright', 'mario', 'slap', leadB='sqbright+fmbell', keysB=['celesta', 'synthwave'],
   extra=bah_at((8, 12), None, 4), verb=2.8),
 'under': world('Pipe_Cavern', 'Pipe Cavern', 120,
   [[69,-1,0,72,0,76,0,0],[75,-1,76,-1,0,0,0,0],[74,-1,0,77,0,81,0,0],[80,-1,-1,76,-1,0,0,0]],
   [[77,0,76,0,74,0,72,-1],[71,-1,-1,68,-1,0,0,0],[72,0,74,0,76,0,79,-1],[81,-1,-1,-1,0,0,0,0]],
   ['Am', 'Am', 'Dm', 'E7'], ['F', 'E7', 'Am', 'Am'], [], 'xylo', 'mario', 'slap', leadB='xylo+marimba', keysB=['marimbaarp'],
   extra=bah_at((4, 12), None, 2), swing=.12, levels={'bass': 1.2}),
 'ghost': world('Haunted_Manor', 'Haunted Manor', 96,
   [[69,-1,-1,72,-1,71,-1,70],[69,-1,-1,-1,0,0,0,0],[74,-1,-1,77,-1,76,-1,75],[76,-1,-1,-1,0,0,0,0]],
   [[77,-1,-1,76,-1,74,-1,-1],[73,-1,-1,74,-1,76,-1,-1],[77,-1,76,74,-1,72,-1,71],[69,-1,-1,-1,0,0,0,0]],
   ['Am', 'Dm', 'E7', 'Am'], ['F', 'E7', 'Dm', 'E7'], ['harpsi'], 'theremin', 'swing', 'upright', leadB='theremin+celesta', keysB=['harpsi', 'pad'],
   swing=.25, verb=3.2, levels={'lead': 1.2}),
 'castle': world('Shellfire_Castle', 'Shellfire Castle', 112,
   [[74,-1,-1,77,-1,76,74,-1],[73,-1,-1,-1,69,-1,-1,-1],[70,-1,74,77,-1,76,-1,74],[73,-1,-1,-1,0,0,0,0]],
   [[77,-1,79,-1,81,-1,82,-1],[84,-1,-1,82,81,-1,-1,-1],[81,-1,79,77,-1,76,-1,73],[74,-1,-1,-1,-1,-1,0,0]],
   ['Dm', 'Bb', 'Gm', 'A'], ['Bb', 'C', 'A', 'Dm'], ['churchorgan', 'strings'], 'organ', 'castle', 'octave', leadB='choirbrass', keysB=['churchorgan', 'choir', 'strings'],
   verb=3.),
}

def coral_waltz():   # underwater: a gentle waltz in 3/4 with harp, strings, flute and celesta
    bpm = 150; beat = 60 / bpm; bar = 3 * beat
    prog = ['F', 'Am', 'Bb', 'C', 'F', 'Dm', 'Gm', 'C', 'Bb', 'C', 'Am', 'Dm', 'Gm', 'C', 'F', 'F']
    melA = [(77, 2), (76, 1), (74, 3), (72, 2), (74, 1), (77, 3), (79, 2), (77, 1), (76, 2), (74, 1), (72, 6),
            (77, 2), (79, 1), (81, 3), (82, 2), (81, 1), (79, 3), (77, 2), (76, 1), (74, 2), (76, 1), (77, 6)]
    melB = [(81, 3), (82, 2), (81, 1), (79, 3), (77, 3), (79, 2), (81, 1), (82, 3), (84, 3),
            (82, 2), (81, 1), (79, 3), (77, 2), (76, 1), (74, 3), (76, 3), (77, 6)]
    order = ['intro', 'A', 'B', 'A', 'B', 'end']; nb = {'intro': 4, 'A': 16, 'B': 16, 'end': 2}
    total = sum(nb[o] for o in order); M = Mix(total * bar + 6); b0 = 0
    for o in order:
        mt = b0 * bar
        if o in ('A', 'B'):
            t = mt; prev = None
            for n, L in (melA if o == 'A' else melB):
                flute(M, 'lead', t, n, L * beat * .95, 1.15)
                if o == 'B': celesta(M, 'glock', t, n, L * beat, .5)
                t += L * beat
        for i in range(nb[o]):
            t0 = (b0 + i) * bar; tones, root = chord(prog[i % 16] if o != 'end' else 'F'); r = root if root < 44 else root - 12
            if o == 'end':
                if i == 0:
                    for c in tones: harp(M, t0, c + 12, .8); violins(M, t0, c + 12, 3., .4, att=.4)
                    flute(M, 'lead', t0, 77, 3., 1.); celesta(M, 'glock', t0, 89, 2., .6); fbass(M, t0, r, 2.5, .6)
                continue
            fbass(M, t0, r, beat * 1.8, .55)
            for k, c in enumerate([tones[0] + 12, tones[1] + 12, tones[2] + 12, tones[1] + 12, tones[2] + 12, tones[0] + 24]): harp(M, t0 + k * beat / 2, c, .6, pan=-.3 + .12 * k)
            for bt in (1, 2):
                for c in tones[:3]: pizz(M, t0 + bt * beat, c + 12, .35, pan=.3)
            if i % 2 == 0:
                for c in tones[:3]: violins(M, t0, c + 12, bar * 2 * .97, .3, att=.5, pan=(c % 3 - 1) * .3)
            if o == 'B' and i % 4 == 3: glock(M, t0 + 2 * beat, tones[-1] + 24, .4)
            if i % 8 == 7: M.add('fx', t0, bp(noise(int(1.2 * SR)), 2000, 8000) * np.sin(np.pi * tarr(int(1.2 * SR)) / 1.2) * .03)   # bubbles of air
        b0 += nb[o]
    render(M, 'Coral_Waltz', sends={'lead': .4, 'harp': .45, 'str': .5, 'bass': .1, 'glock': .5, 'fx': .4},
           levels={'lead': 1.1, 'harp': 1.1, 'str': .9, 'bass': .8, 'glock': .9, 'fx': 1.}, duck=(), fade=0.)

if __name__ == '__main__':
    names = (list(SONGS) + ['water']) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names:
        if k == 'water': coral_waltz(); continue
        build(SONGS[k])
