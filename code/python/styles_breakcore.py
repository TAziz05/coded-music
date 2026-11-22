"""Steady breakcore versions of artist styles, plus an East Asian-themed one. Built with breakcore_engine.py.
python styles_breakcore.py all   (or: bts txt cortis asia kaze)"""
import sys
from breakcore_engine import build
from seasons import AMEN, FUNK

def blocks8(rows):
    """8 eighth-notes per bar, 8 bars -> four 2-bar blocks of (step, note, length) on a 16th grid."""
    flat = [x for r in rows for x in r]; ev = []
    for i, x in enumerate(flat):
        if x > 0:
            L = 1
            while i + L < len(flat) and flat[i + L] == -1: L += 1
            ev.append((i * 2, x, L * 2))
    return [[(s - 32 * b, nn, min(L, 32 * (b + 1) - s)) for s, nn, L in ev if 32 * b <= s < 32 * (b + 1)] for b in range(4)]

GOLDEN = blocks8([[74,-1,72,70,-1,74,-1,77],[77,-1,74,72,-1,69,-1,-1],[70,-1,72,74,-1,77,-1,79],[77,-1,-1,-1,72,-1,74,-1],
                  [74,-1,72,70,-1,74,-1,77],[81,-1,79,77,-1,74,-1,-1],[79,-1,77,74,-1,72,-1,70],[72,-1,-1,-1,0,0,0,0]])
BLUE = blocks8([[78,-1,78,81,-1,78,76,74],[74,-1,-1,71,-1,74,76,-1],[78,-1,78,81,-1,83,81,78],[76,-1,-1,-1,73,-1,74,76],
                [78,-1,78,81,-1,83,85,-1],[86,-1,85,83,-1,81,79,-1],[78,-1,81,-1,78,-1,74,76],[76,-1,-1,-1,-1,-1,0,0]])
RIFF = [(0, 76, 2), (3, 76, 1), (4, 79, 2), (6, 76, 2), (8, 74, 4), (12, 71, 4), (16, 76, 2), (19, 76, 1), (20, 79, 2), (22, 81, 2), (24, 79, 8)]

SONGS = {
 'bts': dict(file='Golden_Hour_Breaks', title='Golden Hour Breaks', bpm=172, chords=['Bbmaj7', 'Dm7', 'Gm7', 'F'], keys='funk', pad=.07, mel='brass', melB='brass', layerB='lead', bass='808',
   kit=dict(K=[[0, 6, 10], [0, 3, 10]], S=[[4, 12], [4, 12]], G=[[7, 14], [9, 15]], hat='hats16', shaker=True, crunch=1.5, clap=.5), patA='P0', patB='P3', melody=GOLDEN, seed=101,
   levels={'keys': 1.3}),
 'txt': dict(file='Blue_Spark_Breaks', title='Blue Spark Breaks', bpm=176, chords=['Bm', 'G', 'D', 'A'], keys='pluck', pad=.08, mel='lead', melB='crunch', layerB='lead', bass='sub',
   kit=dict(AMEN, crunch=1.7, clap=.3), patA='P1', patB='P2', melody=BLUE, seed=111, levels={'mel': 1.2}),
 'cortis': dict(file='Off_the_Lines_Breaks', title='Off the Lines Breaks', bpm=170, chords=['Em', 'C', 'D', 'B7'], keys='pluck', pad=.06, padcut=900, mel='rage', melB='rage', layerB='rage', bass='808',
   kit=dict(K=[[0, 3, 10], [0, 6, 10, 11]], S=[[4, 12], [4, 12, 14]], G=[[7, 9], [13, 15]], hat='hats16', crunch=2.6, punch=1.4, clap=.5), patA='P4', patB='P2', seed=121,
   melody=[RIFF, [(s, n - 4, L) for s, n, L in RIFF], [(s, n - 2, L) for s, n, L in RIFF], [(0, 75, 4), (4, 78, 4), (8, 81, 8), (16, 83, 8), (24, 78, 8)]], levels={'sub': .9, 'mel': 1.2}),
 'asia': dict(file='Lanterns_and_Thunder_Drums', title='Lanterns and Thunder Drums', bpm=168, chords=['Dm7', 'Bbmaj7', 'C', 'Am7'], keys='koto', pad=.06, mel='shaku', melB='shaku', layerB='koto', bass='sub',
   kit=dict(FUNK, crunch=1.4, clap=.3), patA='P3', patB='P1', taiko=True, gong=True, ending='roll', seed=131, verb=2.8, decay=.7,
   melody=[[(0, 74, 4), (4, 77, 4), (8, 79, 2), (10, 77, 2), (12, 74, 4), (16, 72, 8), (24, 69, 8)], [(0, 70, 4), (4, 72, 4), (8, 74, 8), (16, 77, 4), (20, 74, 4), (24, 72, 8)],
           [(0, 72, 4), (4, 74, 4), (8, 79, 4), (12, 77, 4), (16, 79, 8), (24, 77, 8)], [(0, 81, 8), (8, 79, 4), (12, 77, 4), (16, 74, 16)]]),
 'kaze': dict(file='Breeze_Breaks', title='Breeze Breaks', bpm=172, chords=['Amaj9', 'G#m7', 'C#m9', 'F#m9'], keys='piano', pad=.05, mel='voice', melB='piano', layerB='voice', bass='sub',
   kit=dict(AMEN, crunch=1.4, tone=9500, clap=.2), patA='P0', patB='P1', amb=[('vinyl', .5)], seed=141,
   melody=[[(0, 76, 4), (4, 80, 4), (8, 83, 6), (14, 81, 2), (16, 80, 8), (24, 76, 8)], [(0, 78, 4), (4, 75, 4), (8, 71, 8), (16, 75, 4), (20, 78, 4), (24, 80, 8)],
           [(0, 80, 4), (4, 83, 4), (8, 85, 8), (16, 83, 4), (20, 80, 4), (24, 76, 8)], [(0, 81, 6), (6, 80, 2), (8, 78, 8), (16, 76, 4), (20, 75, 4), (24, 73, 8)]]),
}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
