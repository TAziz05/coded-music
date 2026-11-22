"""One original instrumental per BTS album era (style only; all melodies are original). Built with popkit.py.
python bts_albums.py all   (or: school dark hyyh wings her tear answer persona seven be proof arirang)"""
import sys
from popkit import build

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d

SONGS = {
 # 2 COOL 4 SKOOL / O!RUL8,2? / SKOOL LUV AFFAIR: hard 90s boom-bap, horn stabs, scratches, gang chants
 'school': dict(file='Schoolyard_Riot', title='Schoolyard Riot', era='School trilogy (2013–14)', bpm=96, swing=.15, sections={
   'intro': sec(2, ['Cm', 'Ab'], keys=['pianoriff'], scratch=True),
   'verse': sec(8, ['Cm', 'Ab', 'Bb', 'G'], keys=['pianoriff'], drums='boombap', bass='finger', scratch=True, lead='square', lv=.7,
                mel=[[72,-1,0,72,70,-1,67,-1],[68,-1,0,0,72,-1,70,-1],[70,-1,0,70,74,-1,72,-1],[71,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Cm', 'Ab', 'Bb', 'G'], keys=['stabs', 'pianoriff'], drums='boombap', bass='finger', hey=True, lead='brass2',
                 mel=[[72,-1,72,75,-1,72,70,67],[68,-1,68,72,-1,75,-1,-1],[70,-1,70,74,-1,77,75,74],[71,-1,-1,-1,67,-1,-1,-1],
                      [72,-1,72,75,-1,72,70,67],[68,-1,68,72,-1,75,-1,77],[79,-1,77,75,-1,74,72,74],[71,-1,-1,-1,0,0,0,0]]),
   'outro': sec(2, ['Cm', 'Cm'], keys=['stabs'], drums='boombap', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 # DARK & WILD: rock-rap, heavy guitars, brass hits
 'dark': dict(file='Dark_and_Wild_Run', title='Dark and Wild Run', era='Dark & Wild (2014)', bpm=140, sections={
   'intro': sec(4, ['Em', 'C', 'D', 'B7'], keys=['power'], riser=True),
   'verse': sec(8, ['Em', 'C', 'D', 'B7'], keys=['darkgtr'], drums='halfpop', bass='synth8', lead='square', lv=.7,
                mel=[[71,-1,71,74,-1,71,69,-1],[67,-1,67,71,-1,72,-1,-1],[69,-1,69,74,-1,72,71,-1],[71,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Em', 'C', 'D', 'B7'], keys=['power', 'stabs'], drums='rock', bass='synth8', hey=True, lead='crunch', impact=True,
                 mel=[[76,-1,76,79,-1,76,74,71],[72,-1,-1,76,-1,79,-1,-1],[78,-1,78,81,-1,78,76,74],[75,-1,-1,-1,71,-1,-1,-1]]),
   'bridge': sec(4, ['C', 'D', 'Em', 'B7'], keys=['pad', 'darkgtr'], drums='halfpop', bass='long', riser=True),
   'outro': sec(2, ['Em', 'Em'], keys=['power'], drums='rock', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'bridge', 'chorus', 'outro'], levels={'lead': 1.3}),
 # THE MOST BEAUTIFUL MOMENT IN LIFE (Pt.1, Pt.2, Young Forever): emotional synth-pop, piano, bright arps
 'hyyh': dict(file='Youth_in_Bloom', title='Youth in Bloom', era='The Most Beautiful Moment in Life (2015–16)', bpm=128, sections={
   'intro': sec(4, ['Bm', 'G', 'D', 'A'], keys=['piano']),
   'verse': sec(8, ['Bm', 'G', 'D', 'A'], keys=['piano', 'pad'], drums='halfpop', bass='long', lead='voice',
                mel=[[71,-1,71,74,-1,73,71,-1],[71,-1,69,67,-1,-1,0,0],[66,-1,69,74,-1,73,-1,71],[69,-1,-1,-1,0,0,0,0]]),
   'pre': sec(4, ['G', 'A', 'Bm', 'A'], keys=['piano', 'pluck'], drums='halfpop', bass='octave', riser=True, lead='voice',
              mel=[[74,-1,74,76,-1,78,-1,-1],[76,-1,76,78,-1,79,-1,-1],[78,-1,79,81,-1,83,-1,81],[81,-1,-1,-1,-1,-1,0,0]]),
   'chorus': sec(8, ['Bm', 'G', 'D', 'A'], keys=['pluck', 'pad', 'piano'], drums='fourfloor', bass='octave', lead='synth+voice', impact=True,
                 mel=[[78,-1,76,74,-1,76,78,81],[79,-1,-1,78,-1,76,74,-1],[74,-1,76,78,-1,81,-1,78],[76,-1,-1,-1,-1,-1,0,0]]),
   'outro': sec(4, ['Bm', 'G', 'D', 'D'], keys=['piano'], fill=False)},
   order=['intro', 'verse', 'pre', 'chorus', 'verse', 'pre', 'chorus', 'outro']),
 # WINGS / YOU NEVER WALK ALONE: dark moombahton, pan-flute lead, dramatic strings
 'wings': dict(file='Velvet_Wings', title='Velvet Wings', era='Wings (2016–17)', bpm=93, sections={
   'intro': sec(4, ['Am', 'F', 'Dm', 'E'], keys=['strings'], lead='flute', mel=[[76,-1,-1,-1,72,-1,-1,-1],[72,-1,-1,-1,69,-1,-1,-1],[74,-1,-1,-1,69,-1,-1,-1],[68,-1,-1,-1,-1,-1,0,0]]),
   'verse': sec(8, ['Am', 'F', 'Dm', 'E'], keys=['dembowpluck'], drums='dembow', bass='sub', lead='voice', lv=.8,
                mel=[[69,-1,69,72,-1,71,69,-1],[69,-1,-1,65,-1,-1,0,0],[65,-1,69,-1,72,-1,71,69],[68,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Am', 'F', 'Dm', 'E'], keys=['dembowpluck', 'strings'], drums='dembow', bass='808', lead='flute+synth', impact=True,
                 mel=[[76,-1,-1,74,72,-1,71,72],[72,-1,-1,-1,69,-1,-1,-1],[74,-1,-1,72,69,-1,65,-1],[68,-1,-1,-1,71,-1,74,-1]]),
   'outro': sec(2, ['Am', 'Am'], keys=['strings'], fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro'], levels={'lead': 1.2}),
 # LOVE YOURSELF: HER: bright future-bass pop, acoustic guitar, whistle hook
 'her': dict(file='Double_Helix', title='Double Helix', era='Love Yourself: Her (2017)', bpm=128, chorus_keys=True, sections={
   'intro': sec(4, ['F#m', 'D', 'A', 'E'], keys=['acoustic'], lead='whistle', mel=[[85,-1,83,81,-1,78,-1,-1],[81,-1,78,76,-1,-1,0,0],[78,-1,81,83,-1,85,-1,83],[80,-1,-1,-1,0,0,0,0]], up=-12),
   'verse': sec(8, ['F#m', 'D', 'A', 'E'], keys=['acoustic'], drums='halfpop', bass='long', lead='voice',
                mel=[[73,-1,73,76,-1,73,71,-1],[69,-1,-1,66,-1,-1,0,0],[69,-1,71,73,-1,76,-1,73],[71,-1,-1,-1,0,0,0,0]]),
   'pre': sec(4, ['D', 'E', 'F#m', 'E'], keys=['acoustic', 'pad'], drums='halfpop', bass='octave', riser=True, lead='voice',
              mel=[[74,-1,76,78,-1,76,-1,-1],[76,-1,78,80,-1,78,-1,-1],[78,-1,80,81,-1,83,-1,-1],[83,-1,-1,-1,-1,-1,0,0]]),
   'chorus': sec(8, ['F#m', 'D', 'A', 'E'], keys=['futurebass', 'acoustic'], drums='fourfloor', bass='808', lead='synth+flute', impact=True,
                 mel=[[81,-1,81,83,-1,81,78,-1],[78,-1,-1,76,-1,78,81,-1],[81,-1,83,85,-1,83,81,-1],[80,-1,-1,-1,76,-1,-1,-1]]),
   'outro': sec(2, ['F#m', 'F#m'], keys=['acoustic'], fill=False)},
   order=['intro', 'verse', 'pre', 'chorus', 'verse', 'pre', 'chorus', 'outro']),
 # LOVE YOURSELF: TEAR: emo hip-hop, dark guitar, trap drums, strings
 'tear': dict(file='Fragile_Mask', title='Fragile Mask', era='Love Yourself: Tear (2018)', bpm=78, chorus_keys=True, sections={
   'intro': sec(4, ['Bm', 'G', 'Em', 'F#'], keys=['darkgtr']),
   'verse': sec(8, ['Bm', 'G', 'Em', 'F#'], keys=['darkgtr', 'pad'], drums='trap', bass='808', lead='voice', lv=.85,
                mel=[[71,-1,71,74,-1,71,69,-1],[67,-1,-1,71,-1,-1,0,0],[67,-1,71,74,-1,76,-1,74],[73,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Bm', 'G', 'Em', 'F#'], keys=['darkgtr', 'strings'], drums='trap', bass='808', lead='crunch+voice', impact=True,
                 mel=[[74,-1,74,76,78,-1,76,74],[74,-1,-1,71,-1,-1,0,0],[71,-1,74,76,-1,79,-1,78],[78,-1,-1,-1,73,-1,-1,-1]]),
   'outro': sec(2, ['Bm', 'Bm'], keys=['darkgtr'], fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 # LOVE YOURSELF: ANSWER: Korean traditional sounds over a gqom/house beat
 'answer': dict(file='Eolssu_Groove', title='Eolssu Groove', era='Love Yourself: Answer (2018)', bpm=126, sections={
   'intro': sec(4, ['Em', 'C', 'D', 'Em'], keys=['gayageum'], janggu=True, gong=True),
   'verse': sec(8, ['Em', 'C', 'D', 'Em'], keys=['gayageum'], drums='gqom', bass='sub', janggu=True, lead='danso',
                mel=[[71,-1,71,74,-1,76,-1,-1],[74,-1,71,-1,67,-1,-1,-1],[69,-1,71,74,-1,76,74,-1],[71,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Em', 'C', 'D', 'Em'], keys=['gayageum', 'stabs'], drums='gqom', bass='808', kkwaeng=True, hey=True, heystep=0, lead='reed', impact=True,
                 mel=[[76,-1,79,-1,81,-1,79,76],[79,-1,-1,-1,76,-1,74,-1],[74,-1,76,-1,79,-1,81,83],[83,-1,-1,-1,81,79,76,-1]]),
   'outro': sec(2, ['Em', 'Em'], keys=['gayageum'], janggu=True, gong=True, fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro'], levels={'lead': 1.2}),
 # MAP OF THE SOUL: PERSONA: bright funk-pop
 'persona': dict(file='Light_Up_the_Persona', title='Light Up the Persona', era='Map of the Soul: Persona (2019)', bpm=120, sections={
   'intro': sec(4, ['Gmaj7', 'Em7', 'Am7', 'D7'], keys=['chick', 'ep']),
   'verse': sec(8, ['Gmaj7', 'Em7', 'Am7', 'D7'], keys=['chick', 'ep'], drums='funk', bass='funky', lead='voice',
                mel=[[74,-1,74,76,-1,74,71,-1],[71,-1,-1,67,-1,69,71,-1],[72,-1,72,74,-1,76,-1,74],[74,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Gmaj7', 'Em7', 'Am7', 'D7'], keys=['chick', 'ep', 'stabs'], drums='funk', bass='funky', lead='synth+square', impact=True,
                 mel=[[79,-1,78,76,-1,74,-1,76],[78,-1,-1,76,-1,74,71,-1],[72,-1,74,76,-1,79,-1,78],[76,-1,-1,-1,74,-1,-1,-1]]),
   'outro': sec(2, ['Gmaj7', 'Gmaj7'], keys=['chick', 'stabs'], drums='funk', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 # MAP OF THE SOUL: 7: marching drums, orchestra, choir, hip-hop
 'seven': dict(file='March_of_Seven', title='March of Seven', era='Map of the Soul: 7 (2020)', bpm=106, verb=2.8, decay=.65, sections={
   'intro': sec(4, ['F#m', 'D', 'A', 'E'], keys=['horns'], drums='march', riser=True),
   'verse': sec(8, ['F#m', 'D', 'A', 'E'], keys=['strings'], drums='march', bass='808', lead='voice', lv=.8,
                mel=[[69,-1,69,73,-1,69,68,-1],[66,-1,-1,69,-1,-1,0,0],[69,-1,71,73,-1,76,-1,73],[71,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['F#m', 'D', 'A', 'E'], keys=['strings', 'horns'], drums='march', bass='heavy808', lead='choirbrass', impact=True, hey=True,
                 mel=[[73,-1,73,76,-1,78,-1,-1],[81,-1,-1,78,-1,76,-1,-1],[76,-1,78,81,-1,83,81,-1],[80,-1,-1,-1,76,-1,-1,-1]]),
   'outro': sec(2, ['F#m', 'F#m'], keys=['horns'], drums='march', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 # BE: warm acoustic lo-fi pop
 'be': dict(file='Life_Goes_Slow', title='Life Goes Slow', era='BE (2020)', bpm=82, swing=.1, chorus_keys=True, sections={
   'intro': sec(4, ['Cmaj7', 'G', 'Am7', 'Fmaj7'], keys=['guitar']),
   'verse': sec(8, ['Cmaj7', 'G', 'Am7', 'Fmaj7'], keys=['guitar', 'piano'], drums='lofi', bass='finger', lead='voice', kv=.8,
                mel=[[72,-1,72,74,-1,72,71,-1],[71,-1,-1,67,-1,-1,0,0],[69,-1,72,76,-1,74,-1,72],[72,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Cmaj7', 'G', 'Am7', 'Fmaj7'], keys=['guitar', 'piano', 'pad'], drums='lofi', bass='finger', lead='voice+flute', lv=.9,
                 mel=[[76,-1,74,72,-1,74,-1,76],[74,-1,-1,71,-1,-1,0,0],[72,-1,74,76,-1,79,-1,77],[76,-1,-1,-1,0,0,0,0]]),
   'outro': sec(4, ['Cmaj7', 'G', 'Am7', 'Cmaj7'], keys=['guitar'], lead='whistle', mel=[[76,-1,74,72,-1,-1,0,0],[74,-1,71,67,-1,-1,0,0],[72,-1,74,76,-1,-1,0,0],[72,-1,-1,-1,-1,-1,0,0]], up=-12, fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 # PROOF: nostalgic, hopeful mellow hip-hop/R&B
 'proof': dict(file='Yet_to_Bloom', title='Yet to Bloom', era='Proof (2022)', bpm=90, swing=.12, chorus_keys=True, sections={
   'intro': sec(4, ['Dmaj7', 'C#m7', 'Bm7', 'E7'], keys=['ep']),
   'verse': sec(8, ['Dmaj7', 'C#m7', 'Bm7', 'E7'], keys=['ep', 'guitar'], drums='boombap', bass='finger', lead='voice', kv=.8,
                mel=[[73,-1,73,76,-1,73,71,-1],[71,-1,-1,68,-1,-1,0,0],[69,-1,71,73,-1,76,-1,74],[74,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Dmaj7', 'C#m7', 'Bm7', 'E7'], keys=['ep', 'guitar', 'strings'], drums='boombap', bass='finger', lead='synth+voice', lv=.9,
                 mel=[[78,-1,76,73,-1,76,-1,78],[76,-1,-1,73,-1,71,-1,-1],[74,-1,76,78,-1,81,-1,80],[80,-1,-1,-1,76,-1,-1,-1]]),
   'outro': sec(2, ['Dmaj7', 'Dmaj7'], keys=['ep'], fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 # ARIRANG (2026): tradition meets now: temple bell, gayageum and danso, minimal 808 hip-hop with metal clanks, a vocoder hook, an electric-guitar surge
 'arirang': dict(file='Arirang_Dawn', title='Arirang Dawn', era='ARIRANG (2026)', bpm=94, verb=3.0, decay=.75, sections={
   'intro': sec(4, ['Em', 'D', 'C', 'Em'], keys=['gayageum'], janggu=True, bell=True, lead='danso',
                mel=[[76,-1,-1,79,-1,76,74,-1],[74,-1,-1,-1,71,-1,-1,-1],[72,-1,74,-1,76,-1,79,-1],[76,-1,-1,-1,-1,-1,0,0]]),
   'verse': sec(8, ['Em', 'C', 'D', 'Em'], keys=['pad'], drums='trap', bass='heavy808', clank=True, lead='voice', lv=.8,
                mel=[[71,-1,71,74,-1,71,69,-1],[67,-1,-1,69,-1,-1,0,0],[69,-1,71,74,-1,76,-1,74],[71,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['C', 'D', 'Em', 'Em'], keys=['pad', 'gayageum'], drums='trap', bass='heavy808', clank=True, lead='vocoder', impact=True,
                 mel=[[76,-1,79,-1,81,-1,79,76],[78,-1,-1,-1,74,-1,-1,-1],[76,-1,74,-1,71,-1,74,76],[76,-1,-1,-1,-1,-1,0,0]]),
   'bridge': sec(4, ['Em', 'D', 'C', 'Em'], keys=['gayageum'], janggu=True, lead='danso', bell=True, kind='bridge',
                 mel=[[76,-1,-1,79,-1,76,74,-1],[74,-1,-1,-1,71,-1,-1,-1],[72,-1,74,-1,76,-1,79,-1],[76,-1,-1,-1,-1,-1,0,0]]),
   'final': sec(8, ['C', 'D', 'Em', 'Em'], keys=['power', 'gayageum'], drums='rock', bass='heavy808', lead='vocoder+danso', impact=True, kind='chorus',
                mel=[[76,-1,79,-1,81,-1,79,76],[78,-1,-1,-1,74,-1,-1,-1],[76,-1,74,-1,71,-1,74,76],[76,-1,-1,-1,-1,-1,0,0]]),
   'outro': sec(2, ['Em', 'Em'], keys=['gayageum'], bell=True, fill=False)},
   order=['intro', 'verse', 'chorus', 'bridge', 'final', 'outro'], levels={'lead': 1.2}),
}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
