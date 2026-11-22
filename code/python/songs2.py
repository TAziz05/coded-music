"""More songs, in the styles of artists TAziz322 likes. Original melodies and chords; only the style is borrowed.
python songs2.py 6   -> Static Weather (Vocaloid-style J-rock, like inabakumori)
python songs2.py 7   -> Lantern Theory (instrumental jazz / math rock with sax, like Nouvelle Story)"""
import sys
from songs import render, sections_to_bars, ride
from instruments2 import *

def mel8(bars):  # 8 eighth-notes per bar; -1 = hold, 0 = rest
    return melody(bars)

# =====================================================================
# 6) STATIC WEATHER — 146 BPM, D major. Chorused clean guitars, glittery synths,
#    a singing synth lead, soft-but-driving J-rock drums.
# =====================================================================
def static_weather():
    bpm = 146; st = 60 / bpm / 4; B = 16 * st
    C = {'G': ([55, 59, 62, 66], 43), 'A': ([57, 61, 64, 67], 45), 'F#m': ([54, 57, 61, 64], 42), 'Bm': ([59, 62, 66, 69], 47),
         'D': ([57, 62, 66, 69], 38), 'Em': ([55, 59, 62, 64], 40), 'Asus': ([57, 62, 64, 69], 45)}
    verse_p = ['Bm', 'G', 'D', 'A']; pre_p = ['Em', 'F#m', 'G', 'A']; cho_p = ['G', 'A', 'F#m', 'Bm']
    V = mel8([[0,74,-1,73,71,-1,69,-1],[71,-1,-1,0,66,69,71,-1],[74,-1,76,-1,78,-1,76,74],[73,-1,-1,-1,0,0,69,71],
              [74,-1,73,71,-1,69,71,-1],[74,-1,-1,0,76,-1,74,71],[69,-1,71,-1,74,-1,73,71],[69,-1,-1,-1,0,0,0,0]])
    P = mel8([[71,-1,71,74,-1,71,69,-1],[69,-1,69,73,-1,69,66,-1],[67,69,71,74,-1,76,-1,78],[79,-1,-1,-1,76,-1,-1,-1],
              [71,-1,71,74,-1,76,78,-1],[78,-1,76,73,-1,76,78,-1],[79,-1,78,79,-1,81,-1,83],[81,-1,-1,-1,-1,-1,0,0]])
    K = mel8([[78,-1,79,78,-1,74,76,-1],[76,-1,78,76,-1,73,74,-1],[73,-1,74,76,-1,78,81,-1],[78,-1,-1,-1,76,-1,74,-1],
              [78,-1,79,81,-1,79,78,-1],[76,-1,78,79,-1,78,76,-1],[74,-1,76,73,-1,74,69,-1],[71,-1,-1,-1,-1,-1,0,0]])
    secs = [('intro', 8), ('verse', 16), ('pre', 8), ('chorus', 16), ('inter', 8), ('pre', 8), ('chorus', 16), ('outro', 8)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B); prev = [None]
    def sing(mel, i, t0, up=0):
        for s8, nn, L in mel:
            if s8 // 8 == i % 8:
                voice(M, 'lead', t0 + (s8 % 8) * 2 * st, nn + up, L * 2 * st * .93, .55, prev=prev[0]); prev[0] = nn + up
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B
        prog = verse_p if sec in ('verse', 'intro', 'outro') else pre_p if sec == 'pre' else cho_p
        if sec == 'inter': prog = cho_p
        name = prog[i % 4]; tones, root = C[name]
        full = sec in ('chorus',)
        # clean chorused guitar arpeggio (8ths, a 16th pickup every other bar)
        arp = tones + [tones[0] + 12]
        pat = [0, 2, 1, 3, 2, 4, 3, 1]
        for k in range(8):
            guitar(M, 'gtr', t0 + k * 2 * st, arp[pat[k]], 2 * st * 2.2, .16 if not full else .12, pan=-.35, bright=.55)
        if i % 2 and sec != 'intro': guitar(M, 'gtr', t0 + 15 * st, arp[4] + 2, st * 1.5, .1, pan=-.35)
        # second guitar strums in pre and chorus
        if sec in ('pre', 'chorus'):
            for s, dn in ((0, True), (6, False), (8, True), (12, False), (14, True)):
                strum(M, 'gtr2', t0 + s * st, [root + 12] + tones, 2 * st * 1.8, .1, down=dn, pan=.35, bright=.45)
        # glitter: soft high square arp in chorus + interlude
        if sec in ('chorus', 'inter'):
            for k in range(16): pluck(M, 'glit', t0 + k * st, arp[(k * 3) % 5] + 24, st * .8, .045, pan=(-.6, .6)[k % 2], dec=.05, cut=7000)
        # pad
        if sec in ('intro', 'pre', 'inter', 'outro', 'chorus'):
            for nn in tones: supersaw(M, 'pad', t0, nn + 12, B, .04, cut=1500, a=.3, r=.5, voices=3)
        # drums + bass
        if sec in ('verse', 'pre', 'chorus', 'inter') or (sec == 'outro' and i < 4):
            if full:
                for s in (0, 6, 8): kick(M, t0 + s * st, .85)
                for k in range(8): hat(M, t0 + k * 2 * st, .35 if k % 2 else .2, open_=(k % 2 == 1))
                if i % 4 == 0: crash(M, t0, .45)
            else:
                for s in (0, 8, 10): kick(M, t0 + s * st, .75)
                for k in range(8): hat(M, t0 + k * 2 * st, .22 if k % 2 else .14)
            snare(M, t0 + 4 * st, .7); snare(M, t0 + 12 * st, .7)
            if i == n - 1:
                for s, nn in zip(range(8, 16), (52, 52, 48, 48, 45, 45, 41, 41)): tom(M, t0 + s * st, nn, .55, pan=.3 - (s - 8) * .08)
            bl = [(k * 2, root + (12 if k in (3, 7) else 0), 2) for k in range(8)] if full else [(0, root, 3), (3, root, 3), (6, root, 2), (8, root, 3), (11, root + 7, 3), (14, root + 12, 2)]
            for s, nn, L in bl: fbass(M, t0 + s * st, nn, L * st * .9, .6)
        if sec == 'intro' and i == n - 1: riser(M, t0, B, .35)
        if sec == 'pre' and i == n - 1: riser(M, t0, B, .45)
        # the 'vocal' line
        if sec == 'verse': sing(V, i, t0)
        if sec == 'pre': sing(P, i, t0)
        if sec == 'chorus': sing(K, i, t0)
        if sec == 'inter':   # guitar 'solo' answering phrase
            for s8, nn, L in K:
                if s8 // 8 == i % 8: guitar(M, 'gtr', t0 + (s8 % 8) * 2 * st, nn, L * 2 * st, .2, pan=.1, bright=.8, decay=.9985)
        if sec == 'outro' and i == n - 1: strum(M, 'gtr2', t0, [50, 57, 62, 66, 69], B * 1.5, .14)
    M.buses['gtr'] = chorus(M.buses['gtr'], mix=.45); M.buses['gtr2'] = chorus(M.buses['gtr2'], mix=.35)
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .3)
    render(M, 'Static_Weather_146bpm',
           sends={'gtr': .25, 'gtr2': .2, 'lead': .3, 'glit': .5, 'pad': .4, 'drums': .07, 'fx': .3},
           levels={'gtr': 1., 'gtr2': .8, 'lead': 1., 'lead_d': .3, 'glit': .8, 'pad': .7, 'bass': .9, 'drums': .9, 'fx': .7},
           duck=('pad',))

# =====================================================================
# 7) LANTERN THEORY — 150 BPM, E major. Tapped guitar in 7/8, a jazz groove in 4/4,
#    and a saxophone lead. Instrumental math rock / jazz.
# =====================================================================
def lantern_theory():
    bpm = 150; st = 60 / bpm / 4
    A7 = [([57, 61, 64, 68, 71], 45), ([56, 59, 63, 66, 71], 44), ([54, 57, 61, 64, 71], 42), ([59, 64, 66, 68, 71], 40)]   # Amaj9 G#m7 F#m11 Eadd9
    B4 = [([56, 59, 63, 64, 68], 37), ([57, 61, 64, 68, 69], 42), ([57, 61, 64, 66, 69], 47), ([56, 59, 63, 66, 68], 40)]   # C#m9 F#m9 B13sus Emaj9
    C4 = [([57, 61, 64, 68], 45), ([59, 63, 66, 69], 47), ([56, 59, 63, 66], 44), ([56, 61, 64, 68], 49)]                 # Amaj7 B G#m7 C#m
    saxA = [[(0, 76, 4), (4, 75, 2), (6, 73, 4), (10, 71, 4)], [(0, 71, 6), (6, 68, 2), (8, 71, 2), (10, 73, 4)],
            [(0, 69, 4), (4, 73, 4), (8, 76, 2), (10, 78, 4)], [(0, 80, 10), (10, 78, 2), (12, 76, 2)],
            [(0, 76, 4), (4, 78, 2), (6, 80, 4), (10, 81, 4)], [(0, 80, 6), (6, 78, 2), (8, 75, 2), (10, 71, 4)],
            [(0, 73, 4), (4, 76, 4), (8, 78, 6)], [(0, 76, 14)]]
    saxB = [[(0, 80, 3), (3, 78, 3), (6, 76, 2), (8, 75, 4), (12, 73, 4)], [(0, 73, 6), (6, 76, 2), (8, 80, 4), (12, 81, 4)],
            [(0, 80, 4), (4, 78, 2), (6, 76, 2), (8, 73, 8)], [(0, 75, 3), (3, 76, 3), (6, 78, 10)],
            [(0, 80, 3), (3, 78, 3), (6, 76, 2), (8, 75, 4), (12, 73, 4)], [(0, 73, 6), (6, 76, 2), (8, 80, 4), (12, 81, 4)],
            [(0, 83, 4), (4, 81, 2), (6, 80, 2), (8, 78, 8)], [(0, 80, 3), (3, 83, 3), (6, 87, 10)]]
    saxC = [[(0, 81, 16)], [(0, 83, 16)], [(0, 80, 16)], [(0, 76, 8), (8, 78, 8)]]
    secs = [('intro', 7, 4), ('A', 7, 16), ('B', 4, 16), ('C', 4, 8), ('A2', 7, 16), ('B2', 4, 8), ('outro', 7, 4)]
    total = sum((14 if m == 7 else 16) * st * nb for _, m, nb in secs)
    M = Mix(total + 4); T = 0.
    for sec, meter, nb in secs:
        steps = 14 if meter == 7 else 16
        for i in range(nb):
            t0 = T
            if meter == 7:
                tones, root = A7[i % 4]
                # tapped guitar: 16ths, two groups of 7, second group an octave up
                grp = [0, 2, 4, 3, 1, 3, 4]
                for k in range(14):
                    nn = tones[grp[k % 7]] + (12 if k >= 7 else 0)
                    guitar(M, 'gtr', t0 + k * st, nn, st * 2.5, .17 if sec != 'outro' else .14, pan=(-.3 if k < 7 else .3), bright=.75, decay=.996)
                if sec in ('A', 'A2'):
                    for s in (0, 8, 10): kick(M, t0 + s * st, .8)
                    for s in (4, 12): snare(M, t0 + s * st, .7)
                    for s in (2, 7, 13): snare(M, t0 + s * st, .12, pan=.2)
                    for k in range(0, 14, 2): ride(M, t0 + k * st, .7 if k in (0, 4, 8) else .45)
                    if i % 4 == 0: crash(M, t0, .4)
                    for s, L in ((0, 4), (4, 4), (8, 2), (10, 4)): fbass(M, t0 + s * st, root if s != 10 else root + 7, L * st * .9, .6)
                    if sec == 'A2' or i >= 8:
                        for s, nn, L in saxA[i % 8]: sax(M, 'sax', t0 + s * st, nn, L * st * .95, .6)
                if sec == 'outro' and i == nb - 1:
                    strum(M, 'gtr2', t0 + 14 * st, [40, 52, 59, 64, 66, 68, 71], 3.5, .16, gap=.03)
            else:
                prog = B4 if sec in ('B', 'B2') else C4
                tones, root = prog[i % 4]
                if sec in ('B', 'B2'):
                    for s in (0, 7, 10): kick(M, t0 + s * st, .8)
                    for s in (4, 12): snare(M, t0 + s * st, .75)
                    for s in (3, 9, 15): snare(M, t0 + s * st, .12, pan=.2)
                    for k in range(16): hat(M, t0 + k * st, .28 if k % 4 == 2 else .14 if k % 2 else .2, open_=(k == 14))
                    for s in (0, 3, 6, 10, 14):
                        for j, c in enumerate(tones[:4]): epiano(M, 'keys', t0 + s * st + j * .005, c, st * (2.5 if s in (0, 6) else 1.4), .07, pan=(j - 1.5) * .2)
                    for s, nn, L in ((0, root, 3), (3, root + 12, 2), (6, root + 7, 2), (8, root, 3), (11, root + 10, 2), (14, root + 7, 2)):
                        fbass(M, t0 + s * st, nn, L * st * .85, .62)
                    mel = saxB[(i % 8) if sec == 'B' else (4 + i % 4)]
                    for s, nn, L in mel: sax(M, 'sax', t0 + s * st, nn, L * st * .95, .62)
                    if i % 4 == 3:
                        for s, nn in zip((12, 13, 14, 15), (55, 52, 48, 45)): tom(M, t0 + s * st, nn, .5)
                else:  # C: half-time, big strums, long sax notes
                    kick(M, t0, .9); kick(M, t0 + 10 * st, .7); snare(M, t0 + 8 * st, .85)
                    for k in range(0, 16, 2): ride(M, t0 + k * st, .55)
                    if i % 4 == 0: crash(M, t0, .55)
                    strum(M, 'gtr2', t0, [root + 12] + tones, 8 * st, .15, pan=.25, bright=.5)
                    strum(M, 'gtr2', t0 + 10 * st, [root + 12] + tones, 6 * st, .11, down=False, pan=.25, bright=.5)
                    fbass(M, t0, root, 7 * st, .65); fbass(M, t0 + 10 * st, root, 5 * st, .55)
                    for s, nn, L in saxC[i % 4]: sax(M, 'sax', t0 + s * st, nn, L * st * .96, .62)
            T += steps * st
    M.buses['gtr'] = chorus(M.buses['gtr'], depth=.002, mix=.3)
    render(M, 'Lantern_Theory_150bpm',
           sends={'sax': .3, 'gtr': .2, 'gtr2': .25, 'keys': .25, 'drums': .08, 'fx': .25},
           levels={'sax': 1., 'gtr': .9, 'gtr2': .8, 'keys': .8, 'bass': .9, 'drums': .85, 'fx': .7},
           duck=(), fade=3.)

if __name__ == '__main__':
    {'6': static_weather, '7': lantern_theory}[sys.argv[1]]()
