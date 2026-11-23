"""Songs made from other things (all sounds are code):
  Spelled in Notes   words turned into melodies: each letter is a note (A-G as named, then H=A, I=B, ... around again), digits are scale steps
  Polygon Party      shapes as rhythms: a triangle hits 3 times a bar, a square 4, a pentagon 5..., and a star visits a pentagon's corners every other one
  Rainbow Spectrum   colors as notes: each color's light frequency halved 40 times lands in hearing range (red ~409 Hz, violet ~664 Hz), and each color is a section in that key
python concepts.py all  (or: words shapes colors)"""
import sys, math
import numpy as np
from newstyles import *
from popkit import build
from songs5 import harp

def rows_from(notes):
    notes = notes + [0] * (-len(notes) % 8); return [notes[k:k + 8] for k in range(0, len(notes), 8)]

# ---------------- words ----------------
LETTER = {c: [57, 59, 60, 62, 64, 65, 67][(ord(c) - 65) % 7] for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}   # A=A, B=B ... G=G, H=A, I=B ...
DIGIT = {str(d): 57 + [0, 2, 3, 5, 7, 8, 10, 12, 14, 15][d] for d in range(10)}
def spell(text, oct_=12):                   # one eighth note per letter, a rest for a space, the last letter of each word held
    out = []
    for w in text.upper().split():
        ns = [LETTER.get(c, DIGIT.get(c)) for c in w if c in LETTER or c in DIGIT]
        out += [n + oct_ for n in ns[:-1]] + [ns[-1] + oct_, -1] + [0]
    return rows_from(out)
def caption(words):
    def f(M, t0, st, S, i, n, tones, root): pass
    return f
def end_words(M, t0, st, S, i, n, tones, root):    # it spells T-H-E E-N-D
    if i: return
    t = t0
    for w in ('THE', 'END'):
        for c in w: plastic(M, 'lead', t, LETTER[c] + 12, st * 1.8, 1.); t += 2 * st
        t += 2 * st
    kick(M, t, .9); crash(M, t, .5)
    for c in tones[:3]: epiano(M, 'keys', t, c + 12, 2.5, .12)

# ---------------- shapes ----------------
from mathsong import euclid
def polygon(sides, inst, every=1, order=None, rot=0):   # a shape with N corners = N hits spread as evenly as the beat grid allows (Euclidean rhythm); notes walk the corners
    def f(M, t0, st, S, i, n, tones, root):
        if i % every: return
        corners = [tones[k % 3] + 12 * (k // 3) for k in range(sides)]
        seq = order(sides) if order else list(range(sides))
        for j, s in enumerate(euclid(sides, 16, rot)): inst(M, t0 + S(s), corners[seq[j]] + 12)
    return f
def star(n): return [(2 * k) % n for k in range(n)]          # a star polygon: visit every other corner (0, 2, 4, 1, 3)
TRI = polygon(3, lambda M, t, nn: marimba(M, 'keys', t, nn, .3, .8, pan=-.4))   # 3 hits: the 'tresillo' feel
SQU = polygon(4, lambda M, t, nn: pizz(M, t, nn - 12, .8, pan=.4))
PEN = polygon(5, lambda M, t, nn: celesta(M, 'glock', t, nn, .25, .6, pan=.2))
HEX = polygon(6, lambda M, t, nn: woodblock(M, t, nn % 2 == 0, .5), rot=1)
OCT = polygon(8, lambda M, t, nn: hat(M, t, .25))
STAR = polygon(5, lambda M, t, nn: plastic(M, 'lead', t, nn + 12, .3, .9), order=star)
CIRC = [False]
def circle(M, t0, st, S, i, n, tones, root):      # a circle has no corners: one smooth, unbroken pad (it swells in once, then each chord overlaps the next)
    first = not CIRC[0]; CIRC[0] = True
    for c in tones[:3]: supersaw(M, 'pad', t0, c + 12, 16 * st + .5, .045, cut=1500, a=(24 * st if first else .35), r=1.2, voices=3)
def end_circle(M, t0, st, S, i, n, tones, root):  # all the shapes once more, then they melt into one circle
    if i == 0:   # bar 1: all the shapes; bar 2: only the triangle and pentagon; then just the circle, fading away
        for f in (TRI, SQU, PEN, HEX, OCT): f(M, t0, st, S, 0, 1, tones, root)
        for c in tones[:3]: supersaw(M, 'pad', t0, c + 12, 32 * st + 2., .045, cut=1500, a=.35, r=3.5, voices=3)
    elif i == 1:
        for f in (TRI, PEN): f(M, t0, st, S, 0, 1, tones, root)
        harp(M, t0 + 16 * st, tones[0] + 24, .5)
    else: TRI(M, t0, st, S, 0, 1, tones, root)   # the song fades out from here

# ---------------- colors ----------------
COLORS = [('red', 450e12), ('orange', 490e12), ('yellow', 520e12), ('green', 560e12), ('blue', 640e12), ('indigo', 670e12), ('violet', 730e12)]
def color_note(f_light): return int(round(69 + 12 * math.log2(f_light / 2 ** 40 / 440)))   # light frequency halved 40 octaves -> MIDI note
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
COLOR_KEYS = [(c, color_note(f)) for c, f in COLORS]                                   # red 68 (Ab) ... violet 76 (E)
COOL = {'blue', 'indigo'}
def key_chords(root, minor):
    r = NAMES[root % 12]
    if minor: return [r + 'm', NAMES[(root + 8) % 12], NAMES[(root + 3) % 12], NAMES[(root + 10) % 12]]
    return [r, NAMES[(root + 7) % 12], NAMES[(root + 9) % 12] + 'm', NAMES[(root + 5) % 12]]
MOT_MAJ = [0, 4, 7, 9, 7, 4, 2, 4]; MOT_MIN = [0, 3, 7, 8, 7, 3, 2, 3]
def color_mel(root, minor, nxt=None):
    m = MOT_MIN if minor else MOT_MAJ; base = root
    land = base + m[2] if nxt is None else min((nxt + 7 + 12 * o for o in (-1, 0, 1)), key=lambda x: abs(x - (base + m[2])))   # last note leads into the next color's key
    return [[base + m[0], -1, base + m[1], -1, base + m[2], -1, base + m[3], -1], [base + m[4], -1, base + m[5], base + m[6], base + m[7], -1, -1, 0],
            [base + m[2], -1, base + m[3], -1, base + 12, -1, base + m[3], -1], [land, -1, -1, -1, 0, 0, 0, 0]]
COLOR_STYLE = {'red': (['brasshits', 'pad'], 'brass2', 'halfpop'), 'orange': (['guitar', 'pad'], 'guitar', 'halfpop'),
               'yellow': (['plastic', 'pluck', 'pad'], 'sqbright', 'fourfloor'), 'green': (['marimbaarp', 'pad'], 'flute', 'fourfloor'),
               'blue': (['pad', 'pluck'], 'fmbell', 'halfpop'), 'indigo': (['dark', 'pad'], 'saw80s', 'halfpop'),
               'violet': (['celesta', 'pad'], 'celesta+voice', 'fourfloor')}
def end_white(M, t0, st, S, i, n, tones, root):   # white light = all the colors together: each color's note sparkles once, red to violet, and they settle on a warm chord
    if i: return
    kick(M, t0, .6)
    for k, (c, nn) in enumerate(COLOR_KEYS): celesta(M, 'glock', t0 + k * 2 * st, nn + 12, 1.5, .35)
    for c in tones[:3] + [tones[0] + 12]: supersaw(M, 'pad', t0, c + 12, 4., .035, cut=2200, a=.3, r=3., voices=3)
    harp(M, t0 + 14 * st, tones[0] + 24, .5)

def build_colors():
    secs, order = {'intro': sec(2, ['Ab', 'Eb'], keys=['pad'])}, ['intro']
    for j, (c, root) in enumerate(COLOR_KEYS):   # every color keeps the pad and a related beat, and its last bar is the next color's 'five' chord, so it glides into the next key
        minor = c in COOL; keys, lead, drums = COLOR_STYLE[c]
        nxt = COLOR_KEYS[j + 1][1] if j + 1 < len(COLOR_KEYS) else None
        ch = key_chords(root, minor)
        if nxt is not None: ch = ch[:3] + [NAMES[(nxt + 7) % 12]]
        secs[c] = sec(4, ch, keys=keys, drums=drums, bass='octave', lead=lead, mel=color_mel(root, minor, nxt), crash=False,
                      kind='verse')
        order.append(c)
    secs['end'] = sec(1, ['E'], extra=end_white, kind='outro'); order.append('end')
    return dict(file='Rainbow_Spectrum', title='Rainbow Spectrum', bpm=116, sections=secs, order=order, chorus_keys=True, cont_tol=0., verb=2.6,
                targets={'verse': -15.5})   # every color is leveled to the same loudness

SONGS = {
 'words': dict(file='Spelled_in_Notes', title='Spelled in Notes', bpm=120, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Am', 'F', 'C', 'G'], keys=['pad'], lead='fmbell', mel=spell('CODED MUSIC'), lv=.7),
   'verse': sec(8, ['Am', 'F', 'C', 'G'], keys=['pluck', 'pad'], drums='halfpop', bass='long', lead='plastic', mel=spell('TAZIZ322 GG WELL PLAYED'), kind='verse'),
   'chorus': sec(8, ['F', 'G', 'Am', 'Am'], keys=['futurebass', 'pluck'], drums='fourfloor', bass='octave', lead='sqbright+plastic', mel=spell('VICTORY ROYALE DROP IN AGAIN'), impact=True, kind='chorus'),
   'end': sec(1, ['Am'], extra=end_words, kind='outro')},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'end']),
 'shapes': dict(file='Polygon_Party', title='Polygon Party', bpm=112, chorus_keys=True, cont_tol=0., sections={
   'circle': sec(2, ['C', 'Am'], extra=circle),
   'triangle': sec(4, ['C', 'Am', 'F', 'G'], extra=chain(circle, TRI), drums='halfpop', bass='long', kind='verse'),
   'square': sec(4, ['C', 'Am', 'F', 'G'], extra=chain(circle, TRI, SQU), drums='halfpop', bass='long', kind='verse'),
   'pentagon': sec(4, ['F', 'G', 'Em', 'Am'], extra=chain(circle, TRI, SQU, PEN), drums='fourfloor', bass='octave', kind='verse'),
   'star': sec(8, ['F', 'G', 'Em', 'Am'], extra=chain(circle, SQU, STAR, HEX), drums='fourfloor', bass='octave', impact=True, kind='chorus'),
   'all': sec(8, ['C', 'Am', 'F', 'G'], extra=chain(circle, TRI, SQU, PEN, HEX, OCT, STAR), drums='fourfloor', bass='octave', kind='chorus'),
   'end': sec(3, ['C'], extra=end_circle, kind='outro')},
   order=['circle', 'triangle', 'square', 'pentagon', 'star', 'all', 'end'], levels={'glock': .9}),
 'colors': build_colors(),
}

import engine
_add = engine.Mix.add
def soft_add(self, bus, t, L, R=None, gain=1., pan=0.):   # sounds that would stop while still ringing (open hats, plucks) fade out over their last quarter instead of cutting off
    L = np.asarray(L, float); n = len(L)
    if n > 64:
        pk = np.abs(L).max() + 1e-9; tail = np.abs(L[-max(8, n // 50):]).max() / pk
        if tail > .03:
            k = max(32, n // 4); f = np.ones(n); f[-k:] = np.cos(np.linspace(0, np.pi / 2, k)) ** 2; L = L * f
            if R is not None: R = np.asarray(R, float) * f
    return _add(self, bus, t, L, R, gain, pan)
SONGS['shapes']['fadeout'] = 4.7   # from 1:06 the song fades away instead of stopping

if __name__ == '__main__':
    print('color notes:', COLOR_KEYS)
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names:
        engine.Mix.add = soft_add if k == 'shapes' else _add
        build(SONGS[k])
