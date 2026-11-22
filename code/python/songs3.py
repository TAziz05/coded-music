"""Game-themed songs: original melodies written in the *style* of each game's soundtrack and sound hardware.
python songs3.py 8   -> Determined Steps   (Undertale style: solo piano)
python songs3.py 9   -> Channel Plaza      (Wii menu style: bossa nova, e-piano, marimba)
python songs3.py 10  -> Frosty Podium      (Mario & Sonic Winter Games DS style: fanfare, sleigh bells, DS crunch)
python songs3.py 11  -> Coastal Route      (Pokemon Ruby/Sapphire style: GBA trumpet lead, 18 kHz crunch)
python songs3.py 12  -> Homebase Rising    (Fortnite Save the World style: orchestral adventure)"""
import sys, subprocess
from scipy.io import wavfile
from songs import sections_to_bars, ride, piano
from instruments2 import *

def bars8(rows): return melody(rows)
def play(mel, i, t0, st, fn, up=0):
    for s8, nn, L in mel:
        if s8 // 8 == i % 8: fn(t0 + (s8 % 8) * 2 * st, nn + up, L * 2 * st)

def render2(M, name, sends, levels, duck=(), fade=4., crush=None):
    from engine import master
    out = master(M, sends, levels, set(duck), fade_out=fade)
    if crush:  # sample-and-hold to an old console's mixing rate + fewer bits
        rate, bits = crush; step = SR / rate; idx = (np.floor(np.arange(out.shape[1]) / step) * step).astype(int)
        out = out[:, idx]; q = 2 ** (bits - 1); out = np.round(out * q) / q
        out = np.array([lp(c, min(rate * .48, 15000), 1) for c in out]); out = out / np.abs(out).max() * .89
    wavfile.write(f'{name}.wav', SR, (out.T * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{name}.wav', '-b:a', '320k', f'{name}.mp3'], check=True)
    print(name, round(out.shape[1] / SR, 1), 's')

# ---------- extra instruments ----------
def tri(f, n): t, _ = _ph(f, n); return 4 * np.abs(t - .5) - 1
def _ph(f, n):
    f = np.broadcast_to(np.asarray(f, float), (n,)); dt = f / SR; return (np.cumsum(dt) - dt) % 1, dt
def chip(M, bus, t, n, dur, vol, pw=.25, pan=0., vib=True):
    N = int((dur + .03) * SR); tt = tarr(N)
    v = (np.clip((tt - .15) / .15, 0, 1) * .2 * np.sin(2 * np.pi * 6 * tt)) if vib else 0
    x = sqr(mtof(n) * 2 ** (v / 12), N, pw); e = envN(N, dur, .003, .25, .75, .02)
    M.add(bus, t, x * e * vol * .3, pan=pan)
def tribass(M, t, n, dur, vol, bus='bass'):
    N = int((dur + .02) * SR); M.add(bus, t, tri(mtof(n), N) * envN(N, dur, .002, .1, .9, .015) * vol * .6)
def chipkick(M, t, vol=1.):
    N = int(.18 * SR); tt = tarr(N); f = 50 + 180 * np.exp(-tt / .02)
    M.add('drums', t, np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt / .06) * vol * .35); M.kicks.append(t)
def chipsnare(M, t, vol=1.):
    N = int(.16 * SR); tt = tarr(N); M.add('drums', t, noise(N) * np.exp(-tt / .05) * vol * .3)
def chiphat(M, t, vol=1.):
    N = int(.04 * SR); tt = tarr(N); M.add('drums', t, hp(noise(N), 6000) * np.exp(-tt / .01) * vol * .3, pan=.2)
def mallet(M, bus, t, n, dur, vol, ratio=4., dec=.6, pan=0., trem=0.):
    N = int((min(dur, 1.5) + .6) * SR); tt = tarr(N); f = mtof(n)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / dec) + .35 * np.sin(2 * np.pi * f * ratio * tt) * np.exp(-tt / (dec * .15))
    if trem: x *= 1 + trem * np.sin(2 * np.pi * 5.5 * tt)
    M.add(bus, t, x * np.clip(tt / .002, 0, 1) * vol * .4, pan=pan)
def glock(M, t, n, vol, pan=0.): mallet(M, 'glock', t, n, .5, vol, ratio=2.76, dec=.9, pan=pan)
def flute(M, bus, t, n, dur, vol, pan=0.):
    N = int((dur + .1) * SR); tt = tarr(N); v = np.clip((tt - .2) / .2, 0, 1) * .2 * np.sin(2 * np.pi * 5 * tt)
    f = mtof(n) * 2 ** (v / 12); x = sine(f, N) + .15 * sine(2 * f, N) + bp(noise(N), 1500, 6000) * .06
    M.add(bus, t, x * envN(N, dur, .05, .3, .85, .08) * vol * .35, pan=pan)
def rim(M, t, vol=1.):
    N = int(.06 * SR); tt = tarr(N)
    M.add('drums', t, (bp(noise(N), 1500, 5000) * .5 + np.sin(2 * np.pi * 820 * tt)) * np.exp(-tt / .012) * vol * .4, pan=-.2)
def sleigh(M, t, vol=1.):
    N = int(.25 * SR); tt = tarr(N); x = np.zeros(N)
    for o in rng.uniform(0, .03, 5):
        i = int(o * SR); x[i:] += bp(noise(N - i), 6000, 12000) * np.exp(-tarr(N - i) / .05)
    M.add('perc', t, x * vol * .25, pan=.35)
def timpani(M, t, n, vol=1.):
    N = int(1.6 * SR); tt = tarr(N); f = mtof(n) * (1 + .05 * np.exp(-tt / .05))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .6) + lp(noise(N), 600) * np.exp(-tt / .05) * .5
    M.add('drums', t, x * vol * .7)
def strings(M, t, n, dur, vol, att=.25, pan=0.):
    supersaw(M, 'str', t, n, dur, vol, cut=2200, a=att, d=.3, s=.9, r=.35, voices=5, detune=.12, width=.6)
def stacc(M, t, n, dur, vol, pan=0.):
    supersaw(M, 'str', t, n, dur, vol, cut=1800, a=.008, d=.08, s=.4, r=.06, voices=3, detune=.1)
def choir(M, t, n, dur, vol):
    for d in (-.08, .08): voice(M, 'choir', t, n + d, dur, vol * .5, pan=d * 5)

# =====================================================================
# 8) DETERMINED STEPS — 128 BPM, D minor (Undertale style)
# =====================================================================
def determined_steps():
    """All-piano version: left hand bass + broken chords, right hand melody (octaves in the last section)."""
    bpm = 120; st = 60 / bpm / 4; B = 16 * st
    CA = [([62, 65, 69], 38), ([58, 62, 65], 46), ([60, 64, 67], 48), ([57, 61, 64], 45)] * 2
    CB = [([55, 58, 62], 43), ([62, 65, 69], 38), ([58, 62, 65], 46), ([57, 61, 64], 45), ([53, 57, 60], 41), ([60, 64, 67], 48), ([58, 62, 65], 46), ([57, 61, 64], 45)]
    A = bars8([[74,-1,77,74,76,-1,72,-1],[74,-1,70,-1,72,74,-1,77],[79,-1,77,76,-1,72,-1,76],[76,-1,-1,73,-1,-1,69,-1],
               [74,-1,77,74,76,-1,81,-1],[79,-1,77,-1,74,77,-1,82],[81,-1,79,77,-1,76,-1,72],[73,-1,76,-1,81,-1,-1,-1]])
    Bm = bars8([[70,-1,-1,74,-1,-1,79,-1],[77,-1,76,74,-1,-1,69,-1],[70,-1,72,74,-1,77,-1,74],[76,-1,-1,-1,73,-1,-1,-1],
                [72,-1,-1,77,-1,-1,81,-1],[79,-1,77,76,-1,-1,72,-1],[74,-1,77,-1,79,-1,82,-1],[81,-1,-1,-1,-1,-1,0,0]])
    secs = [('intro', 4), ('A', 16), ('B', 16), ('A2', 16), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    P = lambda t, nn, d, v, pan=0.: piano(M, 'piano', t, nn, d, v, pan=pan)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = (CB if sec == 'B' else CA)[i % 8]
        lo = root - 12 if root > 40 else root
        if sec in ('intro', 'outro'):
            P(t0, lo, B * 1.1, .7, -.3)
            for q in range(4): P(t0 + q * 4 * st, ch[[0, 1, 2, 1][q]], 4 * st * 1.5, .38)
            play(A, i, t0, st, lambda t, nn, d: P(t, nn, d, .5, .2))
            if sec == 'outro' and i == n - 1:
                for nn, v in ((38, .6), (50, .5), (62, .45), (65, .4), (69, .4), (74, .45)): P(t0 + B, nn, 3.5, v)
            continue
        # left hand: bass octave on 1 and 3, broken chord 8ths in between
        P(t0, lo, 8 * st * 1.2, .65, -.3); P(t0 + 8 * st, lo + (7 if sec != 'B' else 12), 8 * st * 1.2, .5, -.3)
        broken = [ch[0], ch[1], ch[2], ch[1]] if sec != 'A2' else [ch[0], ch[2], ch[1] + 12, ch[2]]
        for k in range(8): P(t0 + k * 2 * st, broken[k % 4] - (12 if sec == 'B' else 0), 2 * st * 1.6, .28 if k % 2 else .34, -.1)
        mel = Bm if sec == 'B' else A
        play(mel, i, t0, st, lambda t, nn, d: P(t, nn, d, .62, .2))
        if sec == 'A2': play(mel, i, t0, st, lambda t, nn, d: P(t, nn + 12, d, .38, .3))
        if sec == 'B' and i >= 8: play(mel, i, t0, st, lambda t, nn, d: P(t, nn - 12, d, .3, .1))
    render2(M, 'Determined_Steps_piano_120bpm', sends={'piano': .32}, levels={'piano': 1.}, fade=0.)

# =====================================================================
# 9) CHANNEL PLAZA — 116 BPM, F major bossa nova (Wii menu style)
# =====================================================================
def channel_plaza():
    bpm = 116; st = 60 / bpm / 4; B = 16 * st
    CA = [([57, 60, 64, 65], 41), ([55, 60, 64, 67], 45), ([57, 62, 65, 69], 46), ([58, 62, 64, 67], 48)] * 2
    CB = [([58, 62, 65, 67], 43), ([58, 62, 64, 67], 48), ([57, 60, 64, 65], 41), ([57, 60, 62, 65], 38),
          ([58, 62, 65, 67], 43), ([58, 62, 64, 67], 48), ([55, 60, 64, 67], 45), ([54, 57, 60, 62], 38)]
    A = bars8([[72,-1,69,72,-1,76,-1,74],[72,-1,-1,69,-1,67,-1,64],[65,-1,69,-1,72,74,-1,77],[76,-1,74,-1,70,-1,-1,0],
               [72,-1,69,72,-1,76,-1,79],[77,-1,76,-1,72,-1,69,-1],[70,-1,74,-1,77,-1,74,72],[70,-1,-1,-1,67,-1,-1,-1]])
    Bm = bars8([[74,-1,72,70,-1,67,-1,70],[72,-1,-1,-1,0,70,72,74],[76,-1,72,-1,69,-1,72,-1],[74,-1,-1,-1,0,0,0,0],
                [74,-1,77,-1,74,-1,70,-1],[76,-1,74,-1,72,-1,70,-1],[72,-1,76,-1,79,-1,76,-1],[78,-1,-1,-1,0,0,0,0]])
    secs = [('intro', 4), ('A', 16), ('B', 8), ('A', 16), ('B', 8), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    clave = [0, 3, 6, 10, 12]  # 3-2 bossa clave
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = (CB if sec == 'B' else CA)[i % 8]
        for s in (0, 3, 6, 10, 12):
            for j, c in enumerate(ch): epiano(M, 'keys', t0 + s * st + j * .006, c, st * (2.4 if s in (0, 6) else 1.3), .06, pan=(j - 1.5) * .2)
        for k in range(16): shaker(M, t0 + k * st, .55 if k % 2 else .3)
        if sec == 'intro': continue
        for s in clave: rim(M, t0 + s * st, .6)
        for s in (0, 6, 8, 14): kick(M, t0 + s * st, .45, punch=.6)
        for s, o, L in ((0, 0, 5), (6, 7, 2), (8, 0, 5), (14, 7, 2)): bass(M, 'bass', t0 + s * st, root + o, L * st * .9, .55, cut=600, growl=-1)
        if sec == 'A':
            play(A, i, t0, st, lambda t, nn, d: mallet(M, 'lead', t, nn, d, .9, pan=.1))
            if i >= 8: play(A, i, t0, st, lambda t, nn, d: mallet(M, 'lead', t, nn + 12, d, .25, pan=-.3, trem=.3))
        if sec == 'B': play(Bm, i, t0, st, lambda t, nn, d: flute(M, 'lead', t, nn, d * .95, .8))
        if sec == 'outro' and i == n - 1:
            for j, c in enumerate([53, 57, 60, 64, 67]): epiano(M, 'keys', t0 + B + j * .03, c, 2.5, .08)
            mallet(M, 'lead', t0 + B, 77, 1.5, .8)
    render2(M, 'Channel_Plaza_116bpm', sends={'keys': .25, 'lead': .3, 'drums': .05},
            levels={'keys': 1., 'lead': .9, 'bass': .9, 'drums': .8}, duck=(), fade=3.)

# =====================================================================
# 10) FROSTY PODIUM — 150 BPM, C major (Mario & Sonic Winter Games DS style)
# =====================================================================
def frosty_podium():
    bpm = 150; st = 60 / bpm / 4; B = 16 * st
    CA = [([60, 64, 67], 48), ([59, 62, 67], 47), ([57, 60, 64], 45), ([57, 60, 65], 41), ([57, 62, 65], 50), ([59, 62, 67], 43), ([60, 64, 67], 48), ([60, 64, 67], 48)]
    CB = [([57, 60, 65], 41), ([59, 62, 67], 43), ([59, 64, 67], 40), ([57, 60, 64], 45), ([57, 62, 65], 50), ([59, 62, 65], 43), ([60, 64, 67], 48), ([59, 62, 67], 43)]
    A = bars8([[67,-1,72,-1,76,-1,79,-1],[79,-1,77,76,-1,74,-1,-1],[76,-1,72,-1,69,-1,72,76],[77,-1,-1,-1,76,-1,74,-1],
               [74,-1,77,-1,81,-1,77,-1],[79,-1,-1,77,-1,74,71,-1],[72,-1,76,-1,79,-1,84,-1],[84,-1,-1,-1,0,0,0,0]])
    Bm = bars8([[81,-1,79,-1,77,-1,76,-1],[74,-1,76,-1,77,-1,79,-1],[79,-1,76,-1,71,-1,76,-1],[72,-1,-1,-1,76,-1,81,-1],
                [77,-1,81,-1,86,-1,84,-1],[83,-1,81,-1,79,-1,77,74],[76,-1,79,-1,84,-1,-1,-1],[0,0,0,0,0,0,0,0]])
    secs = [('intro', 4), ('A', 16), ('B', 16), ('A2', 16), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    fan = [(0, 67, 2), (2, 67, 2), (4, 72, 4), (8, 76, 4), (12, 79, 4)]
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = (CB if sec == 'B' else CA)[i % 8]
        for k in range(8): sleigh(M, t0 + k * 2 * st, .9 if k % 2 else .6)
        if sec == 'intro':
            if i % 2 == 0:
                for s, nn, L in fan: brass(M, 'lead', t0 + s * st, nn, L * st * .9, .45); brass(M, 'lead', t0 + s * st, nn - 12, L * st * .9, .25)
            for s in range(0, 16, 1 if i == n - 1 else 4): snare(M, t0 + s * st, .35 if i == n - 1 else .5)
            if i == 0: crash(M, t0, .6); timpani(M, t0, 36)
            continue
        if sec == 'outro':
            if i == 0: crash(M, t0, .7)
            for c in ch: brass(M, 'stab', t0, c, B * (2.5 if i == n - 1 else .9), .2)
            timpani(M, t0, 36, .8); glock(M, t0, 84, .5)
            continue
        for nn in ch: strings(M, t0, nn + 12, B, .08)
        if i % 8 == 0: crash(M, t0, .5)
        for s in (0, 8): kick(M, t0 + s * st, .8)
        for s in (4, 12): snare(M, t0 + s * st, .7)
        for k in range(16): hat(M, t0 + k * st, .2 if k % 2 else .12)
        if i % 8 == 7:
            for s in range(8, 16): snare(M, t0 + s * st, .25 + .05 * (s - 8))
        for k in range(8): bass(M, 'bass', t0 + k * 2 * st, root - 12 + (12 if k % 2 else 0), 2 * st * .85, .5, cut=900)
        for s in (2, 6, 10, 14):
            for c in ch: pluck(M, 'arp', t0 + s * st, c + 12, st * 1.2, .06, pan=.3)
        mel = Bm if sec == 'B' else A
        play(mel, i, t0, st, lambda t, nn, d: brass(M, 'lead', t, nn, d * .92, .45))
        play(mel, i, t0, st, lambda t, nn, d: glock(M, t, nn + 12, .28 if sec != 'A' else .15, pan=-.3))
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .2)
    render2(M, 'Frosty_Podium_150bpm', sends={'lead': .25, 'stab': .3, 'str': .3, 'glock': .4, 'perc': .2, 'drums': .06, 'fx': .3},
            levels={'lead': 1., 'lead_d': .25, 'stab': .8, 'str': .7, 'glock': .8, 'perc': .7, 'bass': .85, 'arp': .7, 'drums': .9, 'fx': .7},
            crush=(32768, 10))

# =====================================================================
# 11) COASTAL ROUTE — 132 BPM, G major (Pokemon Ruby/Sapphire route style)
# =====================================================================
def gba_trumpet(M, bus, t, n, dur, vol, pan=0.):
    N = int((dur + .05) * SR); tt = tarr(N); v = np.clip((tt - .18) / .12, 0, 1) * .25 * np.sin(2 * np.pi * 6.2 * tt)
    f = mtof(n) * 2 ** ((v - .4 * np.exp(-tt / .02)) / 12)
    x = sqr(f, N, .25) * .6 + saw(f, N) * .5; lo = lp(x, 900); y = lo + (lp(x, 3800) - lo) * np.clip(tt / .03, 0, 1) * (.6 + .4 * np.exp(-tt / .2))
    M.add(bus, t, y * envN(N, dur, .01, .2, .8, .04) * vol * .4, pan=pan)

def coastal_route():
    bpm = 132; st = 60 / bpm / 4; B = 16 * st
    CA = [([59, 62, 67], 43), ([59, 64, 67], 40), ([60, 64, 67], 48), ([57, 62, 66], 50), ([59, 62, 67], 43), ([59, 62, 66], 47), ([60, 64, 67], 48), ([57, 62, 66], 50)]
    CB = [([57, 60, 64], 45), ([57, 62, 66], 50), ([59, 62, 67], 43), ([59, 64, 67], 40), ([60, 64, 67], 48), ([57, 62, 66], 50), ([59, 64, 67], 40), ([57, 62, 66], 50)]
    A = bars8([[74,-1,71,74,79,-1,78,76],[78,-1,76,-1,71,-1,67,-1],[72,-1,76,-1,79,-1,76,72],[74,-1,-1,-1,0,74,76,78],
               [79,-1,78,79,81,-1,79,78],[78,-1,74,-1,71,-1,74,78],[76,-1,72,76,79,-1,84,-1],[81,-1,-1,-1,-1,-1,0,0]])
    Bm = bars8([[72,-1,76,-1,81,-1,79,76],[78,-1,-1,74,-1,-1,69,-1],[71,-1,74,-1,79,-1,78,79],[76,-1,-1,-1,0,71,74,76],
                [76,-1,72,-1,79,-1,76,-1],[78,-1,74,-1,81,-1,78,-1],[79,-1,-1,78,-1,-1,76,-1],[74,-1,-1,-1,0,0,0,0]])
    secs = [('intro', 2), ('A', 16), ('B', 16), ('A', 16), ('outro', 2)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = (CB if sec == 'B' else CA)[i % 8]
        for s in (0, 6, 8, 11): kick(M, t0 + s * st, .7, punch=.9)
        for s in (4, 12): snare(M, t0 + s * st, .6)
        for k in range(8): hat(M, t0 + k * 2 * st, .3 if k % 2 else .18)
        if i % 4 == 3 and sec != 'intro':
            for s in (12, 13, 14, 15): snare(M, t0 + s * st, .45)
        for k in range(8): bass(M, 'bass', t0 + k * 2 * st, root - 12 + (7 if k in (2, 6) else 0) + (12 if k % 2 else 0), 2 * st * .7, .5, cut=1000)
        for k in range(16): chip(M, 'arp', t0 + k * st, ch[[0, 1, 2, 1][k % 4]] + 12, st * .8, .22, pw=.5, pan=-.3, vib=False)
        for s in (0, 6, 10):
            for c in ch: chip(M, 'harm', t0 + s * st, c, st * 1.6, .18, pw=.25, pan=.3, vib=False)
        if sec in ('intro', 'outro'):
            if sec == 'outro' and i == n - 1:
                for c in (67, 71, 74, 79): gba_trumpet(M, 'lead', t0 + B, c, 1.2, .35)
            continue
        if i == 0: crash(M, t0, .5)
        mel = Bm if sec == 'B' else A
        play(mel, i, t0, st, lambda t, nn, d: gba_trumpet(M, 'lead', t, nn, d * .92, .9))
        if sec == 'B': play(mel, i, t0, st, lambda t, nn, d: gba_trumpet(M, 'lead', t, nn - 4, d * .9, .35, pan=.3))
    M.buses['lead_d'] = pingpong(M.buses['lead'], 3 * st, .3, taps=3)
    render2(M, 'Coastal_Route_132bpm', sends={'lead': .25, 'harm': .2, 'arp': .15, 'drums': .1},
            levels={'lead': 1., 'lead_d': .35, 'harm': .8, 'arp': .7, 'bass': .9, 'drums': .9, 'fx': .6},
            crush=(18157, 9))

# =====================================================================
# 12) HOMEBASE RISING — 112 BPM, C minor / Eb major (Fortnite Save the World style)
# =====================================================================
def homebase_rising():
    bpm = 112; st = 60 / bpm / 4; B = 16 * st
    CA = [([60, 63, 67], 48), ([60, 63, 68], 44), ([58, 63, 67], 51), ([58, 62, 65], 46), ([60, 63, 67], 48), ([60, 63, 68], 44), ([58, 62, 65], 46), ([59, 62, 67], 43)]
    CB = [([60, 63, 68], 44), ([58, 62, 65], 46), ([58, 62, 67], 43), ([60, 63, 67], 48), ([60, 63, 68], 44), ([58, 62, 65], 46), ([58, 63, 67], 51), ([58, 63, 67], 51)]
    A = bars8([[67,-1,-1,72,-1,-1,74,75],[75,-1,74,72,-1,-1,68,-1],[70,-1,-1,75,-1,-1,79,77],[77,-1,-1,-1,74,-1,70,-1],
               [72,-1,-1,75,-1,-1,79,80],[80,-1,79,77,-1,-1,75,-1],[74,-1,75,77,-1,79,-1,-1],[79,-1,-1,-1,-1,-1,0,0]])
    Bm = bars8([[75,-1,-1,77,79,-1,-1,80],[82,-1,-1,-1,79,-1,77,-1],[79,-1,-1,77,75,-1,-1,74],[75,-1,-1,-1,72,-1,-1,-1],
                [75,-1,-1,77,79,-1,80,82],[84,-1,-1,82,-1,80,-1,79],[79,-1,-1,-1,-1,-1,-1,-1],[75,-1,-1,-1,0,0,0,0]])
    secs = [('intro', 4), ('A', 16), ('B', 8), ('A2', 16), ('outro', 4)]
    bars = sections_to_bars(secs); M = Mix(len(bars) * B)
    for b, (sec, i, n) in enumerate(bars):
        t0 = b * B; ch, root = (CB if sec == 'B' else CA)[i % 8]
        if sec == 'intro':
            for nn in ch: choir(M, t0, nn + 12, B, .5)
            strings(M, t0, root, B, .12, att=.6)
            for s in range(0, 16, 1 if i == n - 1 else 8): timpani(M, t0 + s * st, 36, .3 + (.02 * s if i == n - 1 else .3))
            if i == n - 1: riser(M, t0, B, .4)
            continue
        if sec == 'outro':
            if i == 0: crash(M, t0, .7); timpani(M, t0, 39, 1.)
            if i in (0, 2):
                for c in (63, 67, 70, 75): brass(M, 'brass', t0, c, B * (1.8 if i == 2 else .9), .22)
                for c in (51, 58, 63, 67): strings(M, t0, c, B * 2.2, .1)
                choir(M, t0, 75, B * 2, .45)
            continue
        # low string ostinato (the engine of the track)
        pat = [0, 0, 12, 0, 7, 0, 12, 7]
        for k in range(8): stacc(M, t0 + k * 2 * st, root - 12 + pat[k] + 12, st * 1.4, .18)
        for nn in ch: strings(M, t0, nn + 12, B, .06 if sec != 'B' else .09)
        bass(M, 'bass', t0, root - 12, B * .95, .35, cut=400, growl=-1)
        # drums: big toms + snare, timpani on downbeats
        kick(M, t0, .8); kick(M, t0 + 10 * st, .6); snare(M, t0 + 8 * st, .7)
        for s in (4, 12): tom(M, t0 + s * st, 43, .5)
        if i % 2 == 0: timpani(M, t0, root - 12 if root - 12 > 30 else root, .6)
        if i % 8 == 0: crash(M, t0, .55)
        for k in range(0, 16, 2): ride(M, t0 + k * st, .35)
        if i % 4 == 3:
            for s in range(10, 16): snare(M, t0 + s * st, .3 + .08 * (s - 10))
        if sec == 'A':
            play(A, i, t0, st, lambda t, nn, d: brass(M, 'horn', t, nn - 12, d * .95, .45, bright=.6))
            if i >= 8: play(A, i, t0, st, lambda t, nn, d: glock(M, t, nn + 12, .12, pan=-.3))
        if sec == 'B':
            play(Bm, i, t0, st, lambda t, nn, d: brass(M, 'brass', t, nn, d * .95, .45))
            play(Bm, i, t0, st, lambda t, nn, d: brass(M, 'brass', t, nn - 12, d * .95, .3, pan=.2))
            if i % 2 == 0:
                for nn in ch: choir(M, t0, nn + 12, 2 * B, .35)
        if sec == 'A2':
            play(A, i, t0, st, lambda t, nn, d: brass(M, 'brass', t, nn, d * .95, .42))
            play(A, i, t0, st, lambda t, nn, d: strings(M, t, nn + 12, d * .95, .07, att=.05))
            if i % 2 == 0:
                for nn in ch: choir(M, t0, nn + 12, 2 * B, .28)
    render2(M, 'Homebase_Rising_112bpm', sends={'str': .4, 'brass': .35, 'horn': .4, 'choir': .5, 'glock': .4, 'drums': .15, 'fx': .4},
            levels={'str': .8, 'brass': 1., 'horn': .9, 'choir': .7, 'glock': .7, 'bass': .8, 'drums': .9, 'fx': .7}, duck=())

if __name__ == '__main__':
    {'8': determined_steps, '9': channel_plaza, '10': frosty_podium, '11': coastal_route, '12': homebase_rising}[sys.argv[1]]()
