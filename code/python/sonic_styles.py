"""Songs in the different musical styles of the Sonic series (original melodies; style only). Built with popkit.py.
python sonic_styles.py all  (or: genesis cd adventure hiphop rush jazz colors frontiers)"""
import sys
from popkit import build

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d
def song(file, title, bpm, A, B, chA, chB, keys, lead, drums, bass, leadB=None, keysB=None, drumsB=None, swing=0, crush=None, introkeys=None, heyB=False, scratch=False, levels=None, bars=8):
    s = {'intro': sec(4, chA, keys=introkeys or keys, drums=drums if not introkeys else None, bass=None if introkeys else bass, riser=True, crash=False),
         'A': sec(bars, chA, keys=keys, drums=drums, bass=bass, lead=lead, mel=A, scratch=scratch, kind='verse'),
         'B': sec(bars, chB, keys=keysB or keys, drums=drumsB or drums, bass=bass, lead=leadB or lead, mel=B, hey=heyB, scratch=scratch, impact=True, kind='chorus'),
         'outro': sec(2, [chA[0], chA[0]], keys=keys, drums=drums, fill=False)}
    return dict(file=file, title=title, bpm=bpm, swing=swing, crush=crush, sections=s, order=['intro', 'A', 'B', 'A', 'B'] + (['A', 'B'] if bpm >= 140 else []) + ['outro'], levels=levels or {})

SONGS = {
 # Classic Genesis: FM synth lead, slap FM bass, punchy drums, 16-bit crunch
 'genesis': song('Emerald_Shore_Zone', 'Emerald Shore Zone', 142,
   [[72,-1,76,79,-1,77,76,74],[76,-1,-1,72,-1,69,-1,-1],[71,-1,74,77,-1,76,74,72],[74,-1,-1,-1,0,0,0,0]],
   [[84,-1,83,81,-1,79,-1,81],[83,-1,-1,79,-1,76,-1,-1],[77,-1,79,81,-1,83,-1,84],[86,-1,-1,-1,-1,-1,0,0]],
   ['C', 'Am', 'F', 'G'], ['F', 'G', 'Em', 'Am'], ['fm'], 'fm', 'breakbeat', 'fm', leadB='fm+fmbell', crush=(26000, 9)),
 # Sonic CD: 90s Japanese house / techno, organ stabs, chopped shouts
 'cd': song('Time_Warp_Zone', 'Time Warp Zone', 126,
   [[76,-1,0,76,-1,74,72,-1],[74,-1,0,74,-1,72,71,-1],[72,-1,74,76,-1,79,-1,76],[77,-1,-1,-1,0,0,0,0]],
   [[81,-1,79,81,-1,84,-1,81],[79,-1,77,79,-1,76,-1,-1],[77,-1,79,81,-1,83,-1,84],[83,-1,-1,-1,0,0,0,0]],
   ['Am7', 'Dm7', 'G', 'Cmaj7'], ['Fmaj7', 'G', 'Em7', 'Am7'], ['organ', 'pluck'], 'square', 'house', 'octave', leadB='synth', heyB=True),
 # Adventure era: fast punk-rock with crunchy guitars
 'adventure': song('Highway_Escape', 'Highway Escape', 160,
   [[76,-1,76,79,-1,76,74,71],[72,-1,-1,74,-1,76,-1,-1],[74,-1,74,78,-1,81,-1,78],[76,-1,-1,-1,0,0,0,0]],
   [[83,-1,83,81,-1,79,-1,81],[79,-1,-1,76,-1,74,-1,-1],[74,-1,76,78,-1,81,-1,83],[84,-1,-1,-1,83,-1,-1,-1]],
   ['Em', 'C', 'D', 'Em'], ['C', 'D', 'Bm', 'Em'], ['power', 'strings', 'pad'], 'crunch', 'punk', 'synth8', keysB=['power', 'strings', 'pad', 'piano'],
   levels={'lead': 1.05, 'gtrL': .9, 'gtrR': .9, 'drums': 1.15, 'bass': 1.25, 'str': 1.4, 'pad': 1.2, 'keys': 1.2}),
 # SA2 / Heroes hip-hop stages: boom-bap, scratches, horn stabs, funky bass
 'hiphop': song('Treasure_Hunt_Flow', 'Treasure Hunt Flow', 92,
   [[72,-1,0,72,70,-1,67,-1],[70,-1,0,0,72,-1,75,-1],[74,-1,0,74,72,-1,70,-1],[67,-1,-1,-1,0,0,0,0]],
   [[79,-1,79,77,-1,75,-1,77],[75,-1,-1,72,-1,70,-1,-1],[72,-1,74,75,-1,77,-1,79],[79,-1,-1,-1,0,0,0,0]],
   ['Cm7', 'Fm7', 'Bb', 'Ebmaj7' if False else 'Cm7'], ['Abmaj7', 'Bb', 'Gm7', 'Cm7'], ['ep'], 'square', 'boombap', 'funky', leadB='brass2', keysB=['ep', 'stabs'], swing=.15, scratch=True),
 # Sonic Rush: breakbeat jazz-funk, slap bass, chopped shouts, brass stabs
 'rush': song('Rush_Hour_Boost', 'Rush Hour Boost', 152,
   [[76,-1,0,79,-1,0,81,-1],[83,-1,81,79,-1,76,-1,-1],[74,-1,0,77,-1,0,79,-1],[81,-1,-1,-1,0,0,0,0]],
   [[84,-1,83,81,-1,83,-1,84],[86,-1,-1,84,-1,81,-1,-1],[79,-1,81,83,-1,84,-1,86],[88,-1,-1,-1,-1,-1,0,0]],
   ['Am9', 'D7' if False else 'Dm7', 'G', 'Cmaj7'], ['Fmaj7', 'Em7', 'Dm7', 'E7'], ['ep', 'stabs'], 'synth', 'breakbeat', 'funky', heyB=True),
 # Unleashed night stages: swinging jazz, walking bass, sax
 'jazz': song('Moonlit_Night_Stage', 'Moonlit Night Stage', 140,
   [[74,-1,77,-1,81,-1,79,77],[76,-1,-1,72,-1,-1,0,0],[72,-1,76,-1,79,-1,77,76],[74,-1,-1,-1,0,0,0,0]],
   [[81,-1,79,77,-1,76,-1,74],[76,-1,-1,79,-1,-1,0,0],[77,-1,76,74,-1,72,-1,71],[72,-1,-1,-1,0,0,0,0]],
   ['Dm7', 'G7', 'Cmaj7', 'A7' if False else 'Am7'], ['Dm7', 'G7', 'Em7', 'Am7'], ['jazzpiano'], 'sax', 'jazz', 'walking', swing=.3, levels={'lead': 1.2}),
 # Colors: bright space theme-park EDM-pop
 'colors': song('Starlight_Carnival_Run', 'Starlight Carnival Run', 128,
   [[79,-1,76,79,-1,84,-1,83],[81,-1,-1,79,-1,76,-1,-1],[77,-1,81,84,-1,86,-1,84],[83,-1,-1,-1,0,0,0,0]],
   [[88,-1,86,84,-1,83,-1,84],[86,-1,-1,83,-1,79,-1,-1],[81,-1,83,84,-1,86,-1,88],[91,-1,-1,-1,-1,-1,0,0]],
   ['C', 'Em', 'F', 'G'], ['Am', 'F', 'C', 'G'], ['pluck', 'pad'], 'fmbell', 'fourfloor', 'octave', leadB='synth+fmbell', keysB=['futurebass', 'pluck'], introkeys=['pad']),
 # Frontiers: heavy metal with strings and piano
 'frontiers': song('Titan_Undefeated', 'Titan Undefeated', 150,
   [[76,-1,-1,75,76,-1,79,-1],[77,-1,-1,76,74,-1,72,-1],[71,-1,72,74,-1,76,-1,77],[76,-1,-1,-1,-1,-1,0,0]],
   [[83,-1,-1,81,79,-1,81,-1],[79,-1,-1,77,76,-1,74,-1],[72,-1,74,76,-1,79,-1,81],[83,-1,-1,-1,-1,-1,0,0]],
   ['Em', 'C', 'D', 'B'], ['C', 'D', 'Em', 'Em'], ['chug', 'strings'], 'metal', 'metal', 'metalbass', keysB=['power', 'strings', 'piano'], introkeys=['piano', 'strings'],
   levels={'lead': 1.15, 'gtrL': 1.05, 'gtrR': 1.05, 'drums': 1.1, 'bass': 1.1, 'str': 1.5, 'keys': 1.3}),
}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
