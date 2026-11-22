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

if __name__ == '__main__':
    {'1': victory_rush, '2': storm_closing, '3': lobby_loop}[sys.argv[1]]()
