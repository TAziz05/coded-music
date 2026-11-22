"""Generic YouTube / gaming background music. Built with popkit.py.
python bgm.py all  (or: lounge levelup menu final)"""
import sys
from popkit import build

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d

SONGS = {
 'lounge': dict(file='Respawn_Lounge', title='Respawn Lounge', bpm=84, swing=.16, chorus_keys=True, sections={
   'intro': sec(4, ['Dm9', 'G7', 'Cmaj7', 'Am7'], keys=['ep']),
   'verse': sec(8, ['Dm9', 'G7', 'Cmaj7', 'Am7'], keys=['ep', 'guitar'], drums='boombap', bass='finger', kv=.8, lead='square', lv=.6,
                mel=[[74,-1,72,69,-1,-1,0,0],[71,-1,-1,67,-1,-1,0,0],[72,-1,74,76,-1,-1,79,-1],[76,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['Dm9', 'G7', 'Cmaj7', 'Am7'], keys=['ep', 'guitar', 'pad'], drums='boombap', bass='finger', lead='vibes' if False else 'piano',
                 mel=[[77,-1,76,74,-1,72,-1,74],[74,-1,-1,71,-1,-1,0,0],[72,-1,74,76,-1,79,-1,77],[76,-1,-1,-1,-1,-1,0,0]]),
   'outro': sec(2, ['Dm9', 'Cmaj7'], keys=['ep'], fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 'levelup': dict(file='Level_Up_Rush', title='Level Up Rush', bpm=124, ride=.5, targets={'intro': -17., 'verse': -14., 'chorus': -13.}, sections={
   'intro': sec(4, ['C', 'G', 'Am', 'F'], keys=['pluck'], riser=True),
   'verse': sec(8, ['C', 'G', 'Am', 'F'], keys=['pluck', 'pad'], drums='house', bass='octave', lead='square', lv=.7,
                mel=[[72,-1,72,76,-1,72,-1,79],[79,-1,-1,74,-1,71,-1,-1],[72,-1,76,79,-1,81,-1,79],[77,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['C', 'G', 'Am', 'F'], keys=['futurebass', 'pluck'], drums='house', bass='octave', lead='synth', impact=True,
                 mel=[[84,-1,83,79,-1,76,-1,79],[83,-1,-1,79,-1,74,-1,-1],[81,-1,83,84,-1,88,-1,84],[84,-1,-1,-1,81,-1,-1,-1]]),
   'outro': sec(2, ['C', 'C'], keys=['pluck'], drums='house', fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 'menu': dict(file='Menu_Drift', title='Menu Drift', bpm=100, ride=.75, targets={'intro': -16., 'verse': -14., 'chorus': -13.5, 'outro': -15.5}, sections={
   'intro': sec(4, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], keys=['pad']),
   'verse': sec(8, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], keys=['pad', 'pluck'], drums='halfpop', bass='long', lead='fmbell', lv=.8,
                mel=[[76,-1,-1,-1,72,-1,-1,-1],[74,-1,-1,-1,71,-1,-1,-1],[72,-1,-1,-1,69,-1,-1,-1],[71,-1,-1,-1,-1,-1,0,0]]),
   'chorus': sec(8, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], keys=['pad', 'pluck'], drums='fourfloor', bass='octave', lead='synth', lv=.8,
                 mel=[[81,-1,79,76,-1,-1,0,0],[79,-1,76,74,-1,-1,0,0],[77,-1,76,72,-1,-1,74,-1],[72,-1,-1,-1,-1,-1,0,0]]),
   'outro': sec(4, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], keys=['pad'], fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']),
 'final': dict(file='Final_Circle', title='Final Circle', bpm=140, sections={
   'intro': sec(4, ['Fm', 'Db', 'Ab', 'Eb'], keys=['pad'], riser=True, lead='synth', lv=.6, mel=[[77,-1,-1,-1,80,-1,-1,-1],[77,-1,-1,-1,73,-1,-1,-1],[75,-1,-1,-1,72,-1,-1,-1],[70,-1,-1,-1,-1,-1,0,0]]),
   'verse': sec(8, ['Fm', 'Db', 'Ab', 'Eb'], keys=['pad', 'pluck'], drums='trap', bass='heavy808', lead='square', lv=.7,
                mel=[[72,-1,72,75,-1,72,70,-1],[68,-1,-1,72,-1,-1,0,0],[72,-1,75,77,-1,75,-1,72],[70,-1,-1,-1,0,0,0,0]]),
   'drop': sec(8, ['Fm', 'Db', 'Ab', 'Eb'], keys=['futurebass', 'stabs'], drums='trap', bass='heavy808', lead='synth+brass', impact=True, hey=True,
               mel=[[77,-1,77,80,-1,77,75,72],[73,-1,-1,77,-1,80,-1,-1],[80,-1,80,82,-1,84,82,80],[79,-1,-1,-1,75,-1,-1,-1]]),
   'outro': sec(2, ['Fm', 'Fm'], keys=['pad'], fill=False)},
   order=['intro', 'verse', 'drop', 'verse', 'drop', 'verse', 'drop', 'outro']),
}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
