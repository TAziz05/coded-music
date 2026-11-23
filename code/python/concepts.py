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
def polygon(sides, inst, every=1, order=None):    # 'sides' evenly spaced hits per bar (true polyrhythm, not on the 16th grid); notes walk the corners
    def f(M, t0, st, S, i, n, tones, root):
        if i % every: return
        bar = 16 * st; corners = [tones[k % len(tones)] + 12 * (k // len(tones)) for k in range(sides)]
        seq = order(sides) if order else list(range(sides))
        for j in range(sides): inst(M, t0 + j * bar / sides, corners[seq[j]] + 12)
    return f
def star(n): return [(2 * k) % n for k in range(n)]          # a star polygon: visit every other corner (0, 2, 4, 1, 3)
TRI = polygon(3, lambda M, t, nn: marimba(M, 'keys', t, nn, .3, .8, pan=-.4))
SQU = polygon(4, lambda M, t, nn: pizz(M, t, nn - 12, .8, pan=.4))
PEN = polygon(5, lambda M, t, nn: celesta(M, 'glock', t, nn, .25, .6, pan=.2))
HEX = polygon(6, lambda M, t, nn: woodblock(M, t, nn % 2 == 0, .5))
OCT = polygon(8, lambda M, t, nn: hat(M, t, .25))
STAR = polygon(5, lambda M, t, nn: plastic(M, 'lead', t, nn + 12, .3, .9), order=star)
def circle(M, t0, st, S, i, n, tones, root):      # a circle has no corners: one smooth swell
    if i % 2 == 0:
        for c in tones[:3]: supersaw(M, 'pad', t0, c + 12, 32 * st, .045, cut=1500, a=1.5 * 16 * st, r=1., voices=3)
def end_circle(M, t0, st, S, i, n, tones, root):  # all the shapes once more, then they melt into one circle
    if i: return
    for f in (TRI, SQU, PEN, HEX, OCT): f(M, t0, st, S, 0, 1, tones, root)
    te = t0 + 16 * st; kick(M, te, .9)
    for c in tones[:3] + [tones[0] + 12]: supersaw(M, 'pad', te, c + 12, 4., .05, cut=1800, a=.05, r=2., voices=4)
    harp(M, te, tones[0] + 24, .8)

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
def color_mel(root, minor):
    m = MOT_MIN if minor else MOT_MAJ; base = root
    return [[base + m[0], -1, base + m[1], -1, base + m[2], -1, base + m[3], -1], [base + m[4], -1, base + m[5], base + m[6], base + m[7], -1, -1, 0],
            [base + m[2], -1, base + m[3], -1, base + 12, -1, base + m[3], -1], [base + m[2], -1, -1, -1, 0, 0, 0, 0]]
COLOR_STYLE = {'red': (['brasshits', 'pad'], 'brass2', 'rock'), 'orange': (['guitar', 'pad'], 'guitar', 'funk'),
               'yellow': (['plastic', 'pluck'], 'sqbright', 'fourfloor'), 'green': (['marimbaarp'], 'flute', 'calypso'),
               'blue': (['pad', 'pluck'], 'fmbell', 'halfpop'), 'indigo': (['dark', 'pad'], 'saw80s', 'halfpop'),
               'violet': (['celesta', 'pad'], 'celesta+voice', 'fourfloor')}
def end_white(M, t0, st, S, i, n, tones, root):   # white light = every color at once: all seven color notes in one shimmering chord
    if i: return
    kick(M, t0, .9); crash(M, t0, .6)
    for c, nn in COLOR_KEYS:
        supersaw(M, 'pad', t0, nn, 4., .03, cut=3000, a=.02, r=2.5, voices=3); celesta(M, 'glock', t0 + (nn - 68) * .05, nn + 12, 2., .4)

def build_colors():
    secs, order = {'intro': sec(2, ['Ab', 'Eb'], keys=['pad'])}, ['intro']
    for c, root in COLOR_KEYS:
        minor = c in COOL; keys, lead, drums = COLOR_STYLE[c]
        secs[c] = sec(4, key_chords(root, minor), keys=keys, drums=drums, bass='octave', lead=lead, mel=color_mel(root, minor), crash=True,
                      kind='chorus' if c in ('yellow', 'violet') else 'verse')
        order.append(c)
    secs['end'] = sec(1, ['E'], extra=end_white, kind='outro'); order.append('end')
    return dict(file='Rainbow_Spectrum', title='Rainbow Spectrum', bpm=116, sections=secs, order=order, chorus_keys=True, cont_tol=0., verb=2.6)

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
   'end': sec(1, ['C'], extra=end_circle, kind='outro')},
   order=['circle', 'triangle', 'square', 'pentagon', 'star', 'all', 'end'], levels={'glock': .9}),
 'colors': build_colors(),
}

if __name__ == '__main__':
    print('color notes:', COLOR_KEYS)
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
