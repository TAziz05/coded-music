"""One song in the style of each BTS member's solo work (original melodies; the style is the inspiration), each with its own ending.
python bts_solos.py all  (or: rm jin suga jhope jimin v jk)"""
import sys
from newstyles import *
from popkit import build, kkwaeng, janggu
from breakcore_engine import gong

@D('2step')
def _(M, t0, st, S, i, n, fill):        # UK garage: skippy 2-step kick, snares on 2 and 4, shuffled hats
    for s in (0, 7, 10): kick(M, t0 + S(s), .85 if s == 0 else .6, punch=1.1)
    for s in (4, 12): snare(M, t0 + S(s), .75); clap(M, t0 + S(s), .4)
    for k in range(16):
        if k % 4 in (2, 3): hat(M, t0 + S(k), .25 if k % 4 == 2 else .14)
    for s in (5, 15): rim(M, t0 + S(s), .5)

def haegeum(M, t, n, dur, vol):         # two-string Korean fiddle: nasal and bendy
    N = int((dur + .2) * SR); tt = tarr(N); bend = -.6 * np.exp(-tt / .06) + np.clip((tt - .25) / .3, 0, 1) * .25 * np.sin(2 * np.pi * 5 * tt)
    f = mtof(n + bend); x = saw(f, N); y = bp(x, 900, 3500) + .3 * lp(x, 1200)
    M.add('lead', t, y * envN(N, dur, .04, .2, .85, .1) * vol * .14, pan=.1)
LEADS['haegeum'] = lambda M, t, n, d, v: haegeum(M, t, n, d * .95, v)
LEADS['falsetto'] = lambda M, t, n, d, v: voice(M, 'lead', t, n + 12, d * .95, .8 * v)

# ---------- endings, one per song ----------
def ring(kind):        # a soft final chord on one instrument, nothing else
    def f(M, t0, st, S, i, n, tones, root):
        if i: return
        for j, c in enumerate(tones[:4]):
            if kind == 'acoustic': M.add('keys', t0 + j * .03, lp(ks(mtof(c + 12), 4., .55, .998), 5000) * .25, pan=-.2)
            if kind == 'piano': piano(M, 'keys', t0, c + 12, 4., .3)
            if kind == 'ep': epiano(M, 'keys', t0 + j * .04, c + 12, 4., .12)
        if kind == 'piano':
            for c in tones[:3]: violins(M, t0, c + 12, 3.5, .25, att=.6)
        if kind == 'ep': cymbal(M, t0, .25); fbass(M, t0, (root if root < 44 else root - 12), 3., .5)
    return f
def falsetto_close(M, t0, st, S, i, n, tones, root):   # right after the last chorus: a soft Rhodes chord and one held falsetto note
    if i: return
    for j, c in enumerate(tones[:4]): epiano(M, 'keys', t0 + j * .04, c + 12, 4., .1)
    voice(M, 'lead', t0, tones[0] + 24, 2.5, .6); fbass(M, t0, (root if root < 44 else root - 12), 3., .45)
def gong_stop(M, t0, st, S, i, n, tones, root):   # everything cuts out on one gong + 808 hit
    if i: return
    gong(M, t0, 1.); kkwaeng(M, t0, .9); heavy808(M, t0, (root if root < 44 else root - 12), 2., .6); janggu(M, t0, False, 1.)
def big_hit_piano(M, t0, st, S, i, n, tones, root):   # one big band hit, then the piano rings on alone
    if i: return
    kick(M, t0, 1.); crash(M, t0, .7); fbass(M, t0, (root if root < 44 else root - 12), 1., .7)
    for c in tones[:3]: supersaw(M, 'keys', t0, c + 12, .9, .05, cut=3000, a=.003, r=.3, voices=4)
    for c in tones[:4]: piano(M, 'keys', t0 + 8 * st, c + 12, 3.5, .28)
def acapella(M, t0, st, S, i, n, tones, root):   # the band drops out; three vocal chops finish it
    if i: return
    for s, c in ((0, tones[2]), (3, tones[1]), (6, tones[0])): chopv(M, t0 + S(s), c + 12, st * 2.5, .6, 12)

def solo(file, title, bpm, ch, chB, V, C, kv, kc, drums, bass, lv, lc, ending, swing=0., verb=2.2, levels=None, intro=None,
         flags=None, flagsC=None, dV=None, bV=None, outro=None, fadeout=None, tapestop=False, gap=None):
    s = {'intro': sec(4, ch, keys=intro or kv, **(flags or {})),
         'verse': sec(8, ch, keys=kv, drums=dV or drums, bass=bV or bass, lead=lv, mel=V, **(flags or {})),
         'chorus': sec(8, chB, keys=kc, drums=drums, bass=bass, lead=lc, mel=C, impact=True, **(flagsC or flags or {})),
         'outro': sec(4, ch, **(outro or dict(keys=kv, fill=False))),
         'end': sec(1, [ch[0]], extra=ending, fill=False, kind='outro')}
    order = ['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro', 'end']
    if fadeout or tapestop: order = ['intro', 'verse', 'chorus', 'verse', 'chorus', 'chorus'] + (['end'] if tapestop else [])
    cfg = dict(file=file, title=title, bpm=bpm, swing=swing, sections=s, order=order, verb=verb, levels=levels or {}, chorus_keys=True)
    if fadeout: cfg['fadeout'] = fadeout
    if tapestop: cfg['tapestop'] = True; s['end'] = sec(1, [ch[0]], keys=kc, drums=drums, bass=bass, kind='chorus')
    if gap: cfg['mus_gap'] = gap
    return cfg

SONGS = {
 # RM (Indigo / Right Place, Wrong Person): warm alt-folk hip-hop, acoustic guitar, lazy boom-bap, a muted trumpet
 'rm': solo('Indigo_Fields', 'Indigo Fields', 86, ['Cmaj7', 'Am7', 'Fmaj7', 'G'], ['Fmaj7', 'G', 'Em7', 'Am7'],
   [[67,-1,-1,69,-1,72,-1,-1],[71,-1,-1,-1,67,-1,-1,-1],[69,-1,-1,72,-1,76,-1,74],[72,-1,-1,-1,-1,-1,0,0]],
   [[76,-1,-1,74,-1,72,-1,-1],[74,-1,-1,-1,71,-1,-1,-1],[72,-1,-1,71,-1,69,-1,67],[69,-1,-1,-1,-1,-1,0,0]],
   ['acoustic'], ['acoustic', 'piano', 'strings'], 'boombap', 'finger', 'nylon', 'trumpet+voice', ring('acoustic'), swing=.15,
   outro=dict(keys=['acoustic'], lead='nylon', mel=[[67,-1,-1,69,-1,72,-1,-1],[71,-1,-1,-1,-1,-1,0,0],[0] * 8, [0] * 8], fill=False)),
 # Jin (The Astronaut / Happy / Echo): bright anthemic pop-rock, driving piano and guitars, soaring chorus
 'jin': solo('Starlit_Orbit', 'Starlit Orbit', 126, ['D', 'A', 'Bm', 'G'], ['G', 'A', 'F#m', 'Bm'],
   [[74,-1,-1,76,-1,78,-1,-1],[76,-1,-1,-1,73,-1,-1,-1],[71,-1,-1,74,-1,78,-1,76],[74,-1,-1,-1,-1,-1,0,0]],
   [[83,-1,-1,81,-1,78,-1,81],[81,-1,-1,-1,76,-1,-1,-1],[78,-1,81,83,-1,85,-1,86],[86,-1,-1,-1,-1,-1,0,0]],
   ['pianoriff', 'guitar'], ['pianoriff', 'guitar', 'strings', 'pad'], 'rock', 'octave', 'voice', 'voice+synth', big_hit_piano, dV='halfpop', verb=2.6),
 # SUGA / Agust D (D-Day, 'Haegeum', 'Daechwita'): hard hip-hop over Korean royal-procession instruments
 'suga': solo('Royal_Procession', 'Royal Procession', 102, ['Em', 'C', 'Am', 'B7'], ['Em', 'C', 'Am', 'B7'],
   [[76,-1,-1,79,-1,76,74,-1],[72,-1,-1,-1,71,-1,-1,-1],[69,-1,72,76,-1,74,-1,72],[71,-1,-1,-1,-1,-1,0,0]],
   [[83,-1,83,-1,81,79,-1,81],[79,-1,-1,76,-1,-1,0,0],[81,-1,79,76,-1,74,-1,72],[71,-1,-1,-1,-1,-1,0,0]],
   ['gayageum', 'stabs'], ['gayageum', 'stabs', 'horns', 'strings'], 'trap', 'heavy808', 'haegeum', 'reed+haegeum+brass2', gong_stop,
   flags=dict(janggu=True, kkwaeng=True), flagsC=dict(janggu=True, kkwaeng=True, hey=True, heystep=12), intro=['gayageum'], levels={'drums': 1.25, 'sub': 1.15},
   outro=dict(keys=['gayageum'], drums='trap', bass='heavy808', lead='haegeum', mel=[[76,-1,-1,79,-1,76,74,-1],[72,-1,-1,-1,71,-1,-1,-1],[0] * 8, [0] * 8], janggu=True)),
 # j-hope (Jack in the Box / HOPE ON THE STREET): old-school funky hip-hop for dancing, horn stabs and scratches
 'jhope': solo('Street_Neuron', 'Street Neuron', 100, ['Gm7', 'C7', 'Gm7', 'D7'], ['Ebmaj7', 'D7', 'Gm7', 'C7'],
   [[67,-1,0,70,-1,0,72,-1],[70,-1,67,-1,65,-1,0,0],[67,-1,0,70,-1,72,74,-1],[73,-1,74,-1,0,0,0,0]],
   [[79,-1,77,74,-1,72,-1,74],[74,-1,-1,72,-1,70,-1,-1],[70,-1,72,74,-1,77,-1,79],[77,-1,-1,-1,0,0,0,0]],
   ['horns', 'chick'], ['horns', 'chick', 'ep'], 'funk', 'funky', 'sax', 'brass2+sax', None, swing=.1, tapestop=True,
   flags=dict(scratch=True), flagsC=dict(scratch=True, hey=True)),
 # Jimin (FACE / MUSE): glossy 80s synth-pop, dreamy pads and falsetto lead
 'jimin': solo('Midnight_Mirage', 'Midnight Mirage', 118, ['F#m', 'D', 'A', 'E'], ['D', 'E', 'C#m', 'F#m'],
   [[73,-1,-1,76,-1,73,-1,71],[69,-1,-1,-1,66,-1,-1,-1],[69,-1,-1,73,-1,76,-1,78],[76,-1,-1,-1,-1,-1,0,0]],
   [[78,-1,-1,76,-1,73,-1,76],[76,-1,-1,73,-1,71,-1,-1],[73,-1,76,78,-1,81,-1,80],[78,-1,-1,-1,-1,-1,0,0]],
   ['synthwave'], ['synthwave', 'ep'], 'fourfloor', 'synth8', 'falsetto', 'falsetto+saw80s', ring('ep'), dV='halfpop', verb=2.8, gap=3.,
   outro=dict(keys=['synthwave'], lead='falsetto', mel=[[73,-1,-1,76,-1,73,-1,71],[69,-1,-1,-1,-1,-1,-1,-1],[0] * 8, [0] * 8], fill=False)),
 # V (Layover / FRI(END)S): mellow late-night jazz R&B, Rhodes, brushed swing, muted trumpet
 'v': solo('Velvet_Layover', 'Velvet Layover', 76, ['Dm9', 'G7', 'Cmaj9', 'A7'], ['Fmaj7', 'Em7', 'Dm7', 'G7'],
   [[69,-1,-1,72,-1,74,-1,-1],[71,-1,-1,-1,67,-1,-1,-1],[67,-1,-1,71,-1,74,-1,76],[73,-1,-1,-1,-1,-1,0,0]],
   [[77,-1,-1,76,-1,74,-1,72],[74,-1,-1,-1,71,-1,-1,-1],[72,-1,-1,74,-1,77,-1,76],[74,-1,-1,-1,-1,-1,0,0]],
   ['ep'], ['ep', 'jazzpiano'], 'jazz', 'walking', 'trumpet', 'sax+trumpet', ring('ep'), swing=.2, verb=2.8),
 # Jung Kook (GOLDEN): sleek UK-garage pop with funky guitar and vocal chops
 'jk': solo('Gold_Rush_Garage', 'Gold Rush Garage', 126, ['Am7', 'Dm7', 'G', 'Cmaj7'], ['Fmaj7', 'G', 'Em7', 'Am7'],
   [[76,-1,0,76,74,-1,72,-1],[74,-1,-1,72,-1,69,-1,-1],[72,-1,0,72,74,-1,76,-1],[79,-1,-1,-1,0,0,0,0]],
   [[81,-1,79,-1,76,-1,79,-1],[81,-1,-1,79,-1,76,-1,-1],[77,-1,76,74,-1,76,-1,79],[76,-1,-1,-1,0,0,0,0]],
   ['chick', 'ep'], ['chick', 'ep', 'pad'], '2step', 'sub', 'voice', 'voice+chop', acapella),
}

SONGS['jimin'].update(cont_buses=['keys'], cont_tol=0., targets={'intro': -15., 'outro': -16.})   # the arpeggio keeps one level from the intro on
SONGS['jimin']['sections']['verse']['kv'] = 2.; SONGS['jimin']['sections']['chorus']['kv'] = 1.6
SONGS['jk'].update(cont_tol=-1., order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'end'])   # no outro: the band drops straight into the vocal chops
SONGS['jk']['sections']['intro']['keys'] = ['ep']                                                     # the ticking guitar comes in with the verse
SONGS['jimin']['order'] = ['intro', 'verse', 'chorus', 'verse', 'chorus', 'end']                       # no synth outro: it ends right after the last chorus
SONGS['jimin']['sections']['end']['extra'] = falsetto_close                       # the ending no longer jumps back up

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
