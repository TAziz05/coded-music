import sys, subprocess, numpy as np
from scipy.io import wavfile
from engine import *

def render(M, name, sends, levels, duck=('pad', 'bass', 'arp'), fade=6.):
    out = master(M, sends, levels, set(duck), fade_out=fade)
    wav = f'{name}.wav'; wavfile.write(wav, SR, (out.T * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-b:a', '320k', f'{name}.mp3'], check=True)
    print(name, round(out.shape[1] / SR, 1), 's')

def sections_to_bars(secs):
    out = []
    for name, n in secs: out += [(name, i, n) for i in range(n)]
    return out

# =====================================================================
# 1) VICTORY RUSH — 128 BPM, heroic & upbeat (C major: F–G–Em–Am)
# =====================================================================
def victory_rush():
    bpm = 128; st = 60 / bpm / 4; B = 16 * st
    prog = [([53, 57, 60], 41), ([55, 59, 62], 43), ([52, 55, 59], 40), ([57, 60, 64], 45)]
    lead = melody([[72,0,72,74,76,0,74,72],[74,0,74,76,79,0,76,74],[76,0,79,0,83,81,79,76],[81,-1,-1,79,76,-1,74,76],
                   [72,0,72,74,76,0,77,76],[74,0,79,0,79,81,83,-1],[84,-1,83,79,76,-1,79,83],[81,-1,-1,-1,-1,0,0,0]])
    secs = [('intro', 8), ('verse', 16), ('build', 4), ('chorus', 16), ('break', 8), ('build', 4), ('chorus', 16), ('outro', 8)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = prog[b % 4]
        full = sec in ('verse', 'chorus') or (sec == 'outro' and i < 4)
        # pad
        if sec != 'build' or i < 3:
            pv = .5 if sec == 'intro' else .55 if sec == 'break' else .45
            for nn in [root + 12] + [c + 12 for c in ch]:
                supersaw(M, 'pad', t0, nn, B, pv * .35, cut=1400 if sec == 'intro' else 2000, a=.25 if sec in ('intro', 'break') else .05, r=.4)
        # drums
        if full:
            for k in range(4): kick(M, t0 + k * 4 * st)
            clap(M, t0 + 4 * st, .8); clap(M, t0 + 12 * st, .8)
            for k in range(16):
                if k % 4 == 2: hat(M, t0 + k * st, .55, open_=True)
                else: hat(M, t0 + k * st, .22 + .1 * (k % 2 == 0))
            if i == n - 1 and sec == 'verse':
                for k, nn in enumerate([50, 50, 45, 45, 41, 41, 38, 38]): tom(M, t0 + (8 + k) * st, nn, .6, pan=.3 - k * .08)
        if sec == 'intro':
            for k in range(8): hat(M, t0 + (2 * k + 1) * st, .2)
            if i >= 4:
                tones = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24]
                for k in range(16): pluck(M, 'arp', t0 + k * st, tones[[0, 1, 2, 3, 2, 1, 0, 2][k % 8]], st, .12 * (i - 3) / 4, pan=(-.4, .4)[k % 2])
            if i == n - 1: riser(M, t0, B, .5)
        if sec == 'build':
            k = 2 if i < 2 else 1 if i < 3 else .5
            for s in np.arange(0, 16, [4, 2, 1, .5][i]):
                snare(M, t0 + s * st, .25 + .5 * ((b % 4) * 16 + s) / 64)
            if i == 0: riser(M, t0, 4 * B, .7)
            if i < 3:
                for kk in range(4): kick(M, t0 + kk * 4 * st, .7)
        # bass
        if full or (sec == 'build' and i < 3):
            for k in range(8):
                nn = root if k % 2 else root - 12
                bass(M, 'bass', t0 + (2 * k + (1 if k % 2 else 0)) * st, nn + (12 if k % 2 else 12), st * 1.6, .55 if k % 2 else .45, cut=900 if sec != 'chorus' else 1400)
        # arp
        if sec in ('verse', 'chorus', 'build') or (sec == 'outro' and i < 4):
            tones = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24]
            pat = [0, 1, 2, 3, 2, 1, 2, 3, 0, 1, 2, 3, 3, 2, 1, 2]
            for k in range(16): pluck(M, 'arp', t0 + k * st, tones[pat[k]], st * .9, .13 if sec != 'chorus' else .09, pan=(-.35, .35)[k % 2])
        # chorus lead + stabs
        if sec == 'chorus':
            if i % 8 == 0 and i == 0: crash(M, t0, .8); impact(M, t0, .6)
            if i == 8: crash(M, t0, .55)
            bi = i % 8
            for (s8, nn, L) in lead:
                if s8 // 8 == bi:
                    tt = t0 + (s8 % 8) * 2 * st; dur = L * 2 * st * .92
                    brass(M, 'lead', tt, nn, dur, .5, pan=-.1); brass(M, 'lead', tt, nn - 12, dur, .28, pan=.15)
            for s in (0, 6, 10):
                for c in ch: brass(M, 'stab', t0 + s * st, c, st * 1.4, .16, pan=(c % 3 - 1) * .4)
        if sec == 'break':
            if i == 0: crash(M, t0, .5)
            bi = i % 8
            for (s8, nn, L) in lead:
                if s8 // 8 == bi: pluck(M, 'keys', t0 + (s8 % 8) * 2 * st, nn, L * 2 * st, .2, dec=.2, cut=4000)
            if i >= 4: kick(M, t0, .6); kick(M, t0 + 8 * st, .5)
        if sec == 'outro' and i == 4: crash(M, t0, .5)
    M.buses['keys_d'] = pingpong(M.buses.get('keys', np.zeros((2, M.n))), 3 * st, .45)
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .3)
    render(M, 'Victory_Rush_128bpm',
           sends={'pad': .25, 'lead': .3, 'stab': .3, 'arp': .2, 'keys': .4, 'drums': .06, 'fx': .3},
           levels={'pad': .7, 'bass': .9, 'arp': .8, 'lead': 1., 'lead_d': .35, 'stab': .7, 'keys': .9, 'keys_d': .5, 'drums': 1., 'fx': .8})

# =====================================================================
# 2) STORM CLOSING — 140 BPM, tense & driving (A minor)
# =====================================================================
def storm_closing():
    bpm = 140; st = 60 / bpm / 4; B = 16 * st
    vprog = [([57, 60, 64], 45), ([53, 57, 60], 41), ([55, 60, 64], 48), ([55, 59, 62], 43)]
    cprog = [([57, 60, 64], 45), ([53, 57, 60], 41), ([55, 59, 62], 43), ([56, 59, 64], 40)]
    lead = melody([[69,72,76,-1,74,72,71,72],[72,-1,69,-1,65,-1,69,72],[74,-1,71,-1,67,71,74,76],[76,-1,-1,-1,74,-1,71,-1],
                   [69,72,76,-1,74,72,71,72],[77,-1,76,-1,72,-1,69,72],[74,-1,76,-1,79,-1,74,-1],[76,-1,80,-1,83,-1,-1,-1]])
    secs = [('intro', 8), ('verse', 16), ('build', 4), ('chorus', 16), ('break', 8), ('build', 4), ('chorus', 16), ('outro', 8)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = (cprog if sec == 'chorus' else vprog)[b % 4]
        drums = sec in ('verse', 'chorus') or (sec == 'outro' and i < 4)
        # ticking clock hats everywhere but the end
        if sec != 'outro' or i < 6:
            for k in range(16): hat(M, t0 + k * st, (.3 if k % 4 == 2 else .14) * (.6 if sec in ('intro', 'break') else 1), pan=(.3, -.2)[k % 2])
        # arp (minor 16ths)
        if sec != 'outro' or i < 6:
            tones = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24, ch[1] + 24]
            pat = [0, 2, 3, 2, 1, 2, 4, 2, 0, 2, 3, 2, 1, 3, 4, 3]
            av = .11 if sec != 'intro' else .06 + .07 * i / 8
            for k in range(16): pluck(M, 'arp', t0 + k * st, tones[pat[k]], st * .8, av, pan=(-.45, .45)[k % 2], dec=.06)
        # driving octave bass
        if sec in ('verse', 'chorus', 'build') or (sec == 'intro' and i >= 4) or (sec == 'outro' and i < 4):
            for k in range(16 if sec == 'chorus' else 8):
                step = k if sec == 'chorus' else 2 * k
                nn = root - 12 + (12 if (step // 2) % 2 else 0) if sec != 'chorus' else root - 12 + (12 if k % 2 else 0)
                bass(M, 'bass', t0 + step * st, nn, st * (.9 if sec == 'chorus' else 1.7), .5, cut=1300 if sec == 'chorus' else 800, growl=.3)
        if sec == 'break':
            supersaw(M, 'bass', t0, root - 12, B, .4, cut=500, a=.05, r=.2, voices=3)
            for k, nn in enumerate([45, 45, 43, 41] if i % 2 else [45, 0, 45, 0]):
                if nn: tom(M, t0 + k * 4 * st, nn, .7)
        # pad
        for nn in [c + 12 for c in ch]:
            supersaw(M, 'pad', t0, nn, B, .14 if sec != 'chorus' else .11, cut=1600, a=.1, r=.3)
        # drums
        if drums:
            if sec == 'chorus':
                for k in range(4): kick(M, t0 + k * 4 * st, 1., punch=1.2)
            else:
                for s in (0, 7, 10): kick(M, t0 + s * st, .95)
            snare(M, t0 + 4 * st, .75); snare(M, t0 + 12 * st, .75); clap(M, t0 + 12 * st, .4)
            if i == n - 1:
                for k, nn in enumerate([52, 50, 47, 45, 43, 40]): tom(M, t0 + (10 + k) * st, nn, .7, pan=.4 - k * .16)
        # stabs (verse): syncopated brass hits
        if sec == 'verse' and i % 2 == 1:
            for s in (0, 3, 6):
                for c in ch: brass(M, 'stab', t0 + s * st, c, st * 1.2, .2)
        if sec == 'build':
            if i == 0: riser(M, t0, 4 * B, .75)
            dens = [4, 2, 1, .5][i]
            for s in np.arange(0, 16, dens): snare(M, t0 + s * st, .25 + .14 * i + .02 * s)
        if sec == 'chorus':
            if i in (0, 8): crash(M, t0, .8 if i == 0 else .55)
            if i == 0: impact(M, t0, .7)
            for (s8, nn, L) in lead:
                if s8 // 8 == i % 8:
                    tt = t0 + (s8 % 8) * 2 * st; dur = L * 2 * st * .9
                    brass(M, 'lead', tt, nn, dur, .5, pan=-.08); brass(M, 'lead', tt, nn - 12, dur, .3, pan=.12)
            for s in (0, 8):
                for c in ch: brass(M, 'stab', t0 + s * st, c - 12, st * 2.5, .14)
        if sec == 'intro' and i == n - 1: riser(M, t0, B, .5)
        if sec == 'break' and i == 0: crash(M, t0, .5); impact(M, t0, .5)
        if sec == 'outro' and i == 4: crash(M, t0, .55)
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .3)
    render(M, 'Storm_Closing_140bpm',
           sends={'pad': .3, 'lead': .3, 'stab': .3, 'arp': .22, 'drums': .07, 'fx': .3},
           levels={'pad': .7, 'bass': .85, 'arp': .85, 'lead': 1., 'lead_d': .3, 'stab': .75, 'drums': 1., 'fx': .8})

# =====================================================================
# 3) LOBBY LOOP — 102 BPM, chill but polished (Fmaj7–Em7–Dm7–Cmaj7)
# =====================================================================
def lobby_loop():
    bpm = 102; st = 60 / bpm / 4; B = 16 * st; sw = .16 * st
    prog = [([53, 57, 60, 64], 41), ([52, 55, 59, 62], 40), ([50, 53, 57, 60], 38), ([48, 52, 55, 59], 36)]
    melA = melody([[72,0,69,72,76,-1,74,72],[71,-1,67,-1,71,74,76,-1],[77,-1,76,74,72,-1,69,-1],[71,-1,72,-1,67,-1,-1,0],
                   [72,0,69,72,76,-1,79,77],[76,-1,74,-1,71,74,-1,76],[74,-1,72,69,72,-1,74,-1],[72,-1,-1,-1,0,0,0,0]])
    melB = melody([[81,-1,79,-1,76,-1,72,-1],[79,-1,76,-1,74,-1,71,-1],[77,-1,76,-1,74,72,69,-1],[71,-1,72,74,76,-1,-1,-1],
                   [81,-1,79,-1,76,77,79,-1],[79,-1,76,-1,74,76,79,-1],[77,-1,74,-1,72,-1,74,76],[76,-1,-1,-1,0,0,0,0]])
    secs = [('intro', 4), ('A', 16), ('B', 16), ('A', 16), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    S = lambda k: k * st + (sw if k % 2 else 0)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = prog[b % 4]
        # electric piano comping
        rh = [(0, 3), (3, 2), (6, 4), (10, 2), (12, 3)] if sec != 'intro' else [(0, 7), (8, 7)]
        for s, L in rh:
            for j, c in enumerate(ch): epiano(M, 'keys', t0 + S(s) + j * .006, c + 12, L * st, .09, pan=(j - 1.5) * .25)
        if sec == 'B':
            for c in ch: supersaw(M, 'pad', t0, c + 12, B, .09, cut=1500, a=.3, r=.6, voices=3)
        drums = sec in ('A', 'B')
        if drums:
            for s in (0, 7, 10): kick(M, t0 + S(s), .8, punch=.8)
            clap(M, t0 + S(4), .6); clap(M, t0 + S(12), .6); snare(M, t0 + S(12), .25)
            for k in range(16):
                if k % 2 == 0: hat(M, t0 + S(k), .25 if k % 4 else .18)
                shaker(M, t0 + S(k), .6 if k % 2 else .35)
            if i == n - 1: hat(M, t0 + S(14), .4, open_=True)
            if i == 0: crash(M, t0, .35)
        if sec != 'intro' and (sec != 'outro'):
            for s, nn, L in [(0, root, 3), (3, root, 1), (6, root + 7, 2), (8, root + 12, 2), (10, root + 10, 2), (14, root + 7, 2)]:
                bass(M, 'bass', t0 + S(s), nn, L * st * .85, .55, cut=700, growl=-1)
        if sec == 'outro': bass(M, 'bass', t0, root, B * .9, .45, cut=500, growl=-1)
        mel = melA if sec == 'A' else melB if sec == 'B' else None
        if mel and (sec == 'B' or i >= 0):
            for (s8, nn, L) in mel:
                if s8 // 8 == i % 8:
                    leadsq(M, 'lead', t0 + S((s8 % 8) * 2), nn, L * 2 * st * .9, .38, pan=.1)
                    if sec == 'B': pluck(M, 'lead', t0 + S((s8 % 8) * 2), nn + 12, L * 2 * st * .5, .07, pan=-.3, dec=.15)
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .38)
    render(M, 'Lobby_Loop_102bpm',
           sends={'keys': .3, 'lead': .3, 'pad': .4, 'drums': .05, 'fx': .3},
           levels={'keys': 1., 'lead': .9, 'lead_d': .35, 'pad': .7, 'bass': .95, 'drums': .9, 'fx': .7},
           duck=('pad',), fade=5.)

# =====================================================================
# 4) OVERCLOCKED — 174 BPM drum & bass (F minor: F–Db–Ab–Eb)
# =====================================================================
def reese(M, t, n, dur, vol, lfo_rate=.35, bright=1.):
    """Classic DnB 'reese': detuned saws through a slowly moving filter, plus a clean sine sub."""
    N = int((dur + .05) * SR); tt = tarr(N); f = mtof(n)
    x = saw(f * 2 ** (-.14 / 12), N) + saw(f * 2 ** (.14 / 12), N) + .5 * saw(f * 2 ** (.05 / 12), N)
    lo = lp(lp(x, 260), 260); hi = lp(lp(x, 1400 * bright), 1400 * bright)
    m = .5 + .5 * np.sin(2 * np.pi * lfo_rate * (tt + t))
    y = np.tanh((lo + (hi - lo) * m) * 1.4) * .6
    e = env(dur, .01, .3, .9, .05)[:N]
    M.add('reese', t, y[:len(e)] * e * vol * .9, y[:len(e)] * e * vol * .9)
    se = env(dur, .005, .3, .95, .04)[:N]; sub = sine(f / 2, len(se)) * se
    M.add('sub', t, sub * vol)

def dnb():
    bpm = 174; st = 60 / bpm / 4; B = 16 * st
    roots = [41, 37, 44, 39]                    # F2, Db2, Ab2, Eb2
    pads = [[65, 68, 72], [61, 65, 68], [60, 63, 68], [63, 67, 70]]
    secs = [('intro', 8), ('build', 4), ('drop', 32), ('break', 8), ('build', 4), ('drop2', 32), ('outro', 8)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    def beat(t0, i, v=1., ghosts=True):
        kick(M, t0, v, punch=1.1); kick(M, t0 + 10 * st, v * .9, punch=1.1)
        snare(M, t0 + 4 * st, v * .85); snare(M, t0 + 12 * st, v * .85); clap(M, t0 + 12 * st, v * .25)
        if ghosts:
            for s, g in ((7, .18), (9, .12), (15, .2)): snare(M, t0 + s * st, v * g, pan=.2)
        for k in range(0, 16, 2): hat(M, t0 + k * st, v * (.32 if k % 4 == 2 else .2), pan=.3)
        for k in range(16): shaker(M, t0 + k * st, v * (.5 if k % 2 else .25))
        if i % 4 == 3:  # fill
            for s, nn in zip(range(12, 16), (55, 52, 48, 45)): tom(M, t0 + s * st, nn, v * .55, pan=.3 - (s - 12) * .2)
            snare(M, t0 + 14 * st, v * .5); snare(M, t0 + 15 * st, v * .6)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; root = roots[b % 4]; pd = pads[b % 4]
        # pad (sits far back)
        if sec in ('intro', 'break', 'drop', 'drop2', 'outro'):
            for nn in pd: supersaw(M, 'pad', t0, nn, B, .06 if sec.startswith('drop') else .1, cut=1300, a=.4, r=.8, voices=3)
        if sec == 'intro':
            for k in range(0, 16, 2): hat(M, t0 + k * st, .12 + .02 * i)
            if i >= 4: snare(M, t0 + 12 * st, .3); kick(M, t0, .5)
            if i == n - 1: riser(M, t0, B, .5)
        if sec == 'build':
            if i == 0: riser(M, t0, 4 * B, .8)
            for s in np.arange(0, 16, [4, 2, 1, .5][i]): snare(M, t0 + s * st, .25 + .14 * i + .015 * s)
            sine_len = B * .95; M.add('sub', t0, sine(mtof(root) / 2, int(sine_len * SR)) * env(sine_len, .01, .3, .9, .05)[:int(sine_len * SR)] * .4 * (i + 1) / 4)
        if sec in ('drop', 'drop2'):
            if i == 0: crash(M, t0, .9); impact(M, t0, .8)
            if i == 16: crash(M, t0, .6)
            beat(t0, i)
            # rolling reese bassline: long note, pickup, octave stab
            for s, L, o in ((0, 6, 0), (6, 2, 0), (8, 3, 12), (11, 1, 0), (12, 4, 0)):
                reese(M, t0 + s * st, root + o, L * st * .95, .55 if o == 0 else .4, bright=1.3 if sec == 'drop2' else 1.)
            if sec == 'drop2' and i % 2 == 1:   # little stabs on top for the second drop
                for s in (3, 6, 14): pluck(M, 'arp', t0 + s * st, pd[(s // 3) % 3] + 12, st * 1.5, .12, pan=(s % 2) * .6 - .3, dec=.08)
        if sec == 'break':
            if i == 0: crash(M, t0, .5)
            M.add('sub', t0, sine(mtof(root) / 2, int(B * SR)) * env(B * .97, .05, .3, .9, .1)[:int(B * SR)] * .45)
            for k in range(0, 16, 2): hat(M, t0 + k * st, .15)
            if i >= 4: kick(M, t0, .55); snare(M, t0 + 12 * st, .35)
            for k, nn in enumerate((0, 3, 7, 12)): pluck(M, 'arp', t0 + k * 4 * st, pd[0] + nn - 12, st * 3, .14, dec=.25, cut=3000)
        if sec == 'outro':
            if i < 4: beat(t0, i, .7, ghosts=False)
            M.add('sub', t0, sine(mtof(root) / 2, int(B * SR)) * env(B * .97, .02, .3, .9, .1)[:int(B * SR)] * .4)
            if i == 4: crash(M, t0, .5)
    M.buses['arp_d'] = pingpong(M.buses['arp'], 3 * st, .4)
    render(M, 'Overclocked_174bpm',
           sends={'pad': .45, 'arp': .35, 'drums': .05, 'fx': .3},
           levels={'pad': .7, 'reese': .8, 'sub': 1., 'arp': .8, 'arp_d': .4, 'drums': 1.1, 'fx': .8},
           duck=('pad', 'reese'))

# =====================================================================
# 5) NOBODY'S LOOKING — 180 BPM breakcore (D minor: Bbmaj7–Am7–Dm9–Gm7)
#    Sad piano over a chopped, stuttering, code-built breakbeat.
# =====================================================================
def piano(M, bus, t, n, dur, vol, pan=0.):
    """Additive piano: slightly stretched partials that die away faster the higher they are, plus a hammer thump."""
    f = mtof(n); L = min(dur, 3.5) + .4; N = int(L * SR); tt = tarr(N)
    x = np.zeros(N); bright = np.clip(1.4 - (n - 48) / 60, .5, 1.4)
    for k in range(1, 13):
        fk = f * k * np.sqrt(1 + .00035 * k * k)
        if fk > 16000: break
        tau = (3.2 / (1 + .55 * k)) * (1.6 - (n - 40) / 70)
        a = (1 / k ** 1.25) * (bright if k > 3 else 1)
        x += a * np.sin(2 * np.pi * fk * tt + rng.random() * 6) * np.exp(-tt / max(tau, .08))
        x += .3 * a * np.sin(2 * np.pi * fk * 1.0015 * tt) * np.exp(-tt / max(tau, .08))
    x += lp(noise(N), 1800) * np.exp(-tt / .012) * .25
    damp = np.where(tt < dur, 1., np.exp(-(tt - dur) / .12))
    x = lp(x * damp * np.clip(tt / .002, 0, 1), 7000)
    M.add(bus, t, x * vol * .35, pan=pan)

def ride(M, t, vol=1., bus='drums'):
    N = int(.5 * SR); tt = tarr(N); x = np.zeros(N)
    for fr in (3150, 4270, 5340, 6800, 8020, 9930):
        x += np.sign(np.sin(2 * np.pi * fr * tt + rng.random() * 6))
    x = hp(x, 6000) * np.exp(-tt / .18) * .08 + hp(noise(N), 9000) * np.exp(-tt / .05) * .3
    M.add(bus, t, x * vol, pan=-.25)

def make_break(st):
    """Two bars of an 'amen-style' breakbeat built from code drums, returned as stereo 16th-note slices."""
    BM = Mix(32 * st)
    hits = {0: [0, 2, 10, 11], 1: [0, 2, 10]}; snr = {0: [4, 7, 9, 12, 15], 1: [4, 7, 9, 14]}
    for bar in (0, 1):
        o = bar * 16 * st
        for k in hits[bar]: kick(BM, o + k * st, 1., punch=1.2)
        for k in snr[bar]: snare(BM, o + k * st, .95 if k in (4, 12) else .6); clap(BM, o + k * st, .2)
        for k in range(0, 16, 2): ride(BM, o + k * st, .9 if k % 4 == 0 else .6)
        for k in (1, 3, 13): snare(BM, o + k * st, .15)
    x = BM.buses['drums']; x = np.tanh(x * 1.8) / 1.2
    n = int(st * SR); return [x[:, i * n:(i + 1) * n].copy() for i in range(32)], n

def slice_fx(sl, n, mode, arg=None):
    y = sl.copy()
    if mode == 'rev': y = y[:, ::-1]
    elif mode == 'roll':                    # repeat the first 1/arg of the slice
        k = n // arg; y = np.tile(y[:, :k], (1, arg))[:, :n]
    elif mode == 'pitch':                   # resample (arg > 1 = higher & shorter, < 1 = lower)
        idx = np.arange(0, sl.shape[1], arg); idx = idx[idx < sl.shape[1] - 1].astype(int)
        y = sl[:, idx]; y = np.pad(y, ((0, 0), (0, max(0, n - y.shape[1]))))[:, :n]
    f = min(60, n // 8); ramp = np.linspace(0, 1, f)
    y[:, :f] *= ramp; y[:, -f:] *= ramp[::-1]
    return y

def breakcore():
    bpm = 180; st = 60 / bpm / 4; B = 16 * st
    R = np.random.default_rng(1729)
    slices, n = make_break(st)
    chords = [[46, 53, 57, 62], [45, 52, 55, 60], [50, 53, 57, 64], [43, 53, 58, 62]]   # 2 bars each
    melody = [[(0, 69, 12), (12, 72, 4), (16, 74, 16)], [(0, 72, 8), (8, 69, 8), (16, 67, 16)],
              [(0, 65, 8), (8, 69, 8), (16, 76, 12), (28, 74, 4)], [(0, 74, 8), (8, 70, 8), (16, 69, 16)]]
    secs = [('intro', 8), ('build', 4), ('dropA', 32), ('break', 8), ('build', 4), ('dropB', 32), ('outro', 8)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    def put_slice(t, sl, gain=1.): M.add('break', t, sl[0] * gain, sl[1] * gain)
    for b, (sec, i, nb) in enumerate(bars):
        t0 = b * B; ci = (b // 2) % 4; ch = chords[ci]; half = b % 2
        # ---- piano: root + gently broken chord in quarter notes ----
        if sec != 'build' or i < 2:
            pv = 1. if sec in ('intro', 'break', 'outro') else .75
            if half == 0: piano(M, 'piano', t0, ch[0] - 12, 2 * B, .9 * pv, pan=-.2)
            order = [1, 2, 3, 2] if half == 0 else [1, 3, 2, 3]
            for q in range(4): piano(M, 'piano', t0 + q * 4 * st, ch[order[q]], 4 * st * 1.6, .5 * pv, pan=(order[q] - 2) * .25)
        if sec in ('break', 'dropB', 'outro') and half == 0:
            up = 12 if sec == 'dropB' else 0
            for s16, nn, L in melody[ci]:
                piano(M, 'piano', t0 + s16 * st, nn + up, L * st, .62, pan=.15)
        # vinyl dust on the quiet parts
        if sec in ('intro', 'break', 'outro'):
            N = int(B * SR); dust = np.zeros(N); pos = R.integers(0, N, 14); dust[pos] = R.uniform(-.6, .6, 14)
            M.add('fx', t0, lp(dust, 5000) * .25 + hp(noise(N), 3000) * .006)
        if sec == 'break' and half == 0:
            for nn in ch[1:]: supersaw(M, 'pad', t0, nn + 12, 2 * B, .05, cut=1100, a=.8, r=1., voices=3)
        # ---- breaks ----
        if sec == 'build':
            base = (i % 2) * 16
            for k in range(16):
                if i < 2 and k % 2: continue
                sl = slices[base + k]
                if i == 3 and k >= 8: sl = slice_fx(slices[4], n, 'roll', 2 if k < 12 else 4)
                put_slice(t0 + k * st, sl, .35 + .17 * i)
            if i == 0: riser(M, t0, 4 * B, .6)
        if sec in ('dropA', 'dropB'):
            if i == 0: crash(M, t0, .8); impact(M, t0, .7)
            p = .22 if sec == 'dropA' else .42
            k = 0
            while k < 16:
                idx = (b % 2) * 16 + k; sl = slices[idx]; mode = None
                r = R.random()
                if r < p:
                    m = R.choice(['swap', 'rev', 'stut', 'roll', 'pitch'], p=[.35, .15, .2, .2, .1])
                    if m == 'swap': sl = slices[R.choice([0, 2, 4, 7, 9, 12, 15, 26, 30])]
                    elif m == 'rev': sl = slice_fx(slices[R.integers(0, 32)], n, 'rev')
                    elif m == 'stut' and k > 0: sl = slice_fx(slices[idx - 1], n, None)
                    elif m == 'roll': sl = slice_fx(slices[R.choice([4, 12, 20])], n, 'roll', int(R.choice([2, 3, 4])))
                    elif m == 'pitch': sl = slice_fx(slices[idx], n, 'pitch', float(R.choice([1.5, 2.0])))
                put_slice(t0 + k * st, sl)
                k += 1
            if i % 8 == 7:  # end-of-phrase snare roll that speeds up and climbs
                for j, (k2, div, pt) in enumerate([(12, 2, 1.), (13, 3, 1.12), (14, 4, 1.26), (15, 6, 1.5)]):
                    put_slice(t0 + k2 * st, slice_fx(slice_fx(slices[12], n, 'pitch', pt), n, 'roll', div), .9)
            if sec == 'dropA' and i == nb - 1:   # "tape stop" on the last beat
                for j, k2 in enumerate(range(12, 16)): put_slice(t0 + k2 * st, slice_fx(slices[k2], n, 'pitch', .8 - .15 * j), .8)
            # distorted sub bass on the chord roots
            root = ch[0] - 12 if ch[0] - 12 >= 31 else ch[0]
            for s16, L in ((0, 6), (6, 2), (10, 6)):
                Nn = int(L * st * .97 * SR); e = env(L * st * .97, .004, .3, .9, .03)[:Nn]
                x = np.tanh(sine(mtof(root), len(e)) * (2.5 if sec == 'dropA' else 4.)) * e
                M.add('sub', t0 + s16 * st, lp(x, 900) * .5)
        if sec == 'outro' and i < 2:
            put_slice(t0, slices[0], .5)
    M.buses['piano'] = np.array([lp(c, 6500) for c in M.buses['piano']])
    render(M, "Nobodys_Looking_180bpm",
           sends={'piano': .35, 'pad': .5, 'break': .06, 'fx': .1},
           levels={'piano': 1., 'pad': .7, 'break': .95, 'sub': .9, 'fx': .8, 'drums': .9},
           duck=(), fade=4.)

if __name__ == '__main__':
    {'1': victory_rush, '2': storm_closing, '3': lobby_loop, '4': dnb, '5': breakcore}[sys.argv[1]]()
