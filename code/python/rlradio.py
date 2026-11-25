"""Original car-soccer stadium electronic songs in the styles you hear on Rocket League's radio (Monstercat and its
labels): electro house, future bass (the melodic Instinct side), dubstep (the heavy Uncaged side), drum & bass,
glitch hop (classic Monstercat) and melodic progressive house. New melodies; every song has its own shape and ending.
All sounds are code. python rlradio.py all  (or keys from SONGS)"""
import sys
import numpy as np
from newstyles import *
from popkit import build, LEADS
from songs5 import harp

def roll(M, t0, st, S, i, n, tones, root):   # a build: a riser across the section and a snare roll that speeds up in the last 2 bars
    if i == 0: riser(M, t0, n * 16 * st, .3)
    if i >= n - 2:
        k = i - (n - 2); step = [4, 2][k]
        for s in range(0, 16, step): snare(M, t0 + S(s), .18 + .12 * (k * 16 + s) / 32)
        if k == 1:
            for s in range(8, 16): snare(M, t0 + S(s) + st / 2, .25)
def hit(M, t0, st, S, i, n, tones, root):    # an impact on the first beat of a drop
    if i == 0: impact(M, t0, .45)
def stutter_out(inst, notes):                 # a glitch ending: the last chord stutters faster and shorter, then stops
    def f(M, t0, st, S, i, n, tones, root):
        if i: return
        t, d = t0, 2 * st
        for r in range(14):
            for c in notes: LEADS[inst](M, t, c, d * .7, .7 * .93 ** r)
            t += d; d *= .82
    return f
def dj_outro(M, t0, st, S, i, n, tones, root):   # electro-house style: only the kick and hats for the last bars, then one last kick
    if i == n - 1: kick(M, t0 + 16 * st, .9); crash(M, t0 + 16 * st, .35)
def vocal_chop_tail(M, t0, st, S, i, n, tones, root):   # future bass: a last pitched chop, an octave up, ringing out
    if i == 0:
        for c in tones[:3]: supersaw(M, 'pad', t0, c + 24, 2.5, .035, cut=4000, a=.01, r=2., voices=5)
        LEADS['vocoder'](M, t0, tones[0] + 24, 1.5, .8)

R = -1
EVEN = {'intro': -15.5, 'verse': -14., 'pre': -14., 'chorus': -13.5, 'drop': -13.5, 'bridge': -14.5, 'break': -14.5, 'outro': -15.}   # every part of a song at nearly the same loudness, so nothing jumps
SONGS = {
 # electro house: kick from the first beat, a long build, two big drops, a DJ-style drums-only outro
 'electro': dict(file='Turbo_Kickoff', title='Turbo Kickoff', bpm=128, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(8, ['Fm', 'Db', 'Ab', 'Eb'], keys=['pluck'], drums='fourfloor', kind='verse'),
   'build': sec(8, ['Fm', 'Db', 'Ab', 'Eb'], keys=['pluck', 'pad'], drums='halfpop', lead='sqbright',
                mel=[[77,R,80,R,82,R,80,R],[77,R,R,R,75,R,R,R],[77,R,80,R,84,R,82,R],[80,R,R,R,0,0,0,0]], extra=roll, kind='verse'),
   'drop': sec(16, ['Fm', 'Db', 'Ab', 'Eb'], keys=['stabs'], drums='fourfloor', bass='reese', lead='saw80s',
               mel=[[89,R,89,87,R,84,R,R],[85,R,R,84,R,80,R,R],[89,R,89,87,R,84,R,92],[91,R,R,R,87,R,R,R]], extra=hit, impact=True, kind='chorus'),
   'break': sec(8, ['Db', 'Ab', 'Eb', 'Fm'], keys=['pad', 'piano'], lead='piano',
                mel=[[77,R,R,80,R,R,82,R],[80,R,R,R,0,0,0,0],[77,R,R,80,R,R,84,R],[82,R,R,R,0,0,0,0]], kind='bridge'),
   'build2': sec(4, ['Db', 'Eb', 'Fm', 'Fm'], keys=['pluck', 'pad'], drums='halfpop', extra=roll, kind='verse'),
   'outro': sec(4, ['Fm'], drums='fourfloor', extra=dj_outro, fill=False, kind='outro')},
   order=['intro', 'build', 'drop', 'break', 'build2', 'drop', 'outro'], targets=EVEN, ride=1.),
 # future bass (Instinct side): starts cold on the vocal-chop hook, half-time trap drops with chord chops, ends on one chop ringing
 'future': dict(file='Aerial_Boost', title='Aerial Boost', bpm=150, chorus_keys=True, cont_tol=5., sections={
   'hook': sec(4, ['D', 'A', 'Bm', 'G'], keys=['pad'], lead='vocoder',
               mel=[[78,R,81,R,83,R,81,78],[76,R,R,R,0,0,0,0],[78,R,81,R,86,R,85,R],[83,R,R,R,0,0,0,0]], kind='verse'),
   'verse': sec(8, ['D', 'A', 'Bm', 'G'], keys=['pluck', 'pad'], drums='trap', bass='808', lead='vocoder',
                mel=[[74,R,76,R,78,R,R,0],[76,R,74,R,71,R,0,0],[74,R,76,R,78,R,81,R],[79,R,R,R,0,0,0,0]], kind='verse'),
   'build': sec(4, ['G', 'A', 'Bm', 'A'], keys=['pad'], lead='vocoder', mel=[[78,R,81,R,83,R,81,78],[76,R,R,R,0,0,0,0],[78,R,81,R,86,R,85,R],[83,R,R,R,0,0,0,0]], extra=roll, kind='verse'),
   'drop': sec(8, ['D', 'A', 'Bm', 'G'], keys=['futurebass', 'pad'], drums='trap', bass='808', lead='plastic', lv=.6,
               mel=[[90,R,88,R,85,R,83,R],[85,R,R,83,R,81,R,R],[83,R,85,R,88,R,90,R],[88,R,R,R,0,0,0,0]], extra=hit, impact=True, kind='chorus'),
   'end': sec(1, ['D'], extra=vocal_chop_tail, fill=False, kind='outro')},
   order=['hook', 'verse', 'build', 'drop', 'verse', 'build', 'drop', 'end'], targets=EVEN, ride=1.),
 # dubstep (Uncaged side): a dark intro with an impact, wobble-bass drops, a short break, ends with the band slowing to a halt
 'dubstep': dict(file='Demolition_Line', title='Demolition Line', bpm=150, chorus_keys=False, cont_tol=0., sections={
   'intro': sec(4, ['Em', 'C', 'Am', 'B'], keys=['dark'], extra=hit),
   'build': sec(8, ['Em', 'C', 'Am', 'B'], keys=['dark', 'pad'], drums='halfpop', lead='saw80s',
                mel=[[76,R,R,79,R,R,78,R],[76,R,R,R,71,R,R,R],[76,R,R,79,R,R,83,R],[82,R,R,R,0,0,0,0]], extra=roll, kind='verse'),
   'drop': sec(8, ['Em', 'Em', 'C', 'B'], keys=['pad'], drums='dubstep', bass='wobble', lead='saw80s',
               mel=[[88,R,0,88,R,0,86,R],[83,R,R,R,0,0,0,0],[88,R,0,88,R,0,91,R],[90,R,R,R,0,0,0,0]], extra=hit, impact=True, kind='chorus'),
   'break': sec(4, ['C', 'Am', 'B', 'B'], keys=['pad'], lead='piano', mel=[[76,R,R,79,R,R,78,R],[76,R,R,R,0,0,0,0],[76,R,R,79,R,R,83,R],[82,R,R,R,0,0,0,0]], kind='bridge'),
   'drop2': sec(8, ['Em', 'Em', 'C', 'B'], keys=['glitchheavy'], drums='dubstep', bass='wobble', lead='saw80s',
                mel=[[88,R,0,88,R,0,86,R],[83,R,R,R,0,0,0,0],[88,R,0,88,R,0,91,R],[90,R,R,R,0,0,0,0]], extra=hit, impact=True, kind='chorus'),
   'end': sec(1, ['Em'], drums='dubstep', bass='wobble', kind='outro')},
   order=['intro', 'build', 'drop', 'break', 'drop2', 'break', 'drop2', 'end'], tapestop=True, targets=EVEN, ride=1.),
 # drum & bass: drums first, rolling reese drops, a pad breakdown, ends with the last bar echoing away
 'dnb': dict(file='Overtime_Run', title='Overtime Run', bpm=174, chorus_keys=True, cont_tol=0., sections={
   'drums': sec(4, ['Am', 'Am', 'F', 'G'], drums='dnb', kind='verse'),
   'verse': sec(8, ['Am', 'F', 'C', 'G'], keys=['pad'], drums='dnb', bass='sub', lead='sqbright', lv=.75,
                mel=[[81,R,R,79,R,76,R,R],[77,R,R,76,R,72,R,R],[74,R,R,76,R,77,R,79],[76,R,R,R,0,0,0,0]], kind='verse'),
   'drop': sec(16, ['Am', 'F', 'C', 'G'], keys=['stabs', 'pad'], drums='dnb', bass='reese', lead='saw80s', lv=.85,
               mel=[[81,R,R,79,R,76,R,R],[77,R,R,76,R,72,R,R],[74,R,R,76,R,77,R,79],[76,R,R,R,0,0,0,0]], extra=hit, impact=True, kind='chorus'),
   'break': sec(8, ['F', 'G', 'Am', 'Am'], keys=['pad', 'piano'], lead='piano', mel=[[81,R,R,79,R,76,R,R],[77,R,R,R,0,0,0,0],[74,R,R,76,R,77,R,79],[76,R,R,R,0,0,0,0]], extra=roll, kind='bridge')},
   order=['drums', 'verse', 'drop', 'break', 'drop'], echo_out=(8, .55, 7), targets=EVEN, ride=1.),
 # glitch hop: swung, funky, stuttering; ends with the last chord glitching faster until it stops
 'glitch': dict(file='Ceiling_Shot', title='Ceiling Shot', bpm=110, swing=.14, chorus_keys=True, cont_tol=0., sections={
   'intro': sec(4, ['Gm', 'Eb', 'Bb', 'F'], keys=['ep'], drums='boombap', kind='verse'),
   'verse': sec(8, ['Gm', 'Eb', 'Bb', 'F'], keys=['ep'], drums='boombap', bass='funky', lead='synth',
                mel=[[79,R,0,77,79,R,82,R],[79,R,R,0,77,R,74,R],[79,R,0,77,79,R,84,R],[82,R,R,R,0,0,0,0]], kind='verse'),
   'drop': sec(8, ['Gm', 'Eb', 'Bb', 'F'], keys=['brasshits', 'pad'], drums='glitch', bass='funky', lead='saw80s',
               mel=[[91,R,91,0,89,R,86,R],[87,R,R,86,R,82,0,0],[91,R,91,0,89,R,94,R],[93,R,R,R,0,0,0,0]], extra=hit, impact=True, kind='chorus'),
   'end': sec(1, ['Gm'], extra=stutter_out('saw80s', [79, 82, 86]), fill=False, kind='outro')},
   order=['intro', 'verse', 'drop', 'verse', 'drop', 'end'], targets=EVEN, ride=1.),
 # melodic progressive house: grows from a lone piano arp, one long build, an emotional drop, fades back to the piano
 'silk': dict(file='Silk_Rotation', title='Silk Rotation', bpm=122, chorus_keys=True, cont_tol=0., sections={
   'piano': sec(8, ['C#m', 'A', 'E', 'B'], keys=['pianoriff'], kind='verse'),
   'groove': sec(8, ['C#m', 'A', 'E', 'B'], keys=['pianoriff', 'pad'], drums='house', bass='octave', lead='piano',
                 mel=[[76,R,R,73,R,R,76,R],[78,R,R,R,76,R,R,R],[76,R,R,73,R,R,80,R],[78,R,R,R,0,0,0,0]], kind='verse'),
   'build': sec(8, ['A', 'B', 'C#m', 'C#m'], keys=['pianoriff', 'pad'], drums='halfpop', lead='piano', mel=[[76,R,R,73,R,R,76,R],[78,R,R,R,76,R,R,R],[76,R,R,73,R,R,80,R],[78,R,R,R,0,0,0,0]], extra=roll, kind='verse'),
   'drop': sec(16, ['C#m', 'A', 'E', 'B'], keys=['pianoriff', 'stabs'], drums='house', bass='octave', lead='saw80s',
               mel=[[88,R,R,85,R,R,88,R],[90,R,R,R,88,R,R,R],[88,R,R,85,R,R,92,R],[90,R,R,R,0,0,0,0]], extra=hit, impact=True, kind='chorus'),
   'outro': sec(8, ['C#m', 'A', 'E', 'B'], keys=['pianoriff'], kind='outro')},
   order=['piano', 'groove', 'build', 'drop', 'outro'], fadeout=12., targets=EVEN, ride=1.),
}
if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names: build(SONGS[k])
