"""More game-themed originals.
python songs4.py 13  -> Boundless Run   (Sonic Unleashed theme style, upbeat rock with clean guitars)
python songs4.py 14  -> Ringworld Vigil (Halo style: monk chant, then strings, guitars and drums)"""
import sys
from songs import sections_to_bars, ride, piano
from songs3 import render2, bars8, play, strings, stacc, timpani
from instruments2 import *

# ---------- rock instruments ----------
def cab(x, warm=False):
    x = hp(x, 90); x = lp(x, 3800 if warm else 5200, 4); return x + (.2 if warm else .4) * bp(x, 1800, 3200)

def dist_gtr(M, bus, t, notes, dur, vol, mute=False, pan=0., gain=9., warm=False):
    """Distorted guitar: plucked strings -> heavy saturation -> speaker 'cab'. mute = palm-muted chug."""
    L = int((dur + .25) * SR); y = np.zeros(L)
    for j, n in enumerate(notes):
        k = ks(mtof(n), dur, .35 if mute else .55, .985 if mute else .9985); o = int(j * .004 * SR)
        y[o:o + len(k)] += k[:L - o]
    y = cab(np.tanh(y * gain) * .5, warm)
    if mute: y *= np.exp(-tarr(L) / .09)
    M.add(bus, t, y * vol, pan=pan)

def power(root): return [root, root + 7, root + 12]

def clean_gtr(M, bus, t, notes, dur, vol, mute=False, pan=0.):
    """Clean electric guitar chord: plucked strings strummed a few ms apart, no distortion."""
    L = int((dur + .25) * SR); y = np.zeros(L)
    for j, n in enumerate(notes):
        k = ks(mtof(n), dur, .4 if mute else .6, .99 if mute else .998); o = int(j * .007 * SR)
        y[o:o + len(k)] += k[:L - o] * (1 - .05 * j)
    y = lp(hp(y, 90), 7500)
    if mute: y *= np.exp(-tarr(L) / .14)
    M.add(bus, t, y * vol, pan=pan)

def chord_shape(root, minor):
    return [root, root + 7, root + 12, root + (15 if minor else 16), root + 19]

def clean_lead(M, t, n, dur, vol, pan=0.):
    N = int((dur + .2) * SR); y = ks(mtof(n), dur + .05, .7, .9995)[:N]
    tt = tarr(len(y)); vib = 1 + .004 * np.clip((tt - .25) / .2, 0, 1) * np.sin(2 * np.pi * 5.5 * tt)
    idx = np.clip(np.cumsum(vib), 0, len(y) - 1); y = np.interp(idx, np.arange(len(y)), y)
    M.add('lead', t, lp(hp(y, 150), 8000) * vol, pan=pan)

def lead_gtr(M, t, n, dur, vol, pan=0., gain=6., warm=False):
    N = int((dur + .2) * SR); y = ks(mtof(n), dur + .05, .6, .9993)[:N]
    tt = tarr(len(y)); vib = 1 + .004 * np.clip((tt - .25) / .2, 0, 1) * np.sin(2 * np.pi * 5.5 * tt)
    idx = np.clip(np.cumsum(vib), 0, len(y) - 1); y = np.interp(idx, np.arange(len(y)), y)
    y = cab(np.tanh(y * gain) * .5, warm); M.add('lead', t, y * vol, pan=pan)

def monk(M, t, n, dur, vol, pan=0.):
    """Male choir voice singing 'oh': a few slightly detuned saws through vowel formants, slow swell."""
    N = int((dur + .6) * SR); tt = tarr(N); x = np.zeros(N)
    for d in (-.1, -.03, .04, .11):
        vib = .08 * np.sin(2 * np.pi * (4.6 + rng.random()) * tt + rng.random() * 6)
        x += saw(mtof(n + d + vib), N)
    y = .5 * lp(x, 600) + 1.4 * bp(x, 400, 620) + .9 * bp(x, 750, 1000) + .25 * bp(x, 2300, 2900)
    e = np.clip(tt / .35, 0, 1) * np.where(tt < dur, 1., np.exp(-(tt - dur) / .25))
    M.add('choir', t, y * e * vol * .12, pan=pan)

# =====================================================================
# 13) BOUNDLESS RUN — 155 BPM, E major upbeat rock with clean guitars (Sonic style)
# =====================================================================
def boundless_run(tone='crunch'):
    bpm = 155; st = 60 / bpm / 4; B = 16 * st
    V = [('E', 40), ('B', 47), ('C#m', 37), ('A', 45)]; PRE = [('A', 45), ('B', 47), ('C#m', 37), ('B', 47)]
    CH = [('E', 40), ('B', 47), ('C#m', 37), ('A', 45), ('E', 40), ('B', 47), ('A', 45), ('B', 47)]
    BR = [('C#m', 37), ('A', 45), ('E', 40), ('B', 47)]
    vm = bars8([[68,-1,68,71,-1,68,66,64],[66,-1,-1,63,-1,-1,0,0],[64,-1,64,68,-1,71,-1,68],[69,-1,68,66,-1,-1,0,0]])
    pm = bars8([[69,-1,71,-1,73,-1,71,-1],[71,-1,73,-1,75,-1,-1,-1],[76,-1,75,-1,73,-1,71,-1],[75,-1,-1,-1,-1,-1,-1,-1]])
    cm = bars8([[76,-1,-1,75,76,-1,78,-1],[78,-1,75,-1,71,-1,-1,0],[73,-1,76,-1,80,-1,78,76],[76,-1,-1,-1,73,-1,-1,0],
                [76,-1,-1,75,76,-1,80,-1],[78,-1,75,-1,78,-1,80,-1],[81,-1,-1,80,-1,78,-1,76],[78,-1,-1,-1,-1,-1,0,0]])
    secs = [('intro', 4), ('verse', 8), ('pre', 4), ('chorus', 8), ('verse', 8), ('pre', 4), ('chorus', 8), ('bridge', 8), ('chorus', 8), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B + 3)
    ch_count = 0
    G = clean_gtr if tone == 'clean' else (lambda *a, **k: dist_gtr(*a, gain=3.2, warm=True, **k))
    LD = clean_lead if tone == 'clean' else (lambda *a, **k: lead_gtr(*a, gain=2.8, warm=True, **k))
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B
        if sec == 'chorus' and i == 0: ch_count += 1
        key = 1 if (sec == 'chorus' and ch_count == 3) or sec == 'outro' else 0   # last chorus jumps up a key
        prog = {'verse': V, 'intro': V, 'pre': PRE, 'chorus': CH, 'bridge': BR, 'outro': CH}[sec]
        name, root = prog[i % len(prog)]; root += key; r2 = root if root < 44 else root - 12
        pc = chord_shape(r2 + 12, name.endswith('m')) if tone == 'clean' else power(r2 + 12)
        # guitars
        if sec in ('verse',):
            for k in range(8): G(M, 'gtrL', t0 + k * 2 * st, (pc[:3] if tone == 'clean' else pc[:2]), 2 * st * .9, .3, mute=True, pan=-.6)
            for k in range(8): G(M, 'gtrR', t0 + k * 2 * st + .006, (pc[:3] if tone == 'clean' else pc[:2]), 2 * st * .9, .3, mute=True, pan=.6)
        elif sec == 'bridge':
            if i % 2 == 0:
                G(M, 'gtrL', t0, pc, 2 * B * .95, .3, pan=-.6); G(M, 'gtrR', t0 + .008, pc, 2 * B * .95, .3, pan=.6)
        elif sec != 'outro' or i < n - 1:
            for s, L in ((0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)) if sec != 'intro' or i >= 2 else ((0, 8), (8, 8)):
                G(M, 'gtrL', t0 + s * st, pc, L * st * .92, .3, pan=-.6)
                G(M, 'gtrR', t0 + s * st + .007, pc, L * st * .92, .3, pan=.6)
        if sec == 'outro' and i == n - 1:
            G(M, 'gtrL', t0, (chord_shape(40 + key + 12, False) if tone == 'clean' else power(40 + key + 12)), 3., .34, pan=-.6); G(M, 'gtrR', t0 + .01, (chord_shape(40 + key + 12, False) if tone == 'clean' else power(40 + key + 12)), 3., .34, pan=.6)
            crash(M, t0, .8); kick(M, t0, 1.)
            continue
        # bass
        if sec != 'intro' or i >= 2:
            for k in range(8 if sec != 'bridge' else 2): fbass(M, t0 + k * (2 if sec != 'bridge' else 8) * st, r2, (2 if sec != 'bridge' else 8) * st * .9, .55)
        # drums
        if sec == 'intro' and i < 2:
            if i == 1:
                for s in range(8, 16): snare(M, t0 + s * st, .3 + .06 * (s - 8))
        elif sec == 'bridge':
            kick(M, t0, .8); snare(M, t0 + 8 * st, .7)
            for k in range(0, 16, 4): ride(M, t0 + k * st, .5)
            if i == n - 1:
                for s in range(0, 16): snare(M, t0 + s * st, .25 + .04 * s)
        else:
            punk = sec in ('chorus', 'pre')
            for s in ((0, 6, 8, 10) if punk else (0, 8, 10)): kick(M, t0 + s * st, .9)
            for s in (4, 12): snare(M, t0 + s * st, .85)
            for k in range(8):
                if punk: ride(M, t0 + k * 2 * st, .55) if sec == 'pre' else hat(M, t0 + k * 2 * st, .45, open_=True)
                else: hat(M, t0 + k * 2 * st, .3)
            if i == 0 and sec in ('chorus', 'verse'): crash(M, t0, .7)
            if i == n - 1:
                for s, nn in zip(range(10, 16), (52, 52, 48, 48, 43, 43)): tom(M, t0 + s * st, nn, .6, pan=.3 - (s - 10) * .12)
        # lead melody (the 'vocal' line, played on lead guitar)
        mel = {'verse': vm, 'pre': pm, 'chorus': cm}.get(sec)
        if mel: play(mel, i, t0, st, lambda t, nn, d: LD(M, t, nn + key, d * .95, .42, pan=.1))
        if sec == 'chorus':
            play(mel, i, t0, st, lambda t, nn, d: LD(M, t, nn + key - 12, d * .95, .2, pan=-.15))
        if sec == 'bridge' and i % 2 == 0:
            LD(M, t0, [80, 81, 83, 82][i // 2 % 4] - 1 + key, 2 * B * .9, .38)
    if tone == 'clean': M.buses['gtrL'] = chorus(M.buses['gtrL'], mix=.3); M.buses['gtrR'] = chorus(M.buses['gtrR'], mix=.3)
    lv = {'gtrL': 1.9, 'gtrR': 1.9, 'lead': 3.2, 'lead_d': .7, 'bass': .8, 'drums': .7, 'fx': .6} if tone == 'clean' else \
         {'gtrL': 2.2, 'gtrR': 2.2, 'lead': 2.2, 'lead_d': .5, 'bass': .85, 'drums': .75, 'fx': .6}
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .25)
    render2(M, 'Boundless_Run_155bpm_' + tone, sends={'lead': .25, 'gtrL': .15, 'gtrR': .15, 'drums': .05, 'fx': .2},
            levels=lv, duck=(), fade=0.)

# =====================================================================
# 14) RINGWORLD VIGIL — monk chant at 72 BPM, then strings/guitars/drums at 120 BPM (Halo style)
# =====================================================================
def ringworld_vigil():
    chant = [[(62, 1), (62, 1), (65, 1), (67, 1)], [(69, 2), (67, 1), (69, 1)], [(72, 2), (69, 1), (67, 1)], [(69, 4)],
             [(69, 1), (72, 1), (74, 2)], [(72, 1), (71, 1), (69, 2)], [(67, 1), (65, 1), (64, 1), (65, 1)], [(62, 4)]]
    M = Mix(140); T = 0.
    # --- part 1: chant (72 BPM), 12 bars ---
    q = 60 / 72; Bc = 4 * q
    for bar in range(12):
        t0 = T + bar * Bc; ph = chant[bar % 8]
        x = 0.
        for nn, L in ph:
            monk(M, t0 + x * q, nn - 12, L * q * .97, 1.9)
            if bar >= 4: monk(M, t0 + x * q, nn - 17, L * q * .97, 1.2, pan=-.3)      # parallel fourth below (organum)
            if bar >= 8: monk(M, t0 + x * q, nn - 24, L * q * .97, 1., pan=.3)
            x += L
        strings(M, t0, 38, Bc, .12, att=1.)   # low D drone
        if bar >= 4: strings(M, t0, 50, Bc, .04, att=1.)
        if bar == 11: riser(M, t0, Bc, .5)
    T += 12 * Bc
    # --- part 2: driving section (120 BPM), 24 bars ---
    st = 60 / 120 / 4; B = 16 * st
    prog = [(38, [62, 65, 69]), (34, [58, 62, 65]), (36, [60, 64, 67]), (33, [57, 60, 64])]   # Dm Bb C Am
    theme = [[(0, 74, 4), (4, 74, 4), (8, 77, 4), (12, 79, 4)], [(0, 81, 8), (8, 79, 4), (12, 81, 4)],
             [(0, 84, 8), (8, 81, 4), (12, 79, 4)], [(0, 81, 16)]]
    crash(M, T, .8); impact(M, T, .7); timpani(M, T, 38, 1.)
    for bar in range(24):
        t0 = T + bar * B; root, ch = prog[bar % 4]
        climax = bar >= 16
        for k in range(16):   # string ostinato in 16ths: root, root, fifth, octave pattern
            nn = root + 24 + [0, 0, 7, 12, 0, 0, 7, 10, 0, 0, 7, 12, 0, 7, 12, 15][k]
            stacc(M, t0 + k * st, nn, st * .9, .11 if not climax else .13)
        for nn in ch: strings(M, t0, nn, B, .05 if not climax else .07)
        if bar >= 4:
            dist_gtr(M, 'gtrL', t0, power(root + 12), B * .48, .22, pan=-.6); dist_gtr(M, 'gtrR', t0 + .008, power(root + 12), B * .48, .22, pan=.6)
            dist_gtr(M, 'gtrL', t0 + 8 * st, power(root + 12), B * .48, .2, pan=-.6); dist_gtr(M, 'gtrR', t0 + 8 * st + .008, power(root + 12), B * .48, .2, pan=.6)
            fbass(M, t0, root, B * .48, .55); fbass(M, t0 + 8 * st, root, B * .48, .5)
            for s in (0, 3, 8, 10): kick(M, t0 + s * st, .85)
            for s in (4, 12): snare(M, t0 + s * st, .8)
            for k in range(0, 16, 2): ride(M, t0 + k * st, .45)
        else:
            timpani(M, t0, root + 12 if root < 40 else root, .7); timpani(M, t0 + 8 * st, root + 12 if root < 40 else root, .45)
        for s in (0, 6, 12): tom(M, t0 + s * st, 41, .45)
        if bar % 4 == 3:
            for s in range(10, 16): snare(M, t0 + s * st, .3 + .07 * (s - 10))
        if bar % 8 == 0 and bar >= 4: crash(M, t0, .55)
        if bar >= 8:   # brass theme (from the chant), choir doubles it at the climax
            for s, nn, L in theme[bar % 4]:
                brass(M, 'brass', t0 + s * st, nn - 12, L * st * .95, .45)
                brass(M, 'brass', t0 + s * st, nn - 24, L * st * .95, .3, pan=.2)
                if climax: monk(M, t0 + s * st, nn - 12, L * st * .95, .8)
    T += 24 * B
    # --- part 3: chant reprise, 4 bars, final chord ---
    timpani(M, T, 38, .9); crash(M, T, .5)
    for bar in range(4):
        t0 = T + bar * Bc; ph = chant[4 + bar]; x = 0.
        for nn, L in ph:
            monk(M, t0 + x * q, nn - 12, L * q * .97, 1.9); monk(M, t0 + x * q, nn - 17, L * q * .97, 1.2, pan=-.3)
            x += L
        strings(M, t0, 38, Bc * (2 if bar == 3 else 1), .07, att=.8)
    render2(M, 'Ringworld_Vigil', sends={'choir': .7, 'str': .45, 'brass': .4, 'gtrL': .1, 'gtrR': .1, 'drums': .15, 'fx': .4},
            levels={'choir': 1., 'str': .85, 'brass': .9, 'gtrL': .7, 'gtrR': .7, 'bass': .8, 'drums': .9, 'fx': .7}, duck=(), fade=3.)

if __name__ == '__main__':
    {'13': boundless_run, '13c': lambda: boundless_run('clean'), '14': ringworld_vigil}[sys.argv[1]]()
