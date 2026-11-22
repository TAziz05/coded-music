"""Steady breakcores: one sad, four seasons, four kinds of weather. Built with breakcore_engine.py.
python seasons.py all        (or one name: sad, spring, summer, autumn, winter, rain, storm, fog, wind)"""
import sys
from breakcore_engine import build

AMEN = {'K': [[0, 2, 10, 11], [0, 2, 10]], 'S': [[4, 7, 9, 12, 15], [4, 7, 9, 14]], 'G': [[1, 3, 13], [1, 13]], 'hat': 'ride'}
FUNK = {'K': [[0, 7, 10], [0, 3, 10, 11]], 'S': [[4, 12], [4, 12, 15]], 'G': [[6, 9, 14], [7, 13]], 'hat': 'hats16', 'shaker': True}
SONGS = {
 'sad': dict(file='Last_Light', title='Last Light', bpm=174, chords=['Amaj7', 'G#m7', 'F#m9', 'C#m'], keys='piano', pad=.08, mel='piano', melB='piano', layerB='strings', bass='sub',
   kit=dict(AMEN, crunch=1.5, tone=9000, clap=.15), patA='P0', patB='P1', amb=[('vinyl', .7)], seed=11,
   melody=[[(0, 76, 6), (6, 75, 2), (8, 73, 8), (16, 71, 4), (20, 73, 4), (24, 68, 8)], [(0, 75, 6), (6, 73, 2), (8, 71, 8), (16, 68, 4), (20, 71, 4), (24, 75, 8)],
           [(0, 73, 4), (4, 76, 4), (8, 80, 8), (16, 78, 4), (20, 76, 4), (24, 73, 8)], [(0, 76, 12), (12, 75, 4), (16, 73, 16)]]),
 'spring': dict(file='First_Bloom', title='First Bloom', bpm=172, chords=['G', 'D', 'Em', 'C'], keys='guitar', pad=.05, mel='flute', melB='flute', layerB='glock', bass='808',
   kit=dict(FUNK, crunch=1.3, clap=.3), patA='P0', patB='P3', amb=[('birds', 1.)], seed=21,
   melody=[[(0, 74, 4), (4, 79, 4), (8, 78, 2), (10, 76, 2), (12, 74, 4), (16, 71, 8), (24, 74, 8)], [(0, 78, 4), (4, 81, 4), (8, 79, 2), (10, 78, 2), (12, 76, 4), (16, 74, 16)],
           [(0, 76, 4), (4, 79, 4), (8, 83, 8), (16, 81, 4), (20, 79, 4), (24, 76, 8)], [(0, 76, 6), (6, 74, 2), (8, 72, 8), (16, 74, 4), (20, 76, 4), (24, 79, 8)]]),
 'summer': dict(file='Heatwave_Arcade', title='Heatwave Arcade', bpm=180, chords=['A', 'E', 'F#m', 'D'], keys='pluck', pad=.07, mel='lead', melB='lead', layerB='glock', upB=0, bass='808',
   kit=dict(K=[[0, 6, 10], [0, 3, 6, 10]], S=[[4, 12], [4, 12]], G=[[7, 14], [9, 15]], hat='hats8', shaker=True, crunch=1.8, punch=1.3), patA='P2', patB='P4', amb=[('cicadas', 1.)], seed=31,
   melody=[[(0, 76, 2), (2, 76, 2), (4, 81, 4), (8, 80, 2), (10, 81, 2), (12, 83, 4), (16, 85, 8), (24, 83, 8)], [(0, 83, 2), (2, 83, 2), (4, 80, 4), (8, 78, 2), (10, 80, 2), (12, 83, 4), (16, 80, 16)],
           [(0, 81, 2), (2, 81, 2), (4, 85, 4), (8, 83, 2), (10, 81, 2), (12, 80, 4), (16, 78, 8), (24, 76, 8)], [(0, 78, 4), (4, 81, 4), (8, 85, 4), (12, 88, 4), (16, 85, 8), (24, 83, 8)]]),
 'autumn': dict(file='Amber_Leaves', title='Amber Leaves', bpm=168, chords=['Em9', 'Cmaj7', 'Am7', 'B7'], keys='ep', pad=.05, mel='vibes', melB='vibes', layerB='nylon' if False else 'guitar', bass='sub', lofi=True,
   kit=dict(AMEN, crunch=1.3, tone=7000, clap=.2), patA='P3', patB='P1', amb=[('leaves', 1.), ('vinyl', .8)], seed=41,
   melody=[[(0, 71, 6), (6, 74, 2), (8, 78, 8), (16, 76, 4), (20, 74, 4), (24, 71, 8)], [(0, 72, 6), (6, 76, 2), (8, 79, 8), (16, 78, 4), (20, 76, 4), (24, 71, 8)],
           [(0, 72, 4), (4, 76, 4), (8, 79, 4), (12, 81, 4), (16, 79, 8), (24, 76, 8)], [(0, 75, 8), (8, 78, 8), (16, 81, 8), (24, 78, 8)]]),
 'winter': dict(file='Frostline', title='Frostline', bpm=176, chords=['Bm', 'G', 'D', 'A'], keys='harp', pad=.07, mel='glock', melB='flute', layerB='glock', upB=0, bass='808',
   kit=dict(K=[[0, 10], [0, 3, 10]], S=[[4, 12], [4, 12, 14]], G=[[6, 9], [7, 15]], hat='hats16', crunch=1.4, clap=.35), patA='P1', patB='P2', amb=[('bells', 1.), ('wind', .5)], seed=51, verb=2.8, decay=.7,
   melody=[[(0, 78, 4), (4, 81, 4), (8, 83, 4), (12, 85, 2), (14, 83, 2), (16, 81, 8), (24, 78, 8)], [(0, 79, 4), (4, 83, 4), (8, 86, 8), (16, 83, 4), (20, 81, 4), (24, 79, 8)],
           [(0, 78, 4), (4, 81, 4), (8, 86, 4), (12, 85, 4), (16, 81, 8), (24, 78, 8)], [(0, 76, 4), (4, 81, 4), (8, 85, 8), (16, 88, 8), (24, 85, 8)]]),
 'rain': dict(file='Window_Seat', title='Window Seat', bpm=165, chords=['Dmaj7', 'C#m7', 'Bm7', 'Amaj7'], keys='ep', pad=.06, padcut=1100, mel='piano', melB='piano', layerB='vibes', bass='sub', lofi=True,
   kit=dict(FUNK, crunch=1.2, tone=6500, clap=.2), patA='P0', patB='P3', amb=[('rain', 1.), ('vinyl', .6)], seed=61,
   melody=[[(0, 78, 8), (8, 76, 4), (12, 74, 4), (16, 73, 8), (24, 69, 8)], [(0, 76, 8), (8, 73, 4), (12, 71, 4), (16, 68, 16)],
           [(0, 74, 4), (4, 73, 4), (8, 71, 8), (16, 73, 4), (20, 74, 4), (24, 78, 8)], [(0, 76, 16), (16, 73, 8), (24, 69, 8)]]),
 'storm': dict(file='Lightning_Over_the_City', title='Lightning Over the City', bpm=185, chords=['Fm', 'Db', 'Ab', 'Eb'], keys='pluck', pad=.09, padcut=1000, mel='darklead', melB='brass', layerB='darklead', bass='reese',
   kit=dict(AMEN, crunch=2.4, clap=.3, punch=1.3), patA='P2', patB='P4', amb=[('rain', 1.3), ('thunder', 1.)], seed=71,
   melody=[[(0, 72, 4), (4, 75, 4), (8, 77, 8), (16, 80, 4), (20, 79, 4), (24, 77, 8)], [(0, 77, 4), (4, 80, 4), (8, 84, 8), (16, 82, 4), (20, 80, 4), (24, 77, 8)],
           [(0, 75, 4), (4, 77, 4), (8, 80, 8), (16, 79, 4), (20, 77, 4), (24, 75, 8)], [(0, 79, 8), (8, 77, 8), (16, 75, 8), (24, 70, 8)]]),
 'fog': dict(file='Lantern_in_the_Fog', title='Lantern in the Fog', bpm=160, chords=['Dm9', 'Bbmaj7', 'Fmaj7', 'C'], keys='harp', pad=.1, padcut=900, mel='voice', melB='voice', layerB='strings', bass='sub', lofi=True,
   kit=dict(FUNK, crunch=1.2, tone=3500, clap=.15), patA='P1', patB='P0', amb=[('foghorn', 1.), ('drone', .8)], seed=81, verb=3.2, decay=.9,
   melody=[[(0, 69, 16), (16, 72, 8), (24, 74, 8)], [(0, 74, 16), (16, 72, 8), (24, 70, 8)], [(0, 69, 16), (16, 72, 16)], [(0, 72, 8), (8, 74, 8), (16, 76, 16)]]),
 'wind': dict(file='Kite_Season', title='Kite Season', bpm=178, chords=['Bb', 'F', 'Gm', 'Eb'], keys='guitar', pad=.06, mel='flute', melB='lead', layerB='flute', bass='808',
   kit=dict(K=[[0, 7, 10], [0, 10, 13]], S=[[4, 12], [4, 12]], G=[[2, 14], [6, 9]], hat='hats8', shaker=True, crunch=1.5), patA='P3', patB='P2', amb=[('wind', 1.2)], seed=91,
   melody=[[(0, 77, 4), (4, 82, 4), (8, 81, 2), (10, 82, 2), (12, 84, 4), (16, 86, 8), (24, 84, 8)], [(0, 84, 4), (4, 81, 4), (8, 77, 8), (16, 79, 4), (20, 81, 4), (24, 84, 8)],
           [(0, 82, 4), (4, 86, 4), (8, 89, 8), (16, 87, 4), (20, 86, 4), (24, 82, 8)], [(0, 79, 4), (4, 82, 4), (8, 87, 8), (16, 86, 8), (24, 84, 8)]]),
}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
