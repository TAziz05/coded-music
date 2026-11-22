"""Orchestral piece.
python songs5.py 15  -> Morning Over the Valley (cinematic orchestral in 3/4: harp, strings, woodwinds, horns, timpani)"""
import sys, subprocess
from scipy.io import wavfile
from engine import master, reverb_ir
from songs3 import timpani, glock, flute, tri
from instruments2 import *

# ---------- orchestra (all code) ----------
def violins(M, t, n, dur, vol, att=.3, pan=0., bus='str'):
    """String section: several slightly out-of-tune saws, each with its own vibrato, softened like bowed strings."""
    N = int((dur + .5) * SR); tt = tarr(N); x = np.zeros(N)
    for i in range(8):
        vib = .08 * np.sin(2 * np.pi * (4.8 + rng.random()) * tt + rng.random() * 6) * np.clip((tt - .2) / .4, 0, 1)
        x += saw(mtof(n + rng.uniform(-.1, .1) + vib), N)
    c = 1900 if n > 60 else 1200
    y = lp(lp(x, c, 2), c * 1.4, 2) + .12 * bp(x, 800, 1300)
    e = np.clip(tt / att, 0, 1) * np.where(tt < dur, 1., np.exp(-(tt - dur) / .25))
    M.add(bus, t, y * e * vol * .05, pan=pan)
def pizz(M, t, n, vol, pan=0.): M.add('bass', t, ks(mtof(n), .5, .45, .985) * vol * .5, pan=pan)
def harp(M, t, n, vol, pan=0.): M.add('harp', t, ks(mtof(n), 2.5, .7, .9993) * vol * .35, pan=pan)
def oboe(M, t, n, dur, vol, pan=0.):
    N = int((dur + .15) * SR); tt = tarr(N); v = np.clip((tt - .2) / .2, 0, 1) * .18 * np.sin(2 * np.pi * 5.4 * tt)
    f = mtof(n + v); x = tri(f, N) * .8 + sine(2 * f, N) * .35 + lp(saw(f, N), 1800) * .25
    y = lp(x, 3000) + .5 * bp(x, 1000, 1600)
    M.add('wind', t, y * envN(N, dur, .07, .3, .85, .12) * vol * .32, pan=pan)
def clarinet(M, t, n, dur, vol, pan=0.):
    N = int((dur + .15) * SR); tt = tarr(N); v = np.clip((tt - .25) / .2, 0, 1) * .1 * np.sin(2 * np.pi * 5 * tt)
    f = mtof(n + v); x = lp(lp(sqr(f, N, .5), 1300), 1600) * .7 + sine(f, N) * .5 + bp(noise(N), 1200, 3000) * .015
    M.add('wind', t, x * envN(N, dur, .06, .3, .85, .1) * vol * .28, pan=pan)
def horn(M, t, n, dur, vol, pan=0.):
    N = int((dur + .3) * SR); tt = tarr(N); v = np.clip((tt - .3) / .3, 0, 1) * .1 * np.sin(2 * np.pi * 5 * tt)
    f = mtof(n + v - .15 * np.exp(-tt / .06)); x = saw(f * 2 ** (-.05 / 12), N) + saw(f * 2 ** (.05 / 12), N)
    sw = np.clip(tt / .15, 0, 1); y = tri(f, N) * 1.2 + sine(f, N) * .6 + lp(lp(x, 700), 1100) * (.25 + .35 * sw)
    M.add('horn', t, y * envN(N, dur, .1, .3, .9, .25) * vol * .3, pan=pan)
def cymbal(M, t, vol=1.):
    N = int(3 * SR); tt = tarr(N)
    for c, p in ((0, -.4), (1, .4)): M.add('perc', t, lp(hp(noise(N), 3500), 12000) * np.exp(-tt / 1.3) * vol * .3, pan=p)
def roll(M, t, n, dur, vol):   # timpani roll that swells
    k = 0; T = 0
    while T < dur:
        timpani(M, t + T, n, vol * (.3 + .7 * T / dur) * (.8 + .2 * rng.random())); T += .07

def render_hall(M, name, sends, levels, fade=0.):
    for b in ('str', 'lead', 'wind', 'horn', 'low'):
        if b in M.buses: M.buses[b] = np.array([lp(c, 4500, 2) for c in M.buses[b]])
    out = master(M, sends, levels, set(), fade_out=fade, rev=reverb_ir(3.2, .85, 6000))
    wavfile.write(f'{name}.wav', SR, (out.T * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{name}.wav', '-b:a', '320k', f'{name}.mp3'], check=True)
    print(name, round(out.shape[1] / SR, 1), 's')

# =====================================================================
# 15) MORNING OVER THE VALLEY — 90 BPM in 3/4, D major
# =====================================================================
def morning_valley():
    st = 60 / 90 / 2; B = 6 * st   # eighth notes, six per bar
    C = {'D': [50, 57, 62, 66], 'Bm': [47, 54, 59, 62], 'G': [43, 55, 59, 62], 'A': [45, 57, 61, 64], 'F#m': [42, 54, 57, 61],
         'A/C#': [49, 57, 61, 64], 'D/F#': [42, 57, 62, 66], 'Em': [40, 55, 59, 64], 'F#': [42, 54, 58, 61]}
    intro = ['D', 'Bm', 'G', 'A', 'D', 'F#m', 'G', 'A']
    themeP = ['D', 'A/C#', 'Bm', 'F#m', 'G', 'D/F#', 'Em', 'A', 'D', 'A/C#', 'Bm', 'F#m', 'G', 'A', 'D', 'D']
    devP = ['Bm', 'G', 'Em', 'F#'] * 2
    coda = ['D', 'G', 'D', 'A', 'D', 'D']
    T1 = [[(0, 78, 4), (4, 76, 1), (5, 74, 1)], [(0, 73, 4), (4, 74, 1), (5, 76, 1)], [(0, 74, 3), (3, 71, 3)], [(0, 73, 6)],
          [(0, 71, 2), (2, 74, 2), (4, 79, 2)], [(0, 78, 4), (4, 76, 1), (5, 74, 1)], [(0, 76, 2), (2, 79, 2), (4, 78, 2)], [(0, 76, 6)],
          [(0, 78, 4), (4, 79, 1), (5, 81, 1)], [(0, 81, 4), (4, 79, 1), (5, 78, 1)], [(0, 78, 3), (3, 74, 3)], [(0, 76, 2), (2, 73, 2), (4, 69, 2)],
          [(0, 71, 2), (2, 74, 2), (4, 79, 2)], [(0, 81, 3), (3, 79, 2), (5, 76, 1)], [(0, 74, 6)], []]
    DEV = [[(0, 71, 2), (2, 73, 2), (4, 74, 2)], [(0, 76, 4), (4, 74, 2)], [(0, 73, 2), (2, 71, 2), (4, 67, 2)], [(0, 70, 6)],
           [(0, 74, 2), (2, 76, 2), (4, 78, 2)], [(0, 79, 4), (4, 78, 2)], [(0, 76, 2), (2, 74, 2), (4, 73, 2)], [(0, 73, 3), (3, 76, 3)]]
    plan = [('intro', c) for c in intro] + [('theme', c) for c in themeP] + [('dev', c) for c in devP] + [('climax', c) for c in themeP] + [('coda', c) for c in coda]
    M = Mix(len(plan) * B + 6); counts = {}
    for b, (sec, ch) in enumerate(plan):
        i = counts.get(sec, 0); counts[sec] = i + 1; t0 = b * B; v = C[ch]; root = v[0]
        loud = {'intro': 1.35, 'theme': .75, 'dev': .8, 'climax': 1., 'coda': 1.}[sec]
        # harp: rolling eighths up the chord (two octaves), the heartbeat of the piece
        if sec != 'climax' or i % 2 == 0:
            arp = [root + 12, v[1], v[2], v[3], v[2] + 12, v[3] + 12] if sec != 'climax' else [root + 12, v[1] + 12, v[2] + 12, v[3] + 12, v[2] + 24, v[3] + 24]
            for k in range(6): harp(M, t0 + k * st, arp[k], .9 * loud, pan=-.35 + k * .1)
        if sec == 'climax' and i % 4 == 3:   # harp glissando into the next phrase
            for j, nn in enumerate(range(v[1], v[1] + 26, 2)): harp(M, t0 + 3 * st + j * .07, nn, .5, pan=.3)
        # strings: sustained chord, longer swells in quiet parts
        for j, nn in enumerate(v[1:]): violins(M, t0, nn + (12 if sec == 'climax' else 0), B * .98, (.5 if sec in ('intro', 'coda') else .7) * loud, att=.5 if sec in ('intro', 'coda') else .2, pan=(j - 1) * .35)
        violins(M, t0, root, B * .98, .6 * loud, att=.3, pan=.3, bus='low')
        # bass: pizzicato on beat 1 (and 3 in the theme)
        if sec in ('theme', 'dev'):
            pizz(M, t0, root - 12 if root > 45 else root, .9); pizz(M, t0 + 4 * st, root + 7 - (12 if root > 45 else 0), .6)
        # melodies
        if sec == 'theme':
            for s, nn, L in T1[i]:
                if i < 8: flute(M, 'wind', t0 + s * st, nn, L * st * .95, .8)   # flute takes the tune first...
                else: oboe(M, t0 + s * st, nn, L * st * .95, .9)              # ...then the oboe
            if i >= 8:
                for s, nn, L in T1[i]: clarinet(M, t0 + s * st, nn - 12, L * st * .95, .45, pan=-.3)
        if sec == 'dev':
            for s, nn, L in DEV[i]: oboe(M, t0 + s * st, nn, L * st * .95, .9, pan=.15)
            if i >= 4:
                for s, nn, L in DEV[i]: horn(M, t0 + s * st, nn - 12, L * st * .95, .6, pan=-.2)
            if i == 7: roll(M, t0, 45, B, .55)
            for k in range(6): violins(M, t0 + k * st, v[1] - 12 if v[1] > 52 else v[1], st * .5, .25, att=.02, bus='low')   # driving low strings
        if sec == 'climax':
            if i % 8 == 0: cymbal(M, t0, .8); timpani(M, t0, 38, .9)
            elif i % 2 == 0: timpani(M, t0, 38 if ch in ('D', 'D/F#', 'Bm') else 45, .55)
            for s, nn, L in T1[i]:
                horn(M, t0 + s * st, nn - 12, L * st * .97, .9); horn(M, t0 + s * st, nn - 24, L * st * .97, .5, pan=.2)
                violins(M, t0 + s * st, nn, L * st * .97, .55, att=.08, bus='lead')
                violins(M, t0 + s * st, nn + 12, L * st * .97, .3, att=.08, bus='lead')
            for k, nn in enumerate([root - 12 if root > 45 else root] * 3): pizz(M, t0 + k * 2 * st, nn, .8)
            if i == 15: roll(M, t0, 38, B, .4)
        if sec == 'coda':
            if i == 0: cymbal(M, t0, .3)
            if i in (0, 2):
                for s, nn, L in T1[0 if i == 0 else 5]: flute(M, 'wind', t0 + s * st, nn, L * st * .95, .7)
            if i >= 4: glock(M, t0, 86 if i == 4 else 90, .3)
            if i == 5:
                for nn in (50, 57, 62, 66, 69, 74): violins(M, t0, nn, B * 2.5, .45, att=.6)
                timpani(M, t0, 38, .35)
    render_hall(M, 'Morning_Over_the_Valley_90bpm',
                sends={'str': .45, 'low': .35, 'lead': .45, 'wind': .45, 'horn': .5, 'harp': .4, 'bass': .25, 'drums': .35, 'perc': .4, 'glock': .5},
                levels={'str': .9, 'low': .8, 'lead': .8, 'wind': 1., 'horn': .9, 'harp': .8, 'bass': .8, 'drums': .9, 'perc': .7, 'glock': .7}, fade=0.)

if __name__ == '__main__':
    {'15': morning_valley}[sys.argv[1]]()
