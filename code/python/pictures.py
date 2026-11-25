"""Songs read from pictures (photos and drawings by TAziz322). The picture is read left to right like a score:
  - the melody: the picture is cut into thin columns, one per 8th note; in each column the most eye-catching spot
    (brightest against its surroundings, or the most colorful) gives the note: higher in the picture = higher note.
    Columns with nothing standing out are rests, and the same spot twice in a row holds the note.
  - the chords: every bar is a wider strip of the picture; its main color picks the chord
    (red = home chord, yellow = IV, green = V, cyan = ii, blue = vi, magenta = iii; gray/white/black strips keep the last chord).
  - the key comes from the picture's average color, major for bright pictures and minor for dark ones,
    the tempo from how busy the picture is (how many edges it has), and the instruments from how bright and colorful it is.
  - the song plays the picture twice: once with just keys, melody and a light beat, then again with the bass.
    The ending is the right edge of the picture: a bright edge rings out on a bell, a dark edge fades away.
Drawings (PDF scans) are cropped to the drawn art first, so the white paper around it isn't read.
python pictures.py all   (or names from PICS)"""
import sys, os, re
import numpy as np
from PIL import Image
from newstyles import *
from popkit import build
from songs5 import harp

UP = '/mnt/user-data/uploads/'
PICS = {   # name -> (file, title)
 'harbor': ('97598f04-image.jpg', 'Harbor Moon'), 'branches': ('7c59be96-image.jpg', 'Moon Through Branches'),
 'backyard': ('c1c3ae9a-image.jpg', 'Backyard Sun'), 'field': ('8dbfc1c2-image.jpg', 'Field at Sunset'),
 'hanging': ('8bb67a99-image.jpg', 'Hanging Tree'), 'whatsnext': ('0014063d-image.jpg', "What's Next"),
 'empty': ('01eafb90-image.jpg', 'Peacefully Empty'), 'stature': ('3616cae1-image.jpg', 'Stature'),
 'blooming': ('24ecb697-image.jpg', 'Blooming Away'), 'tarheel': ('e2e0baa0-image.jpg', 'Tar Heel Blue'),
 'fading': ('fad8c7fd-image.jpg', 'Fading Drops'), 'spring': ('402a5f82-image.jpg', 'This is What Spring Feels Like'),
 'rolling': ('d52e779a-image.jpg', 'Rolling Away'), 'once': ('1492dfde-image.jpg', 'What it Once Was'),
 'line': ('87d32e82-image.jpg', 'Line of Light'), 'fall': ('4ce5335f-image.jpg', 'This is What Fall Feels Like'),
 'dripping': ('b489d969-image.jpg', 'Dripping'),
 'chok': ('797aafc8-Amar_Chok_ar_Maata.pdf', 'Amar Chok ar Maata'), 'audor': ('e3527f32-Nuton_Audor.pdf', 'Nuton Audor'),
}
PICS2 = {   # the second set of photos
 'rush': ('ecbcf44f-image.jpg', 'Light Rush'), 'frost': ('0ed2c0b3-image.jpg', 'Frost Crystals'), 'koi': ('1f9594f9-image.jpg', 'Koi Pond'),
 'hibiscus': ('12424794-image.jpg', 'Hibiscus'), 'skyfall': ('7d747552-image.jpg', 'Neon Skyfall'), 'rarities': ('eb08eb37-image.jpg', 'Five Rarities'),
 'sparklers': ('34233e60-image.jpg', 'Sparkler Letters'), 'window': ('1d80b330-image.jpg', 'Window to the Harbor'), 'mirror': ('30d0f128-image.jpg', 'Mirror Lake'),
 'summit': ('99ca8584-image.jpg', 'Summit at Sunset'), 'redlight': ('ddbe556d-image.jpg', 'Red Light Rain'), 'flags': ('4b462488-image.jpg', 'Flags at the Rally'),
 'hydrangea': ('7ab3170e-image.jpg', 'Hydrangea'), 'above': ('04a64692-image.jpg', 'Lakeside From Above'), 'tower': ('39d5cd1a-image.jpg', 'Tower in the Clouds'),
 'daisies': ('1ad414c0-image.jpg', 'Daisies on the Blue Bench'), 'hummus': ('1c0cd2ef-image.jpg', 'Heavenly Hummus'), 'undertree': ('41cb4bfd-image.jpg', 'Under the Lakeside Tree'),
}
PICS2.update({
 'dock': ('3916808b-image.jpg', 'Green Valley Dock'), 'lookout': ('e0f4e1e9-image.jpg', 'Mountain Lookout'), 'sunwater': ('a7a00e29-image.jpg', 'Sun on the Water'),
 'hero': ('41381f7b-image.jpg', 'Waddle Warrior'), 'duo': ('6a779938-image.jpg', 'Brother in Arms'),
})
PICS.update(PICS2)

PICS3 = {   # the third set (more varied shapes from here on)
 'sandwiched': ('dc7b873e-image.jpg', 'Sky Sandwich'), 'mist': ('a7926546-image.jpg', 'Mystical Mist'), 'inside': ('75606773-image.jpg', 'An Inside Look'),
 'downtown': ('fd9d5800-image.jpg', 'Downtown'), 'toprun': ('5b2e514d-image.jpg', 'Top of the Run'), 'moonwin': ('459c8f24-image.jpg', 'Moonlit Window'),
 'moonglass': ('10408015-image.jpg', 'Moon Through the Glass'), 'starfield': ('0638ef4e-image.jpg', 'Starfield'), 'twimoon': ('af0cab22-image.jpg', 'Twilight Moon'),
 'blinds': ('bdd5f5b1-image.jpg', 'Shadow on the Blinds'), 'helping': ('f90c2d8d-image.jpg', 'A Helping Hand'), 'cliff': ('c7951f25-image.jpg', 'Cliffside Blooms'),
 'sidebyside': ('e3b6c341-image.jpg', 'Side by Side at Sunset'), 'umbrella': ('6887acd3-image.jpg', 'Under the Umbrella'), 'flock': ('48581c66-image.jpg', 'Flock in the Halo'),
 'palace': ('e8ffb329-image.jpg', 'Palace Road'), 'storm': ('2a31d330-image.jpg', 'Storm Over the Peaks'), 'snowfall': ('186ba1bf-image.jpg', 'Snowfall on the Slopes'),
 'overlook': ('1df67a87-image.jpg', 'City From the Hill'), 'corner': ('b2a73389-image.jpg', 'Corner View at Sunset'),
}
PICS.update(PICS3)

NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
FIFTHS = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
MAJ, MIN = [0, 2, 4, 5, 7, 9, 11], [0, 2, 3, 5, 7, 8, 10]

def load(path):
    if path.endswith('.pdf'):   # a scanned drawing: render the page, then crop to the art (where the paper stops being white)
        from pdf2image import convert_from_path
        im = convert_from_path(path, dpi=150)[0].convert('RGB'); g = np.asarray(im.convert('L')).astype(float)
        ink = g < 215; rows = np.where(ink.mean(1) > .02)[0]; cols = np.where(ink.mean(0) > .02)[0]
        pad = 6; im = im.crop((cols[0] + pad, rows[0] + pad, cols[-1] - pad, rows[-1] - pad))
    else: im = Image.open(path).convert('RGB')
    return im

def read_picture(im, bars=8):
    W = bars * 8; R = 24
    hsv = np.asarray(im.convert('HSV').resize((W * 2, R * 2), Image.LANCZOS)).astype(float) / 255
    hsv = hsv.reshape(R, 2, W, 2, 3).mean((1, 3))
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    g = np.asarray(im.convert('L').resize((256, 256))).astype(float) / 255
    busy = np.abs(np.diff(g, axis=1)).mean() + np.abs(np.diff(g, axis=0)).mean()
    vm, sm = V.mean(), S.mean()
    # the key: the average color (hue weighted by how colorful each spot is) around the circle of fifths
    w = (S * V).ravel(); ang = H.ravel() * 2 * np.pi
    hue = (np.arctan2((w * np.sin(ang)).sum(), (w * np.cos(ang)).sum()) / (2 * np.pi)) % 1
    root = FIFTHS[int(hue * 12) % 12]; minor = vm < .45
    scale = MIN if minor else MAJ
    # the melody: one eye-catching spot per 8th-note column
    from scipy.ndimage import uniform_filter
    detail = np.abs(V - uniform_filter(V, 5, mode='nearest')) + .5 * np.abs(S - uniform_filter(S, 5, mode='nearest'))
    sal = detail + .15 * (np.abs(V - np.median(V)) + .6 * S * V)   # local detail first (edges, lights, petals), overall brightness second
    peak = sal.max(0); thr = np.percentile(peak, 20)
    # on the beat: the outline (the first spot from the top with real detail: tree line, roof, statue, horizon);
    # off the beat: the single most eye-catching spot in that column
    cut = np.percentile(detail, 70)
    outline = np.array([int(np.argmax(detail[1:-1, k] > cut)) + 1 if (detail[1:-1, k] > cut).any() else int(sal[1:-1, k].argmax()) + 1 for k in range(W)])
    spot = sal[1:-1].argmax(0) + 1
    top = .6 * outline + .4 * spot                            # where the eye goes: mostly the outline, pulled toward the brightest detail
    top = np.convolve(np.pad(top, 1, mode='edge'), [.25, .5, .25], 'valid')
    base = 60 + root if root <= 6 else 48 + root
    lo, hi = np.percentile(top, 5), np.percentile(top, 95); hi = max(hi, lo + 4)   # stretch to the rows the picture actually uses
    def dgr(r): return int(round((1 - np.clip((r - lo) / (hi - lo), 0, 1)) * 11)) + 2
    def pitch(r, d=None):
        d = dgr(r) if d is None else d
        return base + 12 * (d // 7) + scale[d % 7]
    mel, last, run = [], None, 0
    for k in range(0, W, 2):   # one beat = two columns: one quarter note, or two 8ths when the picture moves a lot inside the beat
        if max(peak[k], peak[k + 1]) < thr: mel += [0, 0]; last = None; run = 0; continue
        d1, d2 = dgr(top[k]), dgr(top[k + 1])
        if abs(d1 - d2) >= 2: mel += [pitch(0, d1), pitch(0, d2)]; last = pitch(0, d2); run = 0; continue
        p = pitch(0, round((d1 + d2) / 2))
        if p == last and run < 2: mel += [-1, -1]; run += 1
        else: mel += [p, -1]; run = 0
        last = p
    if mel[0] == -1: mel[0] = pitch(top[0])
    rows = [mel[b * 8:(b + 1) * 8] for b in range(bars)]
    # the chords: each bar's color compared with the whole picture's color. Bars ranked from the coolest-shifted to the
    # warmest-shifted get vi, IV, I, V; a bar with a shift too small to matter keeps the last chord
    shift = []
    for b in range(bars):
        hs, ws = H[:, b * 8:(b + 1) * 8].ravel() * 2 * np.pi, (S[:, b * 8:(b + 1) * 8] * V[:, b * 8:(b + 1) * 8]).ravel() + 1e-6
        bh = np.arctan2((ws * np.sin(hs)).sum(), (ws * np.cos(hs)).sum()) / (2 * np.pi)
        shift.append(((bh - hue + .5) % 1 - .5) + .3 * (V[:, b * 8:(b + 1) * 8].mean() - vm))   # hue shift, nudged by brightness
    q = np.argsort(np.argsort(shift)) * 4 // bars
    chords = []
    for b in range(bars):
        d = [5, 3, 0, 4][q[b]]; pc = (root + scale[d]) % 12; third = (scale[(d + 2) % 7] - scale[d]) % 12
        chords.append(NAMES[pc] + ('m' if third == 3 else '' if third == 4 else 'm'))
    edge = V[:, -6:].mean()
    focus = pitch(np.unravel_index(sal.argmax(), sal.shape)[0])
    return dict(rows=rows, chords=chords, root=root, minor=minor, busy=busy, bright=vm, color=sm, edge=edge, focus=focus)

def ending(bright_edge, focus):
    def f(M, t0, st, S, i, n, tones, root):
        if i: return
        for c in tones[:3]: supersaw(M, 'pad', t0, c + 12, 32 * st, .09, cut=2200, a=.05, r=2.5, voices=3)
        if bright_edge:   # a bright right edge: the picture's brightest spot rings out on a bell
            celesta(M, 'glock', t0, focus, 3., .9); harp(M, t0 + 8 * st, tones[0] + 24, .8)
        else:             # a dark right edge: the brightest spot as one soft, fading note
            celesta(M, 'glock', t0, focus - 12, 3., .6)
    return f

def picture_song(name, bars=8):
    fn, title = PICS[name]; im = load(UP + fn); P = read_picture(im, bars)
    drawn = fn.endswith('.pdf')
    bpm = int(round(72 + 70 * np.clip((P['busy'] - .02) / .15, 0, 1)))
    if drawn:                      keys, lead, drums, bass = ['synthwave', 'pad'], 'saw80s', 'gated', 'octave'
    elif P['bright'] < .35:        keys, lead, drums, bass = ['pad', 'celesta'], 'fmbell', 'lofi', 'long'
    elif P['color'] < .35:         keys, lead, drums, bass = ['pad', 'pluck'], 'flute', 'brush', 'long'
    elif P['color'] > .6:          keys, lead, drums, bass = ['marimbaarp', 'pad'], 'plastic', 'halfpop', 'octave'
    else:                          keys, lead, drums, bass = ['pluck', 'pad'], 'marimba', 'halfpop', 'long'
    if P['busy'] > .12 and not drawn: drums = 'fourfloor' if not P['minor'] else 'halfpop'
    ch, rows = P['chords'], P['rows']; half = bars // 2
    lv = .75 if lead == 'flute' else 1.   # the flute sits a little lower
    s = {'intro': sec(2, ch[:2], keys=keys), 'intro2': sec(2, ch[2:4], keys=keys, drums=drums),   # keys, then the beat joins: the song steps in gently
         'A': sec(half, ch[:half], keys=keys, drums=drums, lead=lead, mel=rows[:half], lv=lv, kind='verse'),
         'B': sec(half, ch[half:], keys=keys, drums=drums, lead=lead, mel=rows[half:], lv=lv, kind='verse', crash=False),
         'A2': sec(half, ch[:half], keys=keys, drums=drums, bass=bass, lead=lead, mel=rows[:half], lv=lv, kind='verse', crash=False),
         'B2': sec(half, ch[half:], keys=keys, drums=drums, bass=bass, lead=lead, mel=rows[half:], lv=lv, kind='verse', crash=False),
         'end': sec(2, [ch[-1]], extra=ending(P['edge'] > .45, P['focus']), kind='outro')}
    file = re.sub(r'[^A-Za-z0-9]+', '_', title).strip('_')
    cfg = dict(file=file, title=title, bpm=bpm, sections=s, order=['intro', 'intro2', 'A', 'B', 'A2', 'B2', 'end'], chorus_keys=True, cont_tol=0.,
               gain_like={'intro': 'A', 'intro2': 'A', 'B': 'A', 'A2': 'A', 'B2': 'A'}, targets={'outro': -16.}, verb=2.6, ride_max=6.,
               levels={'keys': 2.2, 'pad': 2.2, 'glock': 2.2, 'str': 2.}, ride=1.)   # the keys stand out more in the verses, so the intro (same keys, same level) isn't faint   # the intro plays at the verses' level, so nothing drops when the melody comes in
    info = f"{title}: {NAMES[P['root']]} {'minor' if P['minor'] else 'major'}, {bpm} BPM, {lead} over {'+'.join(keys)}, {drums} beat | chords {' '.join(ch)}"
    return cfg, info

# ---------------- version 2: every picture also picks its own instruments, song shape, start and ending ----------------
PALETTES = {   # (keys, lead, drums, bass)
 'night':  [(['ep', 'pad'], 'fmbell', 'lofi', 'long'), (['piano', 'pad'], 'celesta', 'brush', 'long'), (['celesta', 'pad'], 'flute', 'lofi', 'sub')],
 'gray':   [(['piano', 'strings'], 'piano', 'brush', 'long'), (['nylon', 'pad'], 'guitar', 'brush', 'long'), (['harpsi', 'pad'], 'strings', 'march', 'long')],
 'warm':   [(['guitar', 'pad'], 'whistle', 'house', 'octave'), (['nylon', 'pad'], 'flute', 'dembow', 'sub'), (['citypop', 'pad'], 'synth', 'funk', 'funky')],
 'green':  [(['marimbaarp', 'pad'], 'marimba', 'halfpop', 'octave'), (['uke', 'pad'], 'whistle', 'funk', 'finger'), (['pizzarp', 'pad'], 'flute', 'halfpop', 'long')],
 'blue':   [(['pluck', 'pad'], 'sqbright', 'fourfloor', 'octave'), (['futurebass', 'pad'], 'plastic', 'trap', '808'), (['synthwave', 'pad'], 'saw80s', 'gated', 'synth8')],
}
SHAPES = [['A', 'B', 'A2', 'B2'], ['A', 'A2', 'B', 'B2'], ['A', 'B', 'brk', 'A2', 'B2'], ['A', 'B', 'tall', 'B2']]
STARTS = ['keys', 'melody', 'beat', 'swell', 'cold']
ENDS = ['ring', 'echo', 'fade', 'stop', 'tapestop', 'thin']

def picture_song_v2(name, bars=16):
    fn, title = PICS[name]; im = load(UP + fn); P = read_picture(im, bars)
    H = np.asarray(im.convert('HSV').resize((64, 64))).astype(float) / 255
    w = H[..., 1] * H[..., 2]; hue = (np.angle((w * np.exp(2j * np.pi * H[..., 0])).sum()) / (2 * np.pi)) % 1
    fam = 'night' if P['bright'] < .3 else 'gray' if P['color'] < .22 else 'warm' if (hue < .14 or hue > .9) else 'green' if hue < .45 else 'blue'
    seed = int(P['busy'] * 9973 + P['color'] * 7919 + P['bright'] * 6007 + P['root'] * 31)   # the picture's own numbers pick the variation
    keys, lead, drums, bass = PALETTES[fam][seed % 3]
    bpm = int(round(70 + 80 * np.clip((P['busy'] - .02) / .15, 0, 1)))
    if drums in ('house', 'fourfloor', 'gated', 'dembow'): bpm = max(bpm, 100)
    if keys[0] == 'futurebass' and bpm < 100: keys, drums, bass = ['pluck', 'pad'], 'halfpop', 'long'   # slow chord chops and trap pump too much at this tempo; softer parts instead
    shape = SHAPES[(seed // 3) % 4]
    start = 'cold' if P['color'] > .55 and P['busy'] > .1 else 'beat' if P['busy'] > .12 else 'swell' if P['bright'] < .3 else STARTS[(seed // 12) % 4]
    end = 'ring' if P['edge'] > .6 else 'fade' if P['edge'] < .2 else ENDS[(seed // 7) % 6]
    ch, rows = P['chords'], P['rows']; half = bars // 2
    flat = [n for r in rows for n in r]; last, run = None, 0
    for k, n in enumerate(flat):   # long empty stretches (plain sky) would leave holes: after half a bar of rest, the last note carries on
        if n > 0: last, run = n, 0
        elif n == 0:
            run += 1
            if run > 4 and last: flat[k] = -1 if flat[k - 1] != 0 else last
        else: run = 0
    rows = [flat[i:i + 8] for i in range(0, len(flat), 8)]
    if start == 'beat' and bpm < 90: start = 'keys'
    lv = .75 if lead == 'flute' else 1.
    up = [[n + 12 if n > 0 else n for n in r] for r in rows]   # the 'tall' part: the melody an octave higher
    s = {'A': sec(half, ch[:half], keys=keys, drums=drums, lead=lead, mel=rows[:half], lv=lv, kind='verse'),
         'B': sec(half, ch[half:], keys=keys, drums=drums, lead=lead, mel=rows[half:], lv=lv, kind='verse', crash=False),
         'A2': sec(half, ch[:half], keys=keys, drums=drums, bass=bass, lead=lead, mel=rows[:half], lv=lv, kind='verse', crash=False),
         'B2': sec(half, ch[half:], keys=keys, drums=drums, bass=bass, lead=lead, mel=rows[half:], lv=lv, kind='verse', crash=False),
         'brk': sec(4, ch[half:half + 4], keys=keys[-1:], lead=lead, mel=rows[half:half + 4], lv=lv, kind='verse'),   # a breakdown: just the pad and the melody
         'tall': sec(half, ch[:half], keys=keys, drums=drums, bass=bass, lead=lead, mel=up[:half], lv=lv * .6, kind='verse', crash=False)}
    intro = {'keys': sec(4, ch[:4], keys=keys), 'melody': sec(2, ch[:2], keys=keys[-1:], lead=lead, mel=rows[:2], lv=lv),
             'beat': sec(2, ch[:2], drums=drums), 'swell': sec(4, ch[:4], keys=keys[-1:], extra=lambda M, t0, st, S, i, n, T, r: i == 0 and riser(M, t0, 64 * st, .25)),
             'cold': None}[start]
    order = list(shape)
    if intro: s['intro'] = intro; order = ['intro'] + order
    cfg = dict(file=re.sub(r'[^A-Za-z0-9]+', '_', title).strip('_'), title=title, bpm=bpm, sections=s, order=order, chorus_keys=True, cont_tol=0., verb=2.6,
               levels={'keys': 2.2, 'pad': 2.2, 'glock': 2.2, 'str': 2.}, ride=1., ride_max=6., targets={'outro': -16.})
    last = order[-1]
    if end == 'ring': s['end'] = sec(2, [ch[-1]], extra=ending(True, P['focus']), kind='outro'); order.append('end')
    elif end == 'thin': s['end'] = sec(2, [ch[-1]], keys=keys[-1:], lead=lead, mel=rows[-1:] + [[0] * 8], lv=lv, kind='outro'); order.append('end')
    elif end == 'echo': cfg['echo_out'] = (8, .55, 7)
    elif end == 'fade': cfg['fadeout'] = 8.
    elif end == 'tapestop': s['end'] = sec(1, [ch[-1]], keys=keys, drums=drums, bass=bass, kind='outro'); order.append('end'); cfg['tapestop'] = True
    elif end == 'stop': s['end'] = sec(1, [ch[0]], extra=lambda M, t0, st, S, i, n, T, r: (kick(M, t0, .9), crash(M, t0, .4), [LEADS['piano'](M, t0, c + 12, 1.5, .6) for c in T[:3]]), fill=False, kind='outro'); order.append('end')
    ref = 'A2' if 'A2' in order else 'A'
    cfg['gain_like'] = {k: ref for k in s if k != ref}   # one steady level for the whole song
    info = f"{title}: {NAMES[P['root']]} {'minor' if P['minor'] else 'major'}, {bpm} BPM, {fam}: {lead} over {'+'.join(keys)}, {drums}; start {start}, shape {'-'.join(shape)}, end {end}"
    return cfg, info

class _All(dict):   # every picture song's settings, made when first asked for (tools/to_looplab.py reads pictures.ALL)
    def items(self):
        for k in PICS:
            if os.path.exists(UP + PICS[k][0]): yield k, (picture_song_v2 if k in PICS3 else picture_song)(k, 16)[0]
    def __contains__(self, k): return False
ALL = _All()

if __name__ == '__main__':
    names = list(PICS) if sys.argv[1] == 'all' else list(PICS2) if sys.argv[1] == 'set2' else sys.argv[1:]
    if sys.argv[1] == 'set3': names = list(PICS3)
    for k in names:
        cfg, info = (picture_song_v2 if k in PICS3 else picture_song)(k, 16); print(info, flush=True); build(cfg)
