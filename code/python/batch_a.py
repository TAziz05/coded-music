"""Anime, South Arcade-style and metal songs, each with a steady breakcore version.
python batch_a.py all  (or: anime anime_bc south south_bc metal metal_bc)"""
import sys
from popkit import build as pbuild, keys_bar
from breakcore_engine import build as bbuild
from seasons import AMEN, FUNK

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d
def kb(style):   # use a popkit keys style inside the breakcore engine
    return lambda M, t0, st, tones, root, vol, bar: keys_bar(M, style, t0, st, lambda k: k * st, tones, root, vol)

ANIME_CH = [[81,-1,81,83,-1,85,-1,83],[81,-1,-1,78,-1,76,78,-1],[76,-1,78,81,-1,83,-1,85],[86,-1,-1,85,-1,83,-1,-1],
            [81,-1,81,83,-1,85,-1,88],[86,-1,-1,85,-1,83,81,-1],[78,-1,81,-1,83,-1,85,83],[81,-1,-1,-1,-1,-1,0,0]]
SOUTH_CH = [[76,-1,76,79,-1,76,74,-1],[72,-1,-1,74,-1,76,-1,-1],[79,-1,79,81,-1,83,81,79],[78,-1,-1,-1,74,-1,-1,-1]]
METAL_CH = [[76,-1,-1,75,76,-1,79,-1],[77,-1,-1,76,74,-1,72,-1],[71,-1,72,74,-1,76,-1,77],[76,-1,-1,-1,-1,-1,0,0]]

def blocks(rows8):   # 8 bars of eighths -> four 2-bar blocks for the breakcore engine
    flat = [x for r in rows8 for x in r]; ev = []
    for i, x in enumerate(flat):
        if x > 0:
            L = 1
            while i + L < len(flat) and flat[i + L] == -1: L += 1
            ev.append((i * 2, x, L * 2))
    return [[(s - 32 * b, n, min(L, 32 * (b + 1) - s)) for s, n, L in ev if 32 * b <= s < 32 * (b + 1)] for b in range(4)]

SONGS = {
 # anime opening style: fast J-rock, piano runs, strings, a soaring hook, last chorus up a key
 'anime': ('pop', dict(file='Sky_Piercing_Promise', title='Sky-Piercing Promise', bpm=176, chorus_keys=True, sections={
   'intro': sec(4, ['A', 'E', 'F#m', 'D'], keys=['piano', 'strings'], drums='rock', bass='octave', lead='crunch', impact=True,
                mel=[[85,-1,83,81,-1,83,-1,85],[83,-1,-1,-1,80,-1,-1,-1],[81,-1,83,85,-1,88,-1,86],[85,-1,-1,-1,-1,-1,0,0]]),
   'verse': sec(8, ['F#m', 'D', 'A', 'E'], keys=['guitar', 'piano'], drums='halfpop', bass='synth8', lead='voice',
                mel=[[73,-1,73,76,-1,73,71,-1],[69,-1,-1,66,-1,69,71,-1],[73,-1,76,78,-1,76,-1,73],[71,-1,-1,-1,0,0,0,0]]),
   'pre': sec(4, ['D', 'E', 'C#m', 'F#m'], keys=['piano', 'pad'], drums='halfpop', bass='octave', riser=True, lead='voice',
              mel=[[74,-1,76,78,-1,81,-1,-1],[80,-1,78,76,-1,80,-1,-1],[76,-1,78,80,-1,81,-1,83],[85,-1,-1,-1,-1,-1,0,0]]),
   'chorus': sec(8, ['A', 'E', 'F#m', 'D', 'A', 'E', 'D', 'E'], keys=['power', 'strings', 'piano'], drums='punk', bass='octave', lead='strings+crunch', impact=True, mel=ANIME_CH),
   'chorus2': sec(8, ['Bb', 'F', 'Gm', 'Eb', 'Bb', 'F', 'Eb', 'F'], keys=['power', 'strings', 'piano'], drums='punk', bass='octave', lead='strings+crunch', impact=True, up=1, kind='chorus', mel=ANIME_CH),
   'bridge': sec(8, ['D', 'E', 'C#m', 'F#m', 'D', 'E', 'F', 'F'], keys=['piano', 'strings'], drums='halfpop', bass='long', riser=True, lead='voice', kind='bridge',
                 mel=[[78,-1,-1,76,-1,74,-1,-1],[76,-1,-1,78,-1,80,-1,-1],[80,-1,-1,78,-1,76,-1,-1],[73,-1,-1,-1,-1,-1,0,0],[78,-1,-1,76,-1,74,-1,-1],[76,-1,-1,78,-1,80,-1,-1],[81,-1,-1,-1,-1,-1,-1,-1],[0,0,0,0,0,0,0,0]]),
   'outro': sec(2, ['Bb', 'Bb'], keys=['power', 'strings'], drums='rock', fill=False)},
   order=['intro', 'verse', 'pre', 'chorus', 'verse', 'pre', 'chorus', 'bridge', 'chorus2', 'outro'], levels={'lead': 1.2})),
 'anime_bc': ('bc', dict(file='Sky_Piercing_Breaks', title='Sky-Piercing Breaks', bpm=180, chords=['A', 'E', 'F#m', 'D'], keys='piano', pad=.07, mel='strings', melB='crunch', layerB='strings', bass='sub',
   kit=dict(AMEN, crunch=1.8, clap=.3), patA='P1', patB='P2', melody=blocks(ANIME_CH), seed=161, levels={'mel': 1.2})),
 # South Arcade style: Y2K pop-punk with nu-metal riffs and glitchy synth textures
 'south': ('pop', dict(file='Arcade_Heartbreak_2005', title='Arcade Heartbreak 2005', bpm=150, sections={
   'intro': sec(4, ['Em', 'C', 'G', 'D'], keys=['glitch'], riser=True),
   'verse': sec(8, ['Em', 'C', 'G', 'D'], keys=['chug', 'glitch'], drums='rock', bass='metalbass', lead='voice', kv=.8,
                mel=[[71,-1,71,74,-1,71,69,-1],[67,-1,-1,71,-1,-1,0,0],[71,-1,74,76,-1,74,-1,71],[69,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Em', 'C', 'G', 'D'], keys=['power', 'glitch'], drums='punk', bass='octave', lead='crunch+voice', hey=True, impact=True, mel=SOUTH_CH),
   'break': sec(4, ['Em', 'Em', 'C', 'D'], keys=['chug'], drums='metal', bass='metalbass', kind='verse'),
   'outro': sec(2, ['Em', 'Em'], keys=['power'], drums='rock', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'break', 'chorus', 'outro'], levels={'lead': 1.2})),
 'south_bc': ('bc', dict(file='Arcade_Heartbreak_Breaks', title='Arcade Heartbreak Breaks', bpm=172, chords=['Em', 'C', 'G', 'D'], keys=kb('glitch'), pad=.05, mel='crunch', melB='crunch', layerB='voice', bass='808',
   kit=dict(FUNK, crunch=2.2, clap=.4, punch=1.3), patA='P4', patB='P2', melody=blocks(SOUTH_CH * 2), seed=171, levels={'mel': 1.2},
   ending='tapestop', stop_bar=4, sections=[('intro', 8), ('build', 4), ('dropA', 16), ('half', 8), ('dropB', 16), ('outro', 6)], targets={'outro': -12.5})),
 # heavy metal: double kick, chugs, tremolo picking, a screaming lead
 'metal': ('pop', dict(file='Iron_Storm_Rising', title='Iron Storm Rising', bpm=168, sections={
   'intro': sec(4, ['Em', 'C', 'D', 'B'], keys=['tremolo'], drums='metal', bass='metalbass', riser=True),
   'verse': sec(8, ['Em', 'Em', 'C', 'D'], keys=['chug'], drums='metal', bass='metalbass'),
   'chorus': sec(8, ['Em', 'C', 'D', 'B'], keys=['power', 'tremolo'], drums='metal', bass='metalbass', lead='metal', impact=True, mel=METAL_CH),
   'solo': sec(8, ['Am', 'Em', 'C', 'B'], keys=['chug'], drums='metal', bass='metalbass', lead='metal', kind='chorus',
               mel=[[81,79,81,83,-1,81,79,76],[79,78,76,-1,74,76,-1,-1],[76,78,79,81,83,84,83,81],[83,-1,-1,-1,-1,-1,0,0]]),
   'outro': sec(2, ['Em', 'Em'], keys=['power'], drums='rock', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'solo', 'chorus', 'outro'], levels={'lead': 1.3, 'gtrL': 1.6, 'gtrR': 1.6})),
 'metal_bc': ('bc', dict(file='Iron_Storm_Breaks', title='Iron Storm Breaks', bpm=176, chords=['Em', 'C', 'D', 'B'], keys=kb('power'), pad=.04, mel='crunch', melB='crunch', layerB='crunch', bass='reese',
   kit=dict(AMEN, crunch=2.8, clap=.3, punch=1.4), patA='P2', patB='P4', melody=blocks(METAL_CH * 2), seed=181, levels={'mel': 1.3, 'gtrL': 1.6, 'gtrR': 1.6})),
}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names:
        kind, cfg = SONGS[k]
        (pbuild if kind == 'pop' else bbuild)(cfg)
