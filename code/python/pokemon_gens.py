"""Route-style songs for each Pokemon generation (original melodies; the console sound and regional flavour are the style).
Gen 3 is Coastal Route (songs3.py). python pokemon_gens.py all  (or: g1 g2 g4 g5 g6 g7 g8 g9)"""
import sys
import numpy as np
import popkit
from popkit import build, LEADS
from engine import SR, saw, sqr, lp, bp, hp, noise, tarr, mtof
from instruments2 import ks, envN
from songs3 import mallet

def accordion(M, t, n, dur, vol):
    N = int((dur + .1) * SR); tt = tarr(N); f = mtof(n)
    x = (saw(f * 2 ** (-.08 / 12), N) + saw(f * 2 ** (.08 / 12), N)) * .5 + sqr(f * 2, N, .4) * .2
    x = lp(x, 3000) + .4 * bp(x, 1000, 1800); x *= 1 + .1 * np.sin(2 * np.pi * 5.5 * tt)
    M.add('lead', t, x * envN(N, dur, .04, .2, .9, .08) * vol * .16, pan=-.1)
def steel(M, t, n, dur, vol):
    N = int((min(dur, 1.2) + .4) * SR); tt = tarr(N); f = mtof(n)
    x = np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt / .15) + .25 * np.sin(2 * np.pi * f * 3.01 * tt) * np.exp(-tt / .08)
    M.add('lead', t, x * np.exp(-tt / .45) * np.clip(tt / .002, 0, 1) * vol * .3, pan=.1)
LEADS['accordion'] = lambda M, t, n, d, v: accordion(M, t, n, d * .93, v)
LEADS['steel'] = lambda M, t, n, d, v: steel(M, t, n, d, v)

def uke(M, t0, st, S, i, n, tones, root):
    for s, dn in ((0, True), (3, True), (6, False), (8, True), (10, False), (12, True), (14, False)):
        seq = [c + 12 for c in tones] if dn else [c + 12 for c in tones[::-1]]
        for j, c in enumerate(seq): M.add('keys', t0 + S(s) + j * .01, lp(ks(mtof(c), .3, .7, .99), 6000) * .12, pan=.25)
def castanets(M, t0, st, S, i, n, tones, root):
    for s in (0, 1, 3, 6, 7, 10, 12, 13, 14):
        N = int(.04 * SR); x = bp(noise(N), 2500, 7000) * np.exp(-tarr(N) / .006); M.add('perc', t0 + S(s), x * .25, pan=-.3)

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d
def route(file, title, bpm, A, B, chA, chB, keys, lead, drums, bass, leadB=None, crush=None, extra=None, swing=0, dry=False, extraB=None, heyB=False, verb=2.2):
    s = {'intro': sec(4, chA, keys=keys, drums=drums, bass=bass, extra=extra, crash=False),
         'A': sec(8, chA, keys=keys, drums=drums, bass=bass, lead=lead, mel=A, extra=extra, kind='verse'),
         'B': sec(8, chB, keys=keys, drums=drums, bass=bass, lead=leadB or lead, mel=B, extra=extraB or extra, hey=heyB, kind='chorus'),
         'outro': sec(2, [chA[0], chA[0]], keys=keys, lead=lead, mel=[[A[0][0], -1, -1, -1, -1, -1, 0, 0], [0] * 8], fill=False, extra=extra)}
    cfg = dict(file=file, title=title, bpm=bpm, swing=swing, sections=s, order=['intro', 'A', 'B', 'A', 'B', 'outro'], crush=crush, verb=verb)
    if dry: cfg['sends'] = {'lead': .0, 'keys': .0, 'drums': .0}; cfg['levels'] = {'lead_d': .12}
    return cfg

SONGS = {
 'g1': route('Pallet_Path', 'Pallet Path', 132,
   [[76,-1,72,74,76,-1,79,-1],[77,-1,76,74,-1,72,-1,-1],[74,-1,72,71,72,-1,74,76],[72,-1,-1,-1,0,0,0,0]],
   [[77,-1,77,76,74,-1,72,-1],[76,-1,76,74,72,-1,71,-1],[72,-1,74,76,-1,77,79,-1],[79,-1,-1,-1,0,0,0,0]],
   ['C', 'F', 'G', 'C'], ['F', 'C', 'Dm', 'G'], ['gbarp'], 'gb', 'gb', 'gbwave', crush=(16384, 6), dry=True),
 'g2': route('Johto_Morning', 'Johto Morning', 128,
   [[78,-1,76,74,-1,76,78,-1],[81,-1,-1,79,78,-1,76,-1],[74,-1,76,78,-1,79,-1,76],[78,-1,-1,-1,0,0,0,0]],
   [[79,-1,78,76,-1,74,-1,76],[78,-1,76,74,-1,73,-1,-1],[71,-1,73,74,-1,76,-1,78],[76,-1,-1,-1,0,0,0,0]],
   ['D', 'G', 'A', 'D'], ['G', 'D', 'Em', 'A'], ['gbarp'], 'gb12', 'gb', 'gbwave', crush=(22050, 7), dry=True),
 'g4': route('Snowpoint_Trail', 'Snowpoint Trail', 120,
   [[77,-1,-1,79,81,-1,84,-1],[82,-1,81,79,-1,77,-1,-1],[79,-1,81,82,-1,84,-1,86],[84,-1,-1,-1,0,0,0,0]],
   [[82,-1,-1,81,79,-1,77,-1],[81,-1,-1,79,77,-1,76,-1],[74,-1,76,77,-1,79,-1,81],[79,-1,-1,-1,0,0,0,0]],
   ['F', 'Bb', 'C', 'F'], ['Bb', 'F', 'Gm', 'C'], ['pluck', 'strings'], 'trumpet', 'breakbeat', 'octave', crush=(32768, 10)),
 'g5': route('Skyscraper_Sprint', 'Skyscraper Sprint', 150,
   [[76,-1,76,-1,79,-1,81,-1],[83,-1,81,79,-1,76,-1,-1],[77,-1,77,79,-1,81,-1,84],[83,-1,-1,-1,0,0,0,0]],
   [[84,-1,83,81,-1,79,-1,81],[83,-1,-1,79,-1,76,-1,-1],[77,-1,79,81,-1,84,-1,86],[88,-1,-1,-1,-1,-1,0,0]],
   ['Am', 'F', 'G', 'Em'], ['F', 'G', 'Am', 'Am'], ['pluck', 'strings'], 'synth', 'fourfloor', 'octave', leadB='synth+trumpet', crush=(32768, 10)),
 'g6': route('Boulevard_Cafe', 'Boulevard Café', 116,
   [[79,-1,78,76,-1,74,-1,76],[78,-1,-1,79,-1,81,-1,-1],[83,-1,81,79,-1,78,-1,76],[74,-1,-1,-1,0,0,0,0]],
   [[76,-1,78,79,-1,81,-1,83],[84,-1,-1,83,-1,81,-1,-1],[79,-1,81,83,-1,86,-1,84],[83,-1,-1,-1,0,0,0,0]],
   ['G', 'Em', 'C', 'D'], ['C', 'D', 'G', 'G'], ['strings', 'jazzpiano'], 'accordion', 'jazz', 'walking', swing=.18),
 'g7': route('Island_Breeze', 'Island Breeze', 104,
   [[72,-1,74,77,-1,79,-1,77],[76,-1,-1,74,-1,72,-1,-1],[74,-1,77,79,-1,81,-1,79],[77,-1,-1,-1,0,0,0,0]],
   [[81,-1,79,77,-1,79,-1,81],[82,-1,-1,81,-1,79,-1,-1],[77,-1,79,81,-1,84,-1,82],[81,-1,-1,-1,0,0,0,0]],
   ['Fmaj7', 'Bbmaj7', 'Gm7', '7C' if False else 'C7'], ['Am7', 'Dm7', 'Gm7', 'C7'], ['pad'], 'steel', 'lofi', 'finger', extra=uke, swing=.12),
 'g8': route('Stadium_Highlands', 'Stadium Highlands', 128,
   [[77,-1,77,82,-1,81,-1,79],[77,-1,-1,74,-1,77,-1,-1],[79,-1,81,82,-1,84,-1,86],[84,-1,-1,-1,0,0,0,0]],
   [[86,-1,84,82,-1,81,-1,79],[81,-1,-1,77,-1,74,-1,-1],[75,-1,77,79,-1,82,-1,81],[82,-1,-1,-1,0,0,0,0]],
   ['Bb', 'Eb', 'F', 'Bb'], ['Eb', 'Bb', 'Cm', 'F'], ['horns', 'strings'], 'brass2', 'march', 'octave', heyB=True, verb=2.8),
 'g9': route('Sunlit_Plaza', 'Sunlit Plaza', 132,
   [[76,-1,77,76,-1,74,72,-1],[74,-1,-1,72,71,-1,-1,-1],[72,-1,74,72,-1,71,69,-1],[68,-1,-1,-1,71,-1,-1,-1]],
   [[81,-1,79,77,-1,76,-1,77],[79,-1,-1,77,76,-1,74,-1],[77,-1,76,74,-1,72,71,-1],[71,-1,-1,-1,-1,-1,0,0]],
   ['Am', 'G', 'F', 'E'], ['Am', 'G', 'F', 'E'], ['nylon', 'strings'], 'nylon', 'breakbeat', 'finger', leadB='trumpet', extra=castanets),
}

SONGS['g5']['targets'] = {'verse': -13., 'chorus': -13.2, 'outro': -18.}   # final chorus no louder than the rest
SONGS['g5']['cont_tol'] = 0.
SONGS['g6']['levels'] = {'bass': .45, 'keys': .65, 'str': .7, 'lead': 1.35, 'drums': .8}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
