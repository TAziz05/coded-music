"""Genres we hadn't covered yet (all sounds are code): drift phonk, synthwave, dubstep, eurobeat, ska, reggae, amapiano,
bluegrass, city pop and jersey club. python genres.py all  (or: phonk synthwave dubstep eurobeat ska reggae amapiano bluegrass citypop jersey)"""
import sys
from newstyles import *
from popkit import build

def button_for(kind):
    def f(M, t0, st, S, i, n, tones, root):   # the ending: one hit with the whole band
        if i: return
        r = root if root < 44 else root - 12
        kick(M, t0, .9); crash(M, t0, .55)
        if kind == 'band':
            fbass(M, t0, r, 1.4, .7)
            for c in tones[:3]: brass(M, 'keys', t0, c + 12, 1.2, .18); epiano(M, 'keys', t0, c + 12, 1.8, .09)
        elif kind == 'string':
            fbass(M, t0, r, 1.4, .7)
            for c in tones[:3]: banjo(M, 'keys', t0, c + 12, 1.5, .6); M.add('keys', t0, lp(ks(mtof(c + 12), 1.5, .6, .996), 5000) * .25)
            fiddle(M, t0, tones[-1] + 12, 1.4, .9)
        else:
            heavy808(M, t0, r, 1.6, .6); impact(M, t0, .3)
            for c in tones[:3]: supersaw(M, 'keys', t0, c + 12, 1.6, .065, cut=3500, a=.003, r=.8, voices=5)
    return f

def song(file, title, bpm, ch, chB, V, C, kv, kc, drums, bass, lv, lc, end='synth', swing=0., levels=None, intro=None, introdrums=None,
         bridge=None, pre=None, verb=2.2, order=None, dV=None, bV=None, gap=None):
    s = {'intro': sec(4, ch, keys=intro or kv, drums=introdrums, riser=pre is None),
         'verse': sec(8, ch, keys=kv, drums=dV or drums, bass=bV or bass, lead=lv, mel=V),
         'chorus': sec(8, chB, keys=kc, drums=drums, bass=bass, lead=lc, mel=C, impact=True),
         'tag': sec(1, [ch[0]], keys=kc, drums=drums, bass=bass, fill=False, kind='chorus'),
         'end': sec(1, [ch[0]], extra=button_for(end), fill=False, kind='outro')}
    if bridge: s['bridge'] = sec(bridge.pop('bars', 4), bridge.pop('chords', chB), kind='bridge', **bridge)
    if pre: s['pre'] = sec(4, pre.pop('chords', chB), kind='pre', riser=True, **pre)
    order = order or (['intro', 'verse'] + (['pre'] if pre else []) + ['chorus', 'verse'] + (['pre'] if pre else []) + ['chorus']
                      + (['bridge', 'chorus'] if bridge else []) + ['tag', 'end'])
    return dict(file=file, title=title, bpm=bpm, swing=swing, sections=s, order=order, verb=verb, levels=levels or {}, chorus_keys=True, **({'mus_gap': gap} if gap else {}))

def ayys(M, t0, st, S, i, n, tones, root):
    if i % 2 == 1: ayy(M, t0 + S(6), .6)

SONGS = {
 # drift phonk: cowbell melody, distorted 808, dark pad, triplet hats, pitched-down shouts
 'phonk': song('Midnight_Drift', 'Midnight Drift', 130, ['Fm', 'Db', 'Eb', 'C'], ['Fm', 'Db', 'Eb', 'C'],
   [[65,0,65,0,68,0,65,0],[63,0,63,0,61,0,60,0],[65,0,65,0,68,0,72,0],[70,0,68,0,67,-1,0,0]],
   [[77,0,77,0,80,0,77,75],[73,0,73,0,72,0,70,0],[77,0,77,0,80,0,84,0],[82,0,80,0,79,-1,0,0]],
   ['dark'], ['dark'], 'phonk', 'phonk808', 'cowbell', 'cowbell', levels={'lead': 1.1, 'sub': 1.1}, intro=['dark'],
   bridge=dict(keys=['dark'], bass='phonk808', extra=ayys, lead='cowbell', mel=[[65,0,0,0,68,0,0,0],[63,0,0,0,60,0,0,0]])),
 # synthwave: gated snares, 16th arpeggios, octave bass, big 80s saw lead
 'synthwave': song('Neon_Horizon', 'Neon Horizon', 104, ['Am', 'F', 'C', 'G'], ['F', 'G', 'Am', 'Am'],
   [[69,-1,72,-1,76,-1,-1,74],[72,-1,-1,-1,69,-1,-1,-1],[67,-1,72,-1,76,-1,-1,79],[79,-1,-1,-1,-1,-1,0,0]],
   [[81,-1,-1,79,-1,77,-1,76],[79,-1,-1,-1,74,-1,-1,-1],[76,-1,-1,77,-1,79,-1,81],[81,-1,-1,-1,-1,-1,0,0]],
   ['synthwave'], ['synthwave'], 'gated', 'synthwave', 'saw80s', 'saw80s+sqbright', intro=['synthwave'], verb=2.8),
 # dubstep: build-up, then a half-time drop with a wobble bass
 'dubstep': song('Bass_Quake', 'Bass Quake', 140, ['Fm', 'Db', 'Ab', 'Eb'], ['Fm', 'Db', 'Ab', 'Eb'],
   [[77,-1,-1,-1,80,-1,-1,-1],[77,-1,-1,-1,73,-1,-1,-1],[75,-1,-1,-1,72,-1,-1,-1],[70,-1,-1,-1,-1,-1,0,0]],
   [[77,0,0,77,0,0,75,0],[73,0,0,0,72,0,0,0],[77,0,0,77,0,0,80,0],[79,-1,0,0,75,-1,0,0]],
   ['dark', 'pluck'], ['dark', 'pluck'], 'dubstep', 'wobble', 'fmbell', 'chop', dV='halfpop', bV='sub', intro=['dark'],
   pre=dict(keys=['dark', 'pluck'], drums=None, extra=lambda M, t0, st, S, i, n, tones, root: [snare(M, t0 + k * st, .12 + .05 * i) for k in range(0, 16, [4, 2, 1, 1][i])]),
   levels={'bass': 1.1}),
 # eurobeat: 156 bpm, offbeat octave bass, supersaw stabs, racing lead
 'eurobeat': song('Turbo_Corner', 'Turbo Corner', 156, ['Am', 'F', 'G', 'Em'], ['F', 'G', 'Em', 'Am'],
   [[76,-1,76,-1,79,-1,76,74],[72,-1,-1,74,-1,76,-1,-1],[74,-1,74,-1,77,-1,74,72],[71,-1,-1,-1,0,0,0,0]],
   [[84,-1,83,81,-1,83,-1,84],[86,-1,-1,84,-1,83,-1,79],[83,-1,81,79,-1,81,-1,83],[81,-1,-1,-1,-1,-1,0,0]],
   ['eurobeat'], ['eurobeat', 'pad'], 'eurobeat', 'octave', 'sqbright', 'saw80s+brass', intro=['eurobeat'], introdrums='eurobeat'),
 # ska: upstroke guitar on every offbeat, horn section, fast walking bass
 'ska': song('Checkerboard_Skank', 'Checkerboard Skank', 168, ['C', 'Am', 'F', 'G'], ['F', 'G', 'Em', 'Am'],
   [[72,-1,0,76,-1,0,79,-1],[77,-1,76,74,-1,0,0,0],[74,-1,0,77,-1,0,81,-1],[79,-1,77,76,-1,0,0,0]],
   [[84,-1,84,-1,83,-1,81,-1],[79,-1,-1,76,-1,72,-1,-1],[77,-1,77,-1,76,-1,74,-1],[72,-1,-1,-1,0,0,0,0]],
   ['skank'], ['skank', 'brasshits'], 'ska', 'walking', 'sax', 'brass2', end='band', introdrums='ska'),
 # reggae: one-drop drums, skank on 2 and 4, organ bubble, deep bass, melodica-style lead
 'reggae': song('Island_Time', 'Island Time', 76, ['G', 'C', 'D', 'C'], ['Em', 'C', 'G', 'D'],
   [[79,-1,-1,76,-1,74,-1,-1],[76,-1,-1,-1,72,-1,-1,-1],[74,-1,-1,78,-1,81,-1,-1],[79,-1,-1,-1,-1,-1,0,0]],
   [[83,-1,-1,81,-1,79,-1,-1],[79,-1,-1,76,-1,-1,0,0],[74,-1,76,-1,79,-1,81,-1],[78,-1,-1,-1,-1,-1,0,0]],
   ['reggae'], ['reggae'], 'onedrop', 'reggae', 'accordion', 'accordion+voice', end='band', swing=.12, levels={'bass': 1.2}),
 # amapiano: log drum bass, shakers, airy pads, jazzy piano, sax
 'amapiano': song('Log_Drum_Sunset', 'Log Drum Sunset', 112, ['Am7', 'Dm7', 'G7', 'Cmaj7'], ['Fmaj7', 'Em7', 'Dm7', 'E7'],
   [[76,-1,-1,74,-1,72,-1,-1],[74,-1,-1,-1,72,-1,69,-1],[71,-1,-1,74,-1,77,-1,-1],[76,-1,-1,-1,0,0,0,0]],
   [[81,-1,-1,79,-1,77,-1,76],[79,-1,-1,-1,76,-1,-1,-1],[77,-1,76,74,-1,72,-1,71],[71,-1,-1,-1,-1,-1,0,0]],
   ['amapiano'], ['amapiano'], 'amapiano', 'logdrum', 'sax', 'sax+piano', end='band', intro=['amapiano'], introdrums='amapiano', levels={'bass': .9}),
 # bluegrass: banjo rolls, fiddle, boom-chuck guitar, upright bass
 'bluegrass': song('Holler_Hoedown', 'Holler Hoedown', 150, ['G', 'C', 'D', 'G'], ['C', 'G', 'D', 'G'],
   [[79,78,79,81,83,-1,81,79],[76,-1,79,-1,76,74,-1,-1],[74,76,78,79,81,-1,79,78],[79,-1,-1,-1,0,0,0,0]],
   [[84,-1,83,81,79,-1,76,-1],[79,-1,81,83,-1,-1,79,-1],[78,-1,76,74,76,-1,78,-1],[79,-1,-1,-1,0,0,0,0]],
   ['bluegrass'], ['bluegrass'], 'brush', 'upright', 'fiddle', 'banjo+fiddle', end='string', intro=['bluegrass'], levels={'lead': 1.1}),
 # city pop: Rhodes chords, slap bass, funky guitar, brass, glossy 80s lead
 'citypop': song('Tokyo_Sunset_Drive', 'Tokyo Sunset Drive', 112, ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7'], ['Bbmaj7', 'A7', 'Dm7', 'G7'],
   [[76,-1,-1,79,-1,77,76,-1],[74,-1,-1,-1,71,-1,-1,-1],[72,-1,74,77,-1,76,74,-1],[72,-1,-1,-1,0,0,0,0]],
   [[81,-1,-1,79,-1,77,-1,74],[76,-1,-1,-1,73,-1,-1,-1],[77,-1,76,74,-1,72,-1,71],[74,-1,-1,-1,-1,-1,0,0]],
   ['citypop'], ['citypop', 'brasshits'], 'funk', 'slap', 'voice', 'saw80s+voice', end='band', intro=['citypop'], verb=2.6),
 # jersey club: bouncing kick pattern, bed squeaks, vocal chops
 'jersey': song('Squeak_Sprint', 'Squeak Sprint', 140, ['Cm', 'Ab', 'Eb', 'Bb'], ['Ab', 'Bb', 'Gm', 'Cm'],
   [[72,0,72,0,75,0,72,0],[70,0,0,70,68,0,0,0],[72,0,72,0,75,0,79,0],[77,-1,75,-1,0,0,0,0]],
   [[84,0,84,82,0,80,0,82],[84,0,0,87,0,84,0,0],[80,0,82,84,0,82,80,0],[79,-1,-1,-1,0,0,0,0]],
   ['pluck', 'pad'], ['futurebass', 'pluck'], 'jersey', '808', 'chop', 'chop+chipmunk', dV='jersey'),
}

SONGS['synthwave']['mus_gap'] = 2.5
# Bass Quake: the pluck stays at one level all the way through (no jump in the build-up); the bell is softer
SONGS['dubstep'].update(cont_buses=['keys'], cont_tol=0., targets={'pre': -16.5, 'verse': -15.5})
SONGS['dubstep']['sections']['pre']['riser'] = False
SONGS['dubstep']['order'] = [o for o in SONGS['dubstep']['order'] if o != 'tag']   # straight from the last drop into the final hit
SONGS['dubstep']['sections']['verse']['lv'] = .6
SONGS['synthwave']['cont_tol'] = -.5
SONGS['synthwave']['sections']['verse']['kv'] = 1.5   # keep the arpeggio as present as in the intro
SONGS['reggae']['mus_gap'] = 2.5
SONGS['bluegrass']['mus_gap'] = 2.5
SONGS['citypop']['mus_gap'] = 2.5

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
