"""Turns TAziz322's coded songs into Loop Lab songs (simplified to fit Loop Lab's sections)
and builds loop-lab/index.html from template.html. Run: python loop-lab/tools/make_presets.py"""
import json

def mel(rows, bars=None):
    """8 eighth-notes per bar (-1 hold, 0 rest) -> note events on a 16-step grid."""
    flat = [x for r in rows for x in r]; ev = []
    for i, x in enumerate(flat):
        if x > 0:
            L = 1
            while i + L < len(flat) and flat[i + L] == -1: L += 1
            ev.append([i * 2, x, L * 2])
    return ev

def drums(bars, **rows):
    """rows given as 16-char strings (one bar), repeated for every bar."""
    out = {}
    for k in ['kick', 'snare', 'clap', 'rim', 'hat', 'open', 'crash']:
        p = rows.get(k, '.' * 16)
        if len(p) == 16: p = p * bars
        out[k] = p
    return out

def sec(name, bars, chords, melody=None, dr=None, chordStyle='pad', bass='root8', sfx=None):
    return {'name': name, 'bars': bars, 'chords': chords, 'melody': melody or [], 'drums': dr or drums(bars),
            'chordStyle': chordStyle, 'bass': bass, 'sfx': sfx or []}

def crash_first(d):
    d['crash'] = 'x' + d['crash'][1:]; return d

P = []

# ---------- Victory Rush ----------
lead = mel([[72,0,72,74,76,0,74,72],[74,0,74,76,79,0,76,74],[76,0,79,0,83,81,79,76],[81,-1,-1,79,76,-1,74,76],
            [72,0,72,74,76,0,77,76],[74,0,79,0,79,81,83,-1],[84,-1,83,79,76,-1,79,83],[81,-1,-1,-1,-1,0,0,0]])
four = dict(kick='x...x...x...x...', clap='....x.......x...', hat='xx.xxx.xxx.xxx.x', open='..x...x...x...x.')
P.append({'name': 'Victory Rush', 'bpm': 128, 'swing': 0, 'kit': 'band', 'lead': 'brass', 'scaleRoot': 'C', 'scale': 'major',
  'sections': [sec('Intro', 4, ['F', 'G', 'Em', 'Am'], dr=drums(4, hat='.x.x.x.x.x.x.x.x'), chordStyle='pad', bass='off', sfx=[[48, 'riser']]),
               sec('Verse', 4, ['F', 'G', 'Em', 'Am'], dr=drums(4, **four), chordStyle='arp', bass='offbeat'),
               sec('Chorus', 8, ['F', 'G', 'Em', 'Am'] * 2, melody=lead, dr=crash_first(drums(8, **four)), chordStyle='stabs', bass='offbeat', sfx=[[0, 'impact']]),
               sec('Break', 4, ['F', 'G', 'Em', 'Am'], dr=drums(4, kick='x.......x.......'), chordStyle='pad', bass='long', sfx=[[48, 'riser']])],
  'arrangement': [0, 1, 1, 2, 3, 2, 0]})

# ---------- Storm Closing ----------
lead = mel([[69,72,76,-1,74,72,71,72],[72,-1,69,-1,65,-1,69,72],[74,-1,71,-1,67,71,74,76],[76,-1,-1,-1,74,-1,71,-1],
            [69,72,76,-1,74,72,71,72],[77,-1,76,-1,72,-1,69,72],[74,-1,76,-1,79,-1,74,-1],[76,-1,80,-1,83,-1,-1,-1]])
vd = dict(kick='x......x..x.....', snare='....x.......x...', hat='xxxxxxxxxxxxxxxx')
cd = dict(kick='x...x...x...x...', snare='....x.......x...', clap='............x...', hat='xxxxxxxxxxxxxxxx')
P.append({'name': 'Storm Closing', 'bpm': 140, 'swing': 0, 'kit': 'band', 'lead': 'brass', 'scaleRoot': 'A', 'scale': 'minor',
  'sections': [sec('Intro', 4, ['Am', 'F', 'C', 'G'], dr=drums(4, hat='xxxxxxxxxxxxxxxx'), chordStyle='arp', bass='off', sfx=[[48, 'riser']]),
               sec('Verse', 4, ['Am', 'F', 'C', 'G'], dr=drums(4, **vd), chordStyle='arp', bass='octave'),
               sec('Chorus', 8, ['Am', 'F', 'G', 'E'] * 2, melody=lead, dr=crash_first(drums(8, **cd)), chordStyle='stabs', bass='pump16', sfx=[[0, 'impact']]),
               sec('Break', 4, ['Am', 'F', 'G', 'E'], dr=drums(4, kick='x...............'), chordStyle='pad', bass='long', sfx=[[48, 'riser']])],
  'arrangement': [0, 1, 2, 3, 2, 0]})

# ---------- Lobby Loop ----------
A = mel([[72,0,69,72,76,-1,74,72],[71,-1,67,-1,71,74,76,-1],[77,-1,76,74,72,-1,69,-1],[71,-1,72,-1,67,-1,-1,0],
         [72,0,69,72,76,-1,79,77],[76,-1,74,-1,71,74,-1,76],[74,-1,72,69,72,-1,74,-1],[72,-1,-1,-1,0,0,0,0]])
B = mel([[81,-1,79,-1,76,-1,72,-1],[79,-1,76,-1,74,-1,71,-1],[77,-1,76,-1,74,72,69,-1],[71,-1,72,74,76,-1,-1,-1],
         [81,-1,79,-1,76,77,79,-1],[79,-1,76,-1,74,76,79,-1],[77,-1,74,-1,72,-1,74,76],[76,-1,-1,-1,0,0,0,0]])
ld = dict(kick='x......x..x.....', clap='....x.......x...', snare='............x...', hat='x.x.x.x.x.x.x.x.')
P.append({'name': 'Lobby Loop', 'bpm': 102, 'swing': .16, 'kit': 'band', 'lead': 'soft', 'scaleRoot': 'C', 'scale': 'major',
  'sections': [sec('Intro', 4, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], chordStyle='ep', bass='off'),
               sec('A', 8, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'] * 2, melody=A, dr=drums(8, **ld), chordStyle='ep', bass='funky'),
               sec('B', 8, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'] * 2, melody=B, dr=drums(8, **ld), chordStyle='ep', bass='funky')],
  'arrangement': [0, 1, 1, 2, 2, 1, 0]})

# ---------- Channel Plaza ----------
A = mel([[72,-1,69,72,-1,76,-1,74],[72,-1,-1,69,-1,67,-1,64],[65,-1,69,-1,72,74,-1,77],[76,-1,74,-1,70,-1,-1,0],
         [72,-1,69,72,-1,76,-1,79],[77,-1,76,-1,72,-1,69,-1],[70,-1,74,-1,77,-1,74,72],[70,-1,-1,-1,67,-1,-1,-1]])
B = mel([[74,-1,72,70,-1,67,-1,70],[72,-1,-1,-1,0,70,72,74],[76,-1,72,-1,69,-1,72,-1],[74,-1,-1,-1,0,0,0,0],
         [74,-1,77,-1,74,-1,70,-1],[76,-1,74,-1,72,-1,70,-1],[72,-1,76,-1,79,-1,76,-1],[78,-1,-1,-1,0,0,0,0]])
bd = dict(kick='x.....x.x.....x.', rim='x..x..x...x.x...', hat='xxxxxxxxxxxxxxxx')
P.append({'name': 'Channel Plaza', 'bpm': 116, 'swing': 0, 'kit': 'band', 'lead': 'marimba', 'scaleRoot': 'F', 'scale': 'major',
  'sections': [sec('Intro', 4, ['Fmaj7', 'Am7', 'Bbmaj7', 'C7'], dr=drums(4, hat='xxxxxxxxxxxxxxxx'), chordStyle='ep', bass='off'),
               sec('A', 8, ['Fmaj7', 'Am7', 'Bbmaj7', 'C7'] * 2, melody=A, dr=drums(8, **bd), chordStyle='ep', bass='bossa'),
               sec('B', 8, ['Gm7', 'C7', 'Fmaj7', 'Dm7', 'Gm7', 'C7', 'Am7', 'D7'], melody=B, dr=drums(8, **bd), chordStyle='ep', bass='bossa')],
  'arrangement': [0, 1, 2, 1, 2, 0]})

# ---------- Frosty Podium ----------
A = mel([[67,-1,72,-1,76,-1,79,-1],[79,-1,77,76,-1,74,-1,-1],[76,-1,72,-1,69,-1,72,76],[77,-1,-1,-1,76,-1,74,-1],
         [74,-1,77,-1,81,-1,77,-1],[79,-1,-1,77,-1,74,71,-1],[72,-1,76,-1,79,-1,84,-1],[84,-1,-1,-1,0,0,0,0]])
B = mel([[81,-1,79,-1,77,-1,76,-1],[74,-1,76,-1,77,-1,79,-1],[79,-1,76,-1,71,-1,76,-1],[72,-1,-1,-1,76,-1,81,-1],
         [77,-1,81,-1,86,-1,84,-1],[83,-1,81,-1,79,-1,77,74],[76,-1,79,-1,84,-1,-1,-1],[0,0,0,0,0,0,0,0]])
fd = dict(kick='x.......x.......', snare='....x.......x...', hat='xxxxxxxxxxxxxxxx')
bells = lambda bars: [[s, 'bells'] for s in range(0, bars * 16, 2)]
P.append({'name': 'Frosty Podium', 'bpm': 150, 'swing': 0, 'kit': 'band', 'lead': 'brass', 'scaleRoot': 'C', 'scale': 'major',
  'sections': [sec('Fanfare', 2, ['C', 'G'], melody=[[0, 67, 2], [2, 67, 2], [4, 72, 4], [8, 76, 4], [12, 79, 4], [16, 79, 8], [24, 84, 8]],
                   dr=drums(2, snare='x...x...x...x...'), chordStyle='stabs', bass='off', sfx=bells(2) + [[0, 'impact']]),
               sec('A', 8, ['C', 'G', 'Am', 'F', 'Dm', 'G', 'C', 'C'], melody=A, dr=crash_first(drums(8, **fd)), chordStyle='pad', bass='octave', sfx=bells(8)),
               sec('B', 8, ['F', 'G', 'Em', 'Am', 'Dm', 'G', 'C', 'G'], melody=B, dr=drums(8, **fd), chordStyle='pad', bass='octave', sfx=bells(8))],
  'arrangement': [0, 1, 2, 1, 0]})

# ---------- Coastal Route ----------
A = mel([[74,-1,71,74,79,-1,78,76],[78,-1,76,-1,71,-1,67,-1],[72,-1,76,-1,79,-1,76,72],[74,-1,-1,-1,0,74,76,78],
         [79,-1,78,79,81,-1,79,78],[78,-1,74,-1,71,-1,74,78],[76,-1,72,76,79,-1,84,-1],[81,-1,-1,-1,-1,-1,0,0]])
B = mel([[72,-1,76,-1,81,-1,79,76],[78,-1,-1,74,-1,-1,69,-1],[71,-1,74,-1,79,-1,78,79],[76,-1,-1,-1,0,71,74,76],
         [76,-1,72,-1,79,-1,76,-1],[78,-1,74,-1,81,-1,78,-1],[79,-1,-1,78,-1,-1,76,-1],[74,-1,-1,-1,0,0,0,0]])
rd = dict(kick='x.....x.x..x....', snare='....x.......x...', hat='x.x.x.x.x.x.x.x.')
P.append({'name': 'Coastal Route', 'bpm': 132, 'swing': 0, 'kit': 'chip', 'lead': 'trumpet', 'scaleRoot': 'G', 'scale': 'major',
  'sections': [sec('Intro', 2, ['G', 'D'], dr=drums(2, **rd), chordStyle='chip', bass='octave'),
               sec('A', 8, ['G', 'Em', 'C', 'D', 'G', 'Bm', 'C', 'D'], melody=A, dr=drums(8, **rd), chordStyle='chip', bass='octave'),
               sec('B', 8, ['Am', 'D', 'G', 'Em', 'C', 'D', 'Em', 'D'], melody=B, dr=drums(8, **rd), chordStyle='chip', bass='octave')],
  'arrangement': [0, 1, 2, 1]})

# ---------- Determined Steps (piano) ----------
A = mel([[74,-1,77,74,76,-1,72,-1],[74,-1,70,-1,72,74,-1,77],[79,-1,77,76,-1,72,-1,76],[76,-1,-1,73,-1,-1,69,-1],
         [74,-1,77,74,76,-1,81,-1],[79,-1,77,-1,74,77,-1,82],[81,-1,79,77,-1,76,-1,72],[73,-1,76,-1,81,-1,-1,-1]])
B = mel([[70,-1,-1,74,-1,-1,79,-1],[77,-1,76,74,-1,-1,69,-1],[70,-1,72,74,-1,77,-1,74],[76,-1,-1,-1,73,-1,-1,-1],
         [72,-1,-1,77,-1,-1,81,-1],[79,-1,77,76,-1,-1,72,-1],[74,-1,77,-1,79,-1,82,-1],[81,-1,-1,-1,-1,-1,0,0]])
P.append({'name': 'Determined Steps', 'bpm': 120, 'swing': 0, 'kit': 'band', 'lead': 'piano', 'scaleRoot': 'D', 'scale': 'minor',
  'sections': [sec('A', 8, ['Dm', 'Bb', 'C', 'A'] * 2, melody=A, chordStyle='piano', bass='walk'),
               sec('B', 8, ['Gm', 'Dm', 'Bb', 'A', 'F', 'C', 'Bb', 'A'], melody=B, chordStyle='piano', bass='walk')],
  'arrangement': [0, 1, 0]})

# ---------- Static Weather ----------
V = mel([[0,74,-1,73,71,-1,69,-1],[71,-1,-1,0,66,69,71,-1],[74,-1,76,-1,78,-1,76,74],[73,-1,-1,-1,0,0,69,71],
         [74,-1,73,71,-1,69,71,-1],[74,-1,-1,0,76,-1,74,71],[69,-1,71,-1,74,-1,73,71],[69,-1,-1,-1,0,0,0,0]])
K = mel([[78,-1,79,78,-1,74,76,-1],[76,-1,78,76,-1,73,74,-1],[73,-1,74,76,-1,78,81,-1],[78,-1,-1,-1,76,-1,74,-1],
         [78,-1,79,81,-1,79,78,-1],[76,-1,78,79,-1,78,76,-1],[74,-1,76,73,-1,74,69,-1],[71,-1,-1,-1,-1,-1,0,0]])
sv = dict(kick='x.......x.x.....', snare='....x.......x...', hat='x.x.x.x.x.x.x.x.')
sc = dict(kick='x.....x.x.......', snare='....x.......x...', hat='x.x.x.x.x.x.x.x.', open='.x.x.x.x.x.x.x.x')
P.append({'name': 'Static Weather', 'bpm': 146, 'swing': 0, 'kit': 'band', 'lead': 'voice', 'scaleRoot': 'D', 'scale': 'major',
  'sections': [sec('Intro', 4, ['Bm', 'G', 'D', 'A'], chordStyle='guitar', bass='off'),
               sec('Verse', 8, ['Bm', 'G', 'D', 'A'] * 2, melody=V, dr=drums(8, **sv), chordStyle='guitar', bass='root8'),
               sec('Chorus', 8, ['G', 'A', 'F#m', 'Bm'] * 2, melody=K, dr=crash_first(drums(8, **sc)), chordStyle='strum', bass='octave', sfx=[[0, 'impact']])],
  'arrangement': [0, 1, 2, 1, 2, 0]})

snd = {'Determined Steps': 'piano', 'Coastal Route': 'chip', 'Channel Plaza': 'finger', 'Static Weather': 'finger', 'Lobby Loop': 'finger'}
for p in P:
    p['bassSound'] = snd.get(p['name'], 'synth')
    for s in p['sections']: assert len(s['chords']) == s['bars'], (p['name'], s['name'])
# build loop-lab/index.html from the template with the songs baked in
import os
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, 'template.html')).read()
open(os.path.join(here, '..', 'index.html'), 'w').write(tpl.replace('__PRESETS__', json.dumps(P, separators=(',', ':'))))
print(len(P), 'songs built into loop-lab/index.html')
