"""DNA: a song read from a real gene, human beta-globin (HBB, part of hemoglobin, which carries oxygen in the blood).
It plays the gene's 444-letter coding sequence from the start codon ATG to the stop codon TAA.
  - The two strands: each base is a note (A = A, C = C, G = G, T = D), three bases (one codon) per beat as triplets.
    The partner strand (A pairs with T, C with G) plays the matching notes an octave lower, and the two strands
    circle around each other in stereo like the double helix.
  - The chords: each codon spells an amino acid. Each bar's most common kind picks the chord:
    oily/water-avoiding amino acids = Am, water-loving = C, positively charged = F, negatively charged = G.
  - The sections are the gene's three exons (the parts that code the protein): codons 1-30, 31-104 and 105-146,
    so the song changes exactly where the gene does. In the last exon a lead plays the protein itself:
    the more water-loving each amino acid is (Kyte-Doolittle scale), the higher its note.
  - At the stop codon TAA everything stops and the last bases echo away.
python dna.py"""
import numpy as np
from newstyles import *
from popkit import build, LEADS
from songs5 import harp

HBB = ("ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCC"
       "TTGGACCCAGAGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAGGTGAAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTG"
       "ATGGCCTGGCTCACCTGGACAACCTCAAGGGCACCTTTGCCACACTGAGTGAGCTGCACTGTGACAAGCTGCACGTGGATCCTGAGAACTTCAGGCTCCTGGGCAACGTGC"
       "TGGTCTGTGTGCTGGCCCATCACTTTGGCAAAGAATTCACCCCACCAGTGCAGGCTGCCTATCAGAAAGTGGTGGCTGGTGTGGCTAATGCCCTGGCCCACAAGTATCACTAA")
B4 = "TCAG"; AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODE = {a + b + c: AA[16 * i + 4 * j + k] for i, a in enumerate(B4) for j, b in enumerate(B4) for k, c in enumerate(B4)}
CODONS = [HBB[i:i + 3] for i in range(0, len(HBB), 3)]
PROT = ''.join(CODE[c] for c in CODONS)
assert PROT.startswith('MVHLTPEEK') and PROT.endswith('HKYH*')   # the real beta-globin protein
NOTE = {'A': 57, 'C': 60, 'G': 55, 'T': 62}
PAIR = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
KIND = {**{a: 'oily' for a in 'AVLIMFWPG'}, **{a: 'water' for a in 'STCYNQ'}, **{a: 'plus' for a in 'KRH'}, **{a: 'minus' for a in 'DE'}, '*': 'stop'}
CHORD = {'oily': 'Am', 'water': 'C', 'plus': 'F', 'minus': 'G', 'stop': 'Am'}
KD = {'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5, 'M': 1.9, 'A': 1.8, 'G': -.4, 'T': -.7, 'S': -.8, 'W': -.9, 'Y': -1.3, 'P': -1.6,
      'H': -3.2, 'E': -3.5, 'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5}
PENTA = [57, 60, 62, 64, 67, 69, 72, 74, 76, 79, 81]
EXONS = [(0, 30), (30, 104), (104, 147)]   # codon ranges (the last one includes the stop codon)

def bars_of(a, b): return (b - a + 3) // 4
def chords_for(a, b):
    out = []
    for k in range(a, b, 4):
        kinds = [KIND[PROT[j]] for j in range(k, min(b, k + 4))]
        out.append(CHORD[max(set(kinds), key=kinds.count)])
    return out

def strands(a, b, lead=False, swirl=True):
    def f(M, t0, st, S, i, n, tones, root):
        beat = 4 * st
        for q in range(4):
            j = a + 4 * i + q
            if j >= b:   # the gap where an intron sits in the gene: the last codon echoes softly
                if b < len(CODONS):
                    for k, base in enumerate(CODONS[b - 1]): LEADS['marimba'](M, t0 + q * beat + k * beat / 3, NOTE[base] + 12, beat / 3 * .9, .35 * .7 ** (j - b))
                continue
            codon = CODONS[j]; tb = t0 + q * beat
            for k, base in enumerate(codon):
                t = tb + k * beat / 3; ph = (j * 3 + k) / 6.
                pan = .7 * np.sin(2 * np.pi * ph) if swirl else 0
                LEADS['marimba'](M, t, NOTE[base] + 12, beat / 3 * .9, .55)
                celesta(M, 'glock', t, NOTE[PAIR[base]], beat / 3 * .9, .25 * (1 + .3 * pan))
            if lead and PROT[j] != '*':   # the protein: water-loving = higher
                d = int(round((4.5 - KD[PROT[j]]) / 9 * (len(PENTA) - 1)))
                LEADS['flute'](M, tb, PENTA[d] + 12, beat * .95, .55)
            if PROT[j] == '*': stop_codon(M, tb, beat, codon)
    return f
def stop_codon(M, t, beat, codon):   # TAA: the stop codon. The last bases echo away
    for r in range(1, 7):
        for k, base in enumerate(codon): LEADS['marimba'](M, t + r * beat + k * beat / 3, NOTE[base] + 12, beat / 3 * .9, .5 * .6 ** r)
    harp(M, t + beat, 69, .5)
def start_codon(M, t0, st, S, i, n, tones, root):   # before the gene: a bell for the start codon ATG
    if i == 1:
        for k, base in enumerate('ATG'): celesta(M, 'glock', t0 + 8 * st + k * 4 * st / 3, NOTE[base] + 24, 1.5, .5)

(a1, b1), (a2, b2), (a3, b3) = EXONS
SONG = dict(file='DNA', title='DNA (Beta-Globin)', bpm=104, chorus_keys=True, cont_tol=0., verb=2.6, sections={
   'intro': sec(2, ['Am', 'Am'], keys=['pad'], extra=start_codon),
   'exon1': sec(bars_of(a1, b1), chords_for(a1, b1), keys=['pad'], extra=strands(a1, b1), kind='verse'),
   'exon2': sec(bars_of(a2, b2), chords_for(a2, b2), keys=['pad', 'ep'], drums='halfpop', bass='long', extra=strands(a2, b2), crash=False, kind='verse'),
   'exon3': sec(bars_of(a3, b3), chords_for(a3, b3), keys=['pad', 'ep'], drums='halfpop', bass='long', extra=strands(a3, b3, lead=True), crash=False, kind='verse'),
   'end': sec(2, ['Am', 'Am'], keys=[], kind='outro')},
   order=['intro', 'exon1', 'exon2', 'exon3', 'end'], gain_like={'intro': 'exon2', 'exon1': 'exon2', 'exon3': 'exon2', 'end': 'exon2'})

if __name__ == '__main__':
    print(len(CODONS), 'codons:', PROT)
    build(SONG)
