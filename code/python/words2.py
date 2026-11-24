"""More songs made from words (all sounds are code):
  Gamer Tags        NOSCOPE68, BATTLEBUS12098, TAZIZ322, PKG315 and DSX spelled as a phonk cowbell melody
                    (each letter is a note: A-G as named, then H=A, I=B ... around again; digits are steps up the scale)
  Morse Code        the rhythm is real Morse code on a 16th-note grid (dit = 1 step, dah = 3, 1 step between signals,
                    3 between letters, 7 between words), and each letter's beeps sit on that letter's note.
                    It sends CQ (calling anyone), CODED MUSIC, GG WP, VICTORY ROYALE, and signs off with SK (end of contact)
  The Good Ol' Days a poem set to music: one note per syllable, each word starting on its first letter's note and falling
                    like speech, one line of the poem per phrase; the music follows what the lines say
python words2.py all  (or: tags morse poem)"""
import sys, re
import numpy as np
from newstyles import *
from popkit import build, LEADS
from songs5 import harp
from concepts import spell, LETTER, DIGIT, rows_from

# ---------------- gamer tags ----------------
def spell_hits(text):   # like spell(), but every letter is one short hit, the last letter of a word too (so X sounds like D and S)
    out = []
    for w in text.upper().split():
        out += [(LETTER.get(c) or DIGIT.get(c)) + 12 for c in w if c in LETTER or c in DIGIT] + [0]
    return rows_from(out)
def end_gg(M, t0, st, S, i, n, tones, root):   # spells G-G, then a pitched-down 'ay'
    if i: return
    for k, c in enumerate('GG'): LEADS['cowbell'](M, t0 + S(2 * k), LETTER[c] + 12, st * 1.5, 1.)   # G-G, the same hits as the melody
    ayy(M, t0 + S(6), .8); kick(M, t0 + S(6), .9)
    for c in tones[:3]: supersaw(M, 'pad', t0 + S(6), c, 2.5, .03, cut=900, a=.01, r=1.5, voices=3)

TAGS = dict(file='Gamer_Tags', title='Gamer Tags', bpm=128, chorus_keys=False, cont_tol=0., sections={
   'intro': sec(4, ['Am', 'F', 'Dm', 'E'], keys=['dark'], lead='fmbell', mel=spell_hits('DSX DSX'), lv=.8),
   'verse': sec(8, ['Am', 'F', 'Dm', 'E'], keys=['dark'], drums='phonk', bass='808', lead='cowbell', mel=spell_hits('NOSCOPE68 PKG315 DSX'), kind='verse'),
   'chorus': sec(8, ['F', 'G', 'Am', 'E'], keys=['dark', 'pad'], drums='phonk', bass='808', lead='cowbell+fmbell', mel=spell_hits('BATTLEBUS12098 TAZIZ322'), impact=True, kind='chorus'),
   'end': sec(1, ['Am'], extra=end_gg, fill=False, kind='outro')},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'end'], levels={'lead': 1.2})

# ---------------- morse ----------------
MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
         'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
         'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--'}
def morse(text):   # -> [(step, length, letter)] on a 16th grid, standard Morse timing
    ev, s = [], 0
    for w in text.upper().split():
        for c in w:
            for sym in MORSE[c]:
                L = 1 if sym == '.' else 3; ev.append((s, L, c)); s += L + 1
            s += 2   # 3 steps between letters (1 already added)
        s += 4       # 7 steps between words
    return ev, s
def beeps(text, inst='sqbright', vol=.9, oct_=12, every=None):
    ev, total = morse(text)
    span = (total + 15) // 16 * 16   # the message, padded to whole bars, repeats through the section
    def f(M, t0, st, S, i, n, tones, root):
        off = (i * 16) % span
        for s, L, c in ev:
            k = s - off
            if 0 <= k < 16: LEADS[inst](M, t0 + S(k), (LETTER.get(c) or DIGIT[c]) + oct_, L * st * .9, vol)
    return f
def static(M, t0, st, S, i, n, tones, root):   # radio hiss under the intro
    N = int(16 * st * SR); M.add('fx', t0, bp(noise(N), 1500, 5000) * .02 * (.6 + .4 * np.sin(np.linspace(0, 6, N))))
def end_sk(M, t0, st, S, i, n, tones, root):   # SK = end of contact: ... -.-  then the radio goes quiet
    if i: return
    for s, L, c in morse('SK')[0]: LEADS['sqbright'](M, t0 + S(s), LETTER[c] + 12, L * st * .9, .8)
    for c in tones[:3]: epiano(M, 'keys', t0 + S(14), c + 12, 2.5, .1)
    static(M, t0, st, S, 0, 1, tones, root)
def chain(*fs):
    def f(*a):
        for g in fs: g(*a)
    return f

MORSE_SONG = dict(file='Morse_Code', title='Morse Code', bpm=120, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Am', 'F', 'C', 'G'], keys=['pad'], extra=chain(static, beeps('CQ CQ', 'sqbright', .7))),
   'verse': sec(8, ['Am', 'F', 'C', 'G'], keys=['pad', 'pluck'], drums='halfpop', bass='long', extra=beeps('CODED MUSIC'), kind='verse'),
   'pre': sec(4, ['F', 'G', 'F', 'G'], keys=['pad', 'pluck'], drums='halfpop', bass='long', extra=beeps('GG WP', 'fmbell', .9), kind='verse'),
   'chorus': sec(8, ['F', 'G', 'Am', 'Am'], keys=['futurebass', 'pad'], drums='fourfloor', bass='octave', extra=chain(beeps('VICTORY ROYALE'), beeps('VICTORY ROYALE', 'fmbell', .5, 0)), impact=True, kind='chorus'),
   'end': sec(1, ['Am'], extra=end_sk, kind='outro')},
   order=['intro', 'verse', 'pre', 'chorus', 'verse', 'pre', 'chorus', 'end'], gain_like={'pre': 'verse'})

# ---------------- The Good Ol' Days (poem by TAziz322) ----------------
POEM = ["Do you leave the lights on", "with the blinds opened and doors ajar",
        "while the adults discuss what to do after her passing,", "and the children cherishing the final moments, with no drama here?",
        "Even after secrets spill, you'll never know who's telling the lie", "or who is in the right,",
        "since the past key doesn't lead to the future gate,", "but to a time of warm sunshine", "and blue skies on the overgrown blades of grass.",
        "The same man doesn't visit the same waterfall twice,", "as the past shrivels and the present is continuous,",
        "while simultaneously the future is unpredictable,", "life won't be the same, the moment that you leave."]
SCALE = [57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79]   # A minor, two octaves
def syllables(w):
    w = re.sub(r'[^a-z]', '', w.lower()); n = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and n > 1 and not w.endswith(('le', 'ee')): n -= 1
    return max(1, n)
def line_notes(line, lift=0):   # one 8th note per syllable; a word starts on its first letter's note and steps down; the last word is held
    out = []; words = line.split()
    for j, w in enumerate(words):
        c = re.sub(r'[^A-Za-z]', '', w)[:1].upper() or 'A'
        d = SCALE.index(LETTER[c]) + lift; ns = [SCALE[max(0, min(len(SCALE) - 1, d - k))] + 12 for k in range(syllables(w))]
        out += ns
        if w[-1] in ',?.': out += [-1]   # a comma or the end of a sentence: a breath
    out += [-1, -1, 0]
    return out
def phrase(lines, lift=0):
    out = []
    for l in lines: out += line_notes(l, lift)
    return rows_from(out)
def end_leave(M, t0, st, S, i, n, tones, root):   # '...the moment that you leave': everything else stops, one note rings on
    if i: return
    LEADS['piano'](M, t0, 69, 4., .6); harp(M, t0 + 8 * st, 81, .4)
    for c in tones[:3]: supersaw(M, 'pad', t0, c + 12, 4., .02, cut=1200, a=.4, r=3., voices=3)
def bars_for(rows): return len(rows)
P1, P2, P3, P4, P5 = phrase(POEM[0:2]), phrase(POEM[2:4]), phrase(POEM[4:7]), phrase(POEM[7:10], 2), phrase(POEM[10:13])
POEM_SONG = dict(file='The_Good_Ol_Days', title="The Good Ol' Days", bpm=84, chorus_keys=True, cont_tol=0., verb=2.8, sections={
   'intro': sec(4, ['Am', 'F', 'C', 'G'], keys=['pad']),
   'home': sec(bars_for(P1), ['Am', 'F', 'C', 'G'], keys=['pad', 'piano'], lead='piano', mel=P1, kind='verse'),                    # the house, lights on
   'family': sec(bars_for(P2), ['Am', 'F', 'C', 'E'], keys=['pad', 'piano'], drums='lofi', lead='piano', mel=P2, kind='verse'),    # the adults and the children
   'secrets': sec(bars_for(P3), ['Dm', 'Am', 'E', 'Am'], keys=['pad', 'piano'], drums='lofi', bass='long', lead='piano+strings', mel=P3, kind='verse'),   # secrets, the past key
   'sunshine': sec(bars_for(P4), ['C', 'G', 'F', 'C'], keys=['pad', 'emoacoustic'], drums='lofi', bass='long', lead='flute', mel=P4, kind='verse'),   # warm sunshine, blue skies, the waterfall
   'leave': sec(bars_for(P5), ['F', 'G', 'Am', 'Am'], keys=['pad', 'piano'], drums='lofi', bass='long', lead='piano+strings', mel=P5, kind='verse'),   # the past shrivels, life won't be the same
   'end': sec(2, ['Am'], extra=end_leave, kind='outro')},
   order=['intro', 'home', 'family', 'secrets', 'sunshine', 'leave', 'end'],
   gain_like={'family': 'home', 'secrets': 'home', 'sunshine': 'home', 'leave': 'home', 'end': 'home'})

# ---------------- Morse songs inspired by the things TAziz322 plays and listens to ----------------
def morse_drums(text, every_bar=True):   # the drum kit plays Morse code: a dah is a kick (and a clap on long gaps), a dit is a hi-hat
    ev, total = morse(text); span = (total + 15) // 16 * 16
    def f(M, t0, st, S, i, n, tones, root):
        off = (i * 16) % span
        for s_, L, c in ev:
            k = s_ - off
            if 0 <= k < 16:
                if L == 3: kick(M, t0 + S(k), .85)
                else: hat(M, t0 + S(k), .55)
        snare(M, t0 + S(4), .5); snare(M, t0 + S(12), .5)
    return f
def end_gg_beeps(M, t0, st, S, i, n, tones, root):   # G G in Morse (--. --.), then the lobby goes quiet
    if i: return
    for s_, L, c in morse('GG')[0]: LEADS['sqbright'](M, t0 + S(s_), LETTER[c] + 12, L * st * .9, .8)
    for c in tones[:3]: supersaw(M, 'pad', t0 + S(14), c + 12, 2.5, .03, cut=1800, a=.05, r=2., voices=3)
def end_levelup(M, t0, st, S, i, n, tones, root):    # a little level-up jingle in Game Boy squares (original)
    if i: return
    for k, d in enumerate([0, 4, 7, 12, 7, 12, 16]): LEADS['gb'](M, t0 + S(k), tones[0] + 12 + d, st * (.9 if k < 6 else 6), .7)
def end_seven(M, t0, st, S, i, n, tones, root):      # seven chimes, one for each member, rising, then a warm chord
    if i: return
    for k in range(7): celesta(M, 'glock', t0 + S(2 * k), [64, 67, 69, 71, 74, 76, 79][k] + 12, 1.5, .5)
    for c in tones[:3]: supersaw(M, 'pad', t0 + S(14), c + 12, 3., .035, cut=2200, a=.1, r=2.5, voices=3)

MORSE_FN = dict(file='Dits_Royale', title='Dits Royale', bpm=140, chorus_keys=True, cont_tol=0., sections={   # Fortnite: the beeps call out the match
   'drop': sec(4, ['Em', 'C', 'G', 'D'], keys=['pad'], extra=chain(static, beeps('DROP DROP', 'sqbright', .7))),
   'loot': sec(8, ['Em', 'C', 'G', 'D'], keys=['pluck', 'pad'], drums='halfpop', bass='octave', extra=beeps('LOOT STORM'), kind='verse'),
   'build': sec(4, ['C', 'D', 'C', 'D'], keys=['pluck', 'pad'], drums='halfpop', bass='octave', extra=beeps('BUS', 'fmbell'), kind='verse'),
   'win': sec(8, ['C', 'D', 'Em', 'Em'], keys=['futurebass', 'pad'], drums='fourfloor', bass='reese', extra=chain(beeps('VICTORY ROYALE', 'saw80s'), beeps('VICTORY ROYALE', 'fmbell', .5, 0)), impact=True, kind='chorus'),
   'end': sec(1, ['Em'], extra=end_gg_beeps, fill=False, kind='outro')},
   order=['drop', 'loot', 'build', 'win', 'loot', 'build', 'win', 'end'], gain_like={'build': 'loot', 'end': 'loot'})
MORSE_PK = dict(file='Morse_Catch', title='Morse Catch', bpm=150, chorus_keys=True, cont_tol=0., crush=(22050, 10), sections={   # Pokémon: Game Boy squares sending trainer words
   'route': sec(8, ['C', 'F', 'G', 'C'], keys=['gbarp'], drums='halfpop', bass='octave', extra=beeps('ROUTE TRAINER', 'gb'), kind='verse'),
   'battle': sec(8, ['Am', 'F', 'G', 'E'], keys=['gbarp'], drums='fourfloor', bass='octave', extra=chain(beeps('CATCH EVOLVE', 'gb'), beeps('CATCH EVOLVE', 'gb12', .45, 0)), kind='chorus'),
   'gym': sec(8, ['F', 'G', 'Em', 'Am'], keys=['gbarp'], drums='fourfloor', bass='octave', extra=beeps('GYM BADGE', 'gb'), kind='chorus'),
   'end': sec(1, ['C'], extra=end_levelup, fill=False, kind='outro')},
   order=['route', 'battle', 'route', 'gym', 'battle', 'end'], gain_like={'gym': 'battle', 'route': 'battle', 'end': 'battle'})
MORSE_BTS = dict(file='Purple_in_Morse', title='Purple in Morse', bpm=112, chorus_keys=True, cont_tol=0., sections={   # BTS: the drums play I PURPLE YOU in Morse
   'intro': sec(4, ['Bm', 'G', 'D', 'A'], keys=['pad'], extra=beeps('ARMY', 'fmbell', .7)),
   'verse': sec(8, ['Bm', 'G', 'D', 'A'], keys=['ep', 'pad'], bass='long', lead='synth', mel=spell_hits('ARMY BORAHAE'), extra=morse_drums('I PURPLE YOU'), kind='verse'),
   'chorus': sec(8, ['G', 'A', 'Bm', 'D'], keys=['futurebass', 'pad'], bass='octave', lead='synth', mel=spell_hits('I PURPLE YOU'), extra=chain(morse_drums('I PURPLE YOU'), beeps('BORAHAE', 'fmbell', .45, 0)), impact=True, kind='chorus'),
   'end': sec(1, ['D'], extra=end_seven, fill=False, kind='outro')},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'end'], gain_like={'end': 'chorus'})

SONGS = {'tags': TAGS, 'morse': MORSE_SONG, 'poem': POEM_SONG, 'mfn': MORSE_FN, 'mpk': MORSE_PK, 'mbts': MORSE_BTS}
if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
