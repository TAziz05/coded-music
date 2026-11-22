"""Red 40 (sugar-rush hyperpop), Meet the Robinsons / Frutiger Aero, and a Bangladesh x Japan mix, each with a steady breakcore version.
python batch_d.py all  (or: red red_bc aero aero_bc bdjp bdjp_bc)"""
import sys
import numpy as np
import popkit
from popkit import build as pbuild, keys_bar, LEADS
from breakcore_engine import build as bbuild, chord, koto, shaku, taiko, gong
from seasons import AMEN, FUNK
from engine import *
from instruments2 import ks, envN, voice
from songs3 import glock
from southasia import bansuri, tabla_bar, harmonium, dotara, ektara, tanpura, KAHARBA, BOL

def sec(bars, chords, **kw): d = dict(bars=bars, chords=chords); d.update(kw); return d
def blocks(rows4):
    flat = [x for r in rows4 * 2 for x in r]; ev = []
    for i, x in enumerate(flat):
        if x > 0:
            L = 1
            while i + L < len(flat) and flat[i + L] == -1: L += 1
            ev.append((i * 2, x, L * 2))
    return [[(s - 32 * b, n, min(L, 32 * (b + 1) - s)) for s, n, L in ev if 32 * b <= s < 32 * (b + 1)] for b in range(4)]

# ---------------- sugar-rush sound effects ----------------
def boing(M, t, vol=1.):
    N = int(.35 * SR); tt = tarr(N); f = 200 * (1 + 1.5 * np.sin(np.pi * np.clip(tt / .3, 0, 1)) * np.exp(-tt / .2))
    M.add('fx', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .12) * vol * .4, pan=rng.uniform(-.5, .5))
def zap(M, t, vol=1.):
    N = int(.18 * SR); tt = tarr(N); f = 2400 * np.exp(-tt / .05) + 150
    M.add('fx', t, np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt / .06) * vol * .12, pan=rng.uniform(-.5, .5))
def sparkle(M, t, vol=1.):
    for j, n in enumerate([84, 88, 91, 96]): glock(M, t + j * .04, n, .25 * vol, pan=-.4 + j * .25)
def chop(M, t, n, dur, vol, up=12): voice(M, 'lead', t, n + up, min(dur, .25) * .9, .9 * vol)
LEADS['chop'] = lambda M, t, n, d, v: chop(M, t, n, d, v, 12)
LEADS['chipmunk'] = lambda M, t, n, d, v: chop(M, t, n, d, v, 19)
def hyper_fx(M, t0, st, S, i, n, tones, root):
    for s, f in ((3, zap), (11, boing)):
        if (i + s) % 3 == 0: f(M, t0 + S(s), .9)
    if i % 4 == 0: sparkle(M, t0, 1.)
def hyper_drums(M, t0, st, S, i, n, tones, root):
    for s in (0, 6, 10): kick(M, t0 + S(s), .95, punch=1.4)
    for s in (4, 12): snare(M, t0 + S(s), .85); clap(M, t0 + S(s), .7)
    for k in range(16): hat(M, t0 + S(k), .3 if k % 2 == 0 else .15)
    if i % 2 == 1:
        for j in range(8): snare(M, t0 + 14 * st + j * st / 4, .15 + .04 * j)
    hyper_fx(M, t0, st, S, i, n, tones, root)

# ---------------- Frutiger Aero: bubbles, water, glossy bells ----------------
def bubble(M, t, n, vol=1., pan=0.):   # pitched 'bloop' that slides up from a chord tone
    N = int(.12 * SR); tt = tarr(N); f = mtof(n) * (1 + 1.5 * tt / tt[-1])
    M.add('fx', t, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) * vol * .18, pan=pan)
def aero_fx(M, t0, st, S, i, n, tones, root):    # bubbles in a fixed rhythm: 'bloop-bloop' pairs on the offbeats, a rising run every 4th bar
    up = [c + 24 for c in tones[:3]]
    for s, j, p in ((2, 0, -.5), (3, 1, -.5), (10, 1, .5), (11, 2, .5)): bubble(M, t0 + S(s), up[j], .85, p)
    if i % 4 == 3:
        for k, s in enumerate((12, 13, 14, 15)): bubble(M, t0 + S(s), up[k % 3] + (12 if k == 3 else 0), .8, -.6 + .4 * k)
    if i % 2 == 0: glock(M, t0 + S(14), tones[-1] + 24, .25, pan=.4)

# ---------------- Bangladesh x Japan ----------------
def bdjp_keys(M, t0, st, tones, root, vol, bar):    # koto arpeggios + harmonium + ektara
    arp = tones + [tones[0] + 12, tones[1] + 12]
    for k in range(8): koto(M, t0 + k * 2 * st, arp[[0, 2, 4, 3, 1, 3, 4, 2][k] % len(arp)] + 12, 2 * st * 3, .7 * vol, pan=(-.35 if k % 2 else .35))
    harmonium(M, t0, tones[:3], 16 * st * .97, .6 * vol)
    for s in (0, 6, 8, 12): ektara(M, t0 + s * st, (.6 if s == 0 else .4) * vol)
TIHAI_BAR = 8 + 4 + 16 + 8 + 16 + 6      # the last two outro bars hold the tihai
def bdjp_keys_bc(M, t0, st, tones, root, vol, bar):
    if t0 < TIHAI_BAR * 16 * st - 1e-6: bdjp_keys(M, t0, st, tones, root, vol, bar)
def tihai_end(M, t_out, st, B, nb, ch):  # traditional ending: one phrase three times, the last stroke landing on the downbeat (sam)
    t0 = t_out + 6 * B; tones, r = ch[0]
    harmonium(M, t0, tones[:3], 2 * B, .7); tanp = Mix(2 * B + 6); tanpura(tanp, 2 * B + 3, .9, step=8 * st); M.add('drone', t0, tanp.buses['drone'][0], tanp.buses['drone'][1])
    phrase = [(0, 74, 'dha'), (2, 77, 'na'), (4, 79, 'na'), (6, 77, 'ti'), (8, 74, 'dha')]
    prev = None
    for k, s0 in enumerate((2, 13, 24)):
        for s, nn, bol in phrase:
            tt = t0 + (s0 + s) * st
            if s0 + s >= 32: continue
            bansuri(M, tt, nn, 2 * st * .95, 1., prev=prev); prev = nn; BOL[bol](M, tt, .85)
            koto(M, tt, nn - 12, 2 * st * 2, .5, pan=-.3)
        taiko(M, t0 + s0 * st, .6 + .1 * k)
    sam = t0 + 32 * st                    # sam: everyone lands together, softly, and rings out
    BOL['dha'](M, sam, .9); taiko(M, sam, .9); gong(M, sam, .55)
    harmonium(M, sam, tones[:3], 3., .6); bansuri(M, sam, 74, 3., .9, prev=prev); shaku(M, sam, 62, 3., .7)
    for nn in tones[:3]: koto(M, sam, nn + 12, 3., .4)
def bdjp_extra(M, sec, i, t0, st, tones, root):     # tabla kaharba with taiko on the downbeats
    if sec == 'outro' and i >= 6: return
    if sec in ('intro', 'half', 'outro'): tabla_bar(M, t0, st, .8, fill=(i % 4 == 3))
    elif sec in ('dropA', 'dropB'):
        for k, b in enumerate(KAHARBA):
            if k % 2 == 0: BOL[b](M, t0 + k * 2 * st, .5)
    if sec in ('build', 'dropA', 'dropB', 'half') and i % 2 == 0: taiko(M, t0, .8)
def callresp(M, t, n, dur, vol):                     # bansuri and shakuhachi trade phrases
    if int(t / 4) % 2 == 0: bansuri(M, t, n, dur * .96, 1.05 * vol)
    else: shaku(M, t, n, dur * .95, 1.1 * vol)
def bdjp_pop_keys(M, style, t0, st, S, tones, root, v):
    if style == 'bdjp': return bdjp_keys(M, t0, st, tones, root, v, 0)
    return _orig(M, style, t0, st, S, tones, root, v)
_orig = popkit.keys_bar; popkit.keys_bar = bdjp_pop_keys
LEADS['callresp'] = lambda M, t, n, d, v: callresp(M, t, n, d, v)
def bdjp_song_extra(M, t0, st, S, i, n, tones, root):
    tabla_bar(M, t0, st, .85, fill=(i % 4 == 3))
    if i % 2 == 0: taiko(M, t0, .7)

RED = [[84,-1,0,86,-1,0,88,-1],[86,-1,84,81,-1,0,79,-1],[81,-1,0,84,-1,0,86,88],[91,-1,-1,-1,0,0,0,0]]
AERO = [[76,-1,74,72,-1,74,-1,76],[79,-1,-1,76,-1,74,-1,-1],[72,-1,74,76,-1,79,-1,81],[79,-1,-1,-1,-1,-1,0,0]]
BDJP = [[74,-1,77,-1,79,-1,81,-1],[79,-1,77,74,-1,72,-1,-1],[74,-1,72,70,-1,69,-1,67],[69,-1,-1,-1,0,0,0,0]]

SONGS = {
 'red': ('pop', dict(file='Red_40_Sugar_Rush', title='Red 40 Sugar Rush', bpm=162, sections={
   'intro': sec(4, ['C', 'G', 'Am', 'F'], keys=['glitch'], lead='chipmunk', mel=RED, lv=.7, extra=hyper_fx, riser=True),
   'verse': sec(8, ['C', 'G', 'Am', 'F'], keys=['pluck', 'glitch'], bass='heavy808', lead='chop', extra=hyper_drums,
                mel=[[72,-1,0,72,74,-1,76,-1],[74,-1,0,71,-1,0,67,-1],[69,-1,0,72,-1,76,-1,79],[77,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['C', 'G', 'Am', 'F'], keys=['futurebass', 'glitch'], bass='heavy808', lead='chipmunk+synth', impact=True, extra=hyper_drums, mel=RED),
   'switch': sec(4, ['Am', 'F', 'C', 'G'], keys=['pad'], bass='heavy808', lead='chop', kind='bridge', extra=hyper_fx, riser=True,
                 mel=[[76,-1,-1,-1,72,-1,-1,-1],[77,-1,-1,-1,72,-1,-1,-1],[79,-1,-1,-1,76,-1,-1,-1],[79,-1,81,-1,83,-1,84,-1]]),
   'outro': sec(2, ['C', 'C'], keys=['glitch'], extra=hyper_fx, fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'switch', 'chorus', 'outro'], levels={'lead': 1.2, 'fx': 1.})),
 'red_bc': ('bc', dict(file='Red_40_Breaks', title='Red 40 Breaks', bpm=178, chords=['C', 'G', 'Am', 'F'],
   keys=lambda M, t0, st, tones, root, vol, bar: (keys_bar(M, 'glitch', t0, st, lambda k: k * st, tones, root, vol), hyper_fx(M, t0, st, lambda k: k * st, bar, 0, tones, root)),
   pad=.05, mel=lambda M, t, n, d, v: chop(M, t, n, d, v, 19), melB=lambda M, t, n, d, v: chop(M, t, n, d, v, 19), layerB='lead', bass='808',
   kit=dict(FUNK, crunch=2.6, clap=.5, punch=1.4), patA='P4', patB='P2', melody=blocks(RED), seed=211, levels={'fx': 1.})),
 'aero': ('pop', dict(file='Aqua_Tomorrow', title='Aqua Tomorrow', bpm=116, chorus_keys=True, sections={
   'intro': sec(4, ['C', 'G', 'Am', 'F'], keys=['pad', 'pluck'], lead='fmbell', mel=AERO, lv=.7, extra=aero_fx),
   'verse': sec(8, ['C', 'G', 'Am', 'F'], keys=['acoustic', 'piano'], drums='halfpop', bass='long', lead='voice', extra=aero_fx, kv=.8,
                mel=[[72,-1,72,74,-1,72,71,-1],[71,-1,-1,67,-1,69,71,-1],[72,-1,74,76,-1,77,-1,76],[74,-1,-1,-1,0,0,0,0]]),
   'chorus': sec(8, ['F', 'G', 'Em', 'Am', 'F', 'G', 'C', 'C'], keys=['acoustic', 'pad', 'pluck'], drums='rock', bass='octave', lead='synth+fmbell', impact=True, extra=aero_fx, mel=AERO),
   'outro': sec(4, ['C', 'G', 'F', 'C'], keys=['pad', 'pluck'], lead='fmbell', mel=[[76,-1,-1,-1,0,0,0,0],[74,-1,-1,-1,0,0,0,0],[72,-1,-1,-1,0,0,0,0],[72,-1,-1,-1,-1,-1,0,0]], extra=aero_fx, fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro'], levels={'fx': .9})),
 'aero_bc': ('bc', dict(file='Aqua_Tomorrow_Breaks', title='Aqua Tomorrow Breaks', bpm=172, chords=['C', 'G', 'Am', 'F'],
   keys=lambda M, t0, st, tones, root, vol, bar: (keys_bar(M, 'pluck', t0, st, lambda k: k * st, tones, root, vol), aero_fx(M, t0, st, lambda k: k * st, bar, 0, tones, root)),
   pad=.08, mel='glock', melB='lead', layerB='glock', bass='808', amb=[('rain', .25)], kit=dict(FUNK, crunch=1.3, clap=.35), patA='P0', patB='P3', melody=blocks(AERO), seed=221, levels={'fx': .9})),
 'bdjp': ('pop', dict(file='Padma_to_Kyoto', title='Padma to Kyoto', bpm=100, sections={
   'intro': sec(4, ['Dm', 'C', 'Bb', 'C'], keys=['bdjp'], lead='danso', mel=BDJP, lv=.8, gong=True),
   'verse': sec(8, ['Dm', 'C', 'Bb', 'C'], keys=['bdjp'], bass='finger', lead='callresp', extra=bdjp_song_extra, mel=BDJP),
   'chorus': sec(8, ['Bb', 'C', 'Dm', 'Dm'], keys=['bdjp', 'strings'], bass='finger', lead='callresp+gayageum', extra=bdjp_song_extra, impact=True,
                 mel=[[77,-1,79,-1,81,-1,84,-1],[81,-1,79,77,-1,74,-1,-1],[77,-1,74,72,-1,74,-1,77],[74,-1,-1,-1,-1,-1,0,0]]),
   'outro': sec(2, ['Dm', 'Dm'], keys=['bdjp'], gong=True, fill=False)},
   order=['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro'], levels={'lead': 1.1})),
 'bdjp_bc': ('bc', dict(file='Padma_to_Kyoto_Breaks', title='Padma to Kyoto Breaks', bpm=172, chords=['Dm', 'C', 'Bb', 'C'], keys=bdjp_keys_bc, pad=.04, mel=callresp, melB=callresp, layerB='koto', bass='sub', ending='custom', ending_fn=tihai_end,
   kit=dict(FUNK, crunch=1.4, clap=.25), patA='P1', patB='P3', extra=bdjp_extra, melody=blocks(BDJP), seed=231, verb=2.6, decay=.65, gong=True)),
}

if __name__ == '__main__':
    names = list(SONGS) if sys.argv[1] == 'all' else sys.argv[1:]
    for k in names:
        kind, cfg = SONGS[k]
        (pbuild if kind == 'pop' else bbuild)(cfg)
