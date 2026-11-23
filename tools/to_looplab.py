"""Turns TAziz322's coded songs into Loop Lab song code (simplified to Loop Lab's instruments and 8-bar sections),
so any song on the website can be opened in Loop Lab, changed and exported again.
Writes site/looplab/<song-id>.json and site/looplab/index.json. Run from the repo root: python tools/to_looplab.py"""
import importlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'code', 'python')); os.chdir(os.path.join(ROOT, 'code', 'python'))
OUT = os.path.join(ROOT, 'site', 'looplab'); os.makedirs(OUT, exist_ok=True)
def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('é', 'e')).strip('-')

# ---------- mapping the coded instruments onto Loop Lab's ----------
def first(names, table, default):
    for n in names:
        for key, val in table:
            if key in n: return val
    return default
CHORD = [('piano', 'piano'), ('stride', 'piano'), ('jazz', 'ep'), ('ep', 'ep'), ('citypop', 'ep'), ('amapiano', 'ep'), ('acoustic', 'strum'), ('uke', 'strum'),
         ('strum', 'strum'), ('guitar', 'guitar'), ('nylon', 'guitar'), ('banjo', 'guitar'), ('bluegrass', 'guitar'), ('stab', 'stabs'), ('brass', 'stabs'), ('horn', 'stabs'),
         ('power', 'stabs'), ('chip', 'chip'), ('gb', 'chip'), ('pluck', 'arp'), ('arp', 'arp'), ('synthwave', 'arp'), ('eurobeat', 'arp'), ('marimba', 'arp'),
         ('celesta', 'arp'), ('harpsi', 'arp'), ('pizz', 'arp'), ('steel', 'arp'), ('plastic', 'arp'), ('nightcore', 'arp'), ('futurebass', 'stabs')]
BASS = [('walk', 'walk'), ('upright', 'walk'), ('funky', 'funky'), ('slap', 'funky'), ('octave', 'octave'), ('synthwave', 'pump16'), ('synth8', 'root8'), ('finger', 'root8'),
        ('tuba', 'walk'), ('reggae', 'funky'), ('logdrum', 'funky'), ('wobble', 'long'), ('808', 'long'), ('sub', 'long'), ('reese', 'long'), ('long', 'long'), ('metal', 'pump16')]
LEAD = [('trumpet', 'trumpet'), ('brass', 'brass'), ('horn', 'brass'), ('organ', 'brass'), ('chip', 'chip'), ('gb', 'chip'), ('square', 'square'), ('sqbright', 'square'),
        ('voice', 'voice'), ('chop', 'voice'), ('falsetto', 'voice'), ('choir', 'voice'), ('flute', 'flute'), ('whistle', 'flute'), ('ocarina', 'flute'), ('danso', 'flute'),
        ('sax', 'sax'), ('clarinet', 'sax'), ('oboe', 'sax'), ('reed', 'sax'), ('accordion', 'sax'), ('piano', 'piano'), ('guitar', 'guitar'), ('crunch', 'guitar'),
        ('nylon', 'guitar'), ('banjo', 'guitar'), ('fiddle', 'guitar'), ('haegeum', 'guitar'), ('oud', 'guitar'), ('gayageum', 'guitar'), ('marimba', 'marimba'), ('xylo', 'marimba'),
        ('steel', 'marimba'), ('celesta', 'marimba'), ('fmbell', 'marimba'), ('plastic', 'marimba'), ('cowbell', 'marimba'), ('vibes', 'marimba'), ('harpsi', 'marimba'),
        ('fourier', 'soft'), ('saw80s', 'soft'), ('synth', 'soft'), ('strings', 'soft'), ('lead', 'soft'), ('theremin', 'soft')]
DRUMS = {   # 16-step patterns for each drum style (kick, snare, clap, hat, open)
 'four': dict(kick='x...x...x...x...', clap='....x.......x...', hat='..x...x...x...x.'),
 'house': dict(kick='x...x...x...x...', clap='....x.......x...', hat='xx.xxx.xxx.xxx.x', open='..x...x...x...x.'),
 'half': dict(kick='x.........x.....', snare='........x.......', hat='x.x.x.x.x.x.x.x.'),
 'trap': dict(kick='x......x..x.....', snare='........x.......', hat='xxxxxxxxxxxxxxxx'),
 'boombap': dict(kick='x.......x.x.....', snare='....x.......x...', hat='x.x.x.x.x.x.x.x.'),
 'rock': dict(kick='x.......x.x.....', snare='....x.......x...', hat='x.x.x.x.x.x.x.x.'),
 'punk': dict(kick='x...x...x...x...', snare='....x.......x...', hat='xxxxxxxxxxxxxxxx'),
 'metal': dict(kick='xxxxxxxxxxxxxxxx', snare='....x.......x...', hat='x.x.x.x.x.x.x.x.'),
 'funk': dict(kick='x......x..x.....', snare='....x.......x...', hat='xxxxxxxxxxxxxxxx', rim='.......x.......x'),
 'dnb': dict(kick='x.........x.....', snare='....x.......x...', hat='x.x.x.x.x.x.x.x.'),
 'break': dict(kick='x.x.......xx....', snare='....x..x.x..x..x', hat='x.x.x.x.x.x.x.x.'),
 'swing': dict(kick='x.......x.......', hat='x..xx..xx..xx..x', rim='....x.......x...'),
 'latin': dict(kick='x.....x.x.....x.', rim='x..x..x...x.x...', hat='xxxxxxxxxxxxxxxx'),
 'march': dict(kick='x.......x.......', snare='x.xxx.xxx.xxx.xx', hat='................'),
 'reggae': dict(kick='........x.......', rim='........x.......', hat='x.x.x.x.x.x.x.x.'),
 'jersey': dict(kick='x...x..x..x.x.x.', clap='....x.......x...', hat='x.x.x.x.x.x.x.x.'),
 'garage': dict(kick='x......x..x.....', snare='....x.......x...', hat='..xx..xx..xx..xx', rim='.....x.........x'),
 'none': {}}
DMAP = [('fourfloor', 'four'), ('eurobeat', 'four'), ('house', 'house'), ('halfpop', 'half'), ('dubstep', 'half'), ('lofi', 'half'), ('trap', 'trap'), ('phonk', 'trap'),
        ('boombap', 'boombap'), ('hyper', 'trap'), ('rock', 'rock'), ('gated', 'rock'), ('punk', 'punk'), ('ska', 'punk'), ('metal', 'metal'), ('funk', 'funk'),
        ('dnb', 'dnb'), ('steps_dnb', 'dnb'), ('breakbeat', 'break'), ('swing', 'swing'), ('jazz', 'swing'), ('brush', 'swing'), ('calypso', 'latin'), ('samba', 'latin'),
        ('mario', 'latin'), ('dembow', 'latin'), ('amapiano', 'four'), ('march', 'march'), ('drumline', 'march'), ('castle', 'march'), ('trailer', 'march'), ('polka', 'rock'),
        ('onedrop', 'reggae'), ('jersey', 'jersey'), ('2step', 'garage'), ('euclid', 'funk'), ('primes', 'four'), ('sierpinski', 'four'), ('steps', 'four'), ('darbuka', 'latin'), ('gqom', 'four')]
def drumrows(style, bars, crash=False):
    pat = DRUMS[first([style], DMAP, 'rock')] if style else {}
    out = {k: (pat.get(k, '.' * 16) * bars) for k in ['kick', 'snare', 'clap', 'rim', 'hat', 'open', 'crash']}
    if crash: out['crash'] = 'x' + out['crash'][1:]
    return out
def mel_events(rows, bars, up=0):
    flat = [x for b in range(bars) for x in rows[b % len(rows)]]; ev = []
    for i, x in enumerate(flat):
        if x > 0:
            L = 1
            while i + L < len(flat) and flat[i + L] == -1: L += 1
            ev.append([i * 2, int(x + up), L * 2])
    return ev
def key_of(ch):
    m = re.match(r'([A-G][b#]?)(.*)', ch); root, q = m.group(1), m.group(2)
    root = {'Db': 'C#', 'D#': 'Eb', 'Gb': 'F#', 'G#': 'Ab', 'A#': 'Bb'}.get(root, root)
    return root, ('minor' if q.startswith('m') and not q.startswith('maj') else 'major')
def split8(name, bars, chords, melody, drums, **kw):     # Loop Lab sections are up to 8 bars: longer ones become parts 1, 2...
    parts = []
    for p in range(0, bars, 8):
        nb = min(8, bars - p)
        parts.append({'name': (name if bars <= 8 else f'{name} {p // 8 + 1}')[:20], 'bars': nb, 'chords': chords[p:p + nb],
                      'melody': [[s - p * 16, n, min(L, (nb * 16) - (s - p * 16))] for s, n, L in melody if p * 16 <= s < (p + nb) * 16],
                      'drums': {k: v[p * 16:(p + nb) * 16] for k, v in drums.items()}, **kw})
    return parts

def from_popkit(cfg):
    secs, order = cfg['sections'], cfg['order']; out, index = [], {}
    for name in order:
        if name in index: continue
        s = secs[name]; nb = s['bars']; chords = [s['chords'][i % len(s['chords'])] for i in range(nb)]
        mel = mel_events(s['mel'], nb, s.get('up', 0)) if s.get('mel') and s.get('lead') else []
        sfx = ([[0, 'impact']] if s.get('impact') else []) + ([[(nb - 1) * 16, 'riser']] if s.get('riser') else [])
        parts = split8(name.capitalize(), nb, chords, mel, drumrows(s.get('drums'), nb, crash=bool(s.get('drums')) and name != 'intro'),
                       chordStyle=first(s.get('keys', []), CHORD, 'pad') if s.get('keys') else ('pad' if not s.get('extra') else 'off'),
                       bass=first([s['bass']], BASS, 'root8') if s.get('bass') else 'off', sfx=sfx)
        for k, p in enumerate(parts): p['sfx'] = [e for e in sfx if (k == 0 and e[1] == 'impact') or (k == len(parts) - 1 and e[1] == 'riser')]
        index[name] = list(range(len(out), len(out) + len(parts))); out += parts
    leads = [s.get('lead', '') for s in secs.values() if s.get('lead')]
    first_chord = next(s['chords'][0] for s in secs.values())
    root, scale = key_of(first_chord)
    return dict(name=cfg['title'], bpm=cfg['bpm'], swing=round(cfg.get('swing', 0), 2), kit='chip' if cfg.get('crush') else 'band',
                lead=first(leads, LEAD, 'soft'), scaleRoot=root, scale=scale, sections=out, arrangement=[i for n in order for i in index[n]],
                bassSound='chip' if cfg.get('crush') else 'synth')

def from_breakcore(cfg):
    ch = cfg['chords']; chords8 = [ch[(b // 2) % 4] for b in range(16)]
    def melody(blocks_):
        ev = []
        for b in range(4):
            for s, n, L in blocks_[b]: ev.append([b * 32 + s, int(n), int(L)])
        return ev
    mA = melody(cfg['melody']); mB = melody(cfg.get('melodyB') or cfg['melody'])
    half = lambda ev: [e for e in ev if e[0] < 128]
    br = drumrows('breakbeat', 8, True); none = drumrows(None, 8)
    build_dr = drumrows('dnb', 4); build_dr['hat'] = 'xxxxxxxxxxxxxxxx' * 4
    root, scale = key_of(ch[0]); keys = cfg.get('keys'); keys = keys if isinstance(keys, str) else 'piano'
    cs = {'piano': 'piano', 'ep': 'ep', 'guitar': 'guitar', 'koto': 'arp', 'glock': 'arp', 'harp': 'arp', 'vibes': 'arp'}.get(keys, 'arp')
    secs = [dict(name='Intro', bars=8, chords=chords8[:8], melody=[], drums=none, chordStyle=cs, bass='off', sfx=[]),
            dict(name='Build', bars=4, chords=chords8[:4], melody=[], drums=build_dr, chordStyle=cs, bass='off', sfx=[[48, 'riser']]),
            dict(name='Drop A', bars=8, chords=chords8[:8], melody=half(mA), drums=br, chordStyle=cs, bass='long', sfx=[[0, 'impact']]),
            dict(name='Breakdown', bars=8, chords=chords8[:8], melody=half(mA), drums=none, chordStyle='pad', bass='long', sfx=[[112, 'riser']]),
            dict(name='Drop B', bars=8, chords=chords8[:8], melody=half(mB), drums=br, chordStyle=cs, bass='long', sfx=[[0, 'impact']]),
            dict(name='Outro', bars=8, chords=chords8[:8], melody=[], drums=none, chordStyle=cs, bass='off', sfx=[])]
    mk = cfg.get('mel'); mk = mk if isinstance(mk, str) else 'lead'
    return dict(name=cfg['title'], bpm=min(cfg['bpm'], 200), swing=0, kit='band', lead=first([mk], LEAD, 'soft'), scaleRoot=root, scale=scale,
                sections=secs, arrangement=[0, 1, 2, 2, 3, 4, 4, 5], bassSound='synth')

MODS = {'bts_albums': 'SONGS', 'batch_a': 'SONGS', 'bgm': 'SONGS', 'pokemon_gens': 'SONGS', 'sonic_styles': 'SONGS', 'batch_c': 'SONGS', 'batch_d': 'SONGS',
        'mario_worlds': 'SONGS', 'hyperpop2': 'SONGS', 'genres': 'SONGS', 'bts_solos': 'SONGS', 'batch_e': 'BC POP', 'seasons': 'SONGS', 'styles_breakcore': 'SONGS',
        'sports': 'SONGS', 'math2': 'SONGS', 'concepts': 'SONGS', 'mathsong': 'SONG'}
index = {}
for mod, names in MODS.items():
    try: M = importlib.import_module(mod)
    except Exception as e: print('skip', mod, e); continue
    for nm in names.split():
        d = getattr(M, nm, None)
        if d is None: continue
        items = [(None, d)] if 'sections' in d or 'chords' in d else d.items()
        for k, v in items:
            if isinstance(v, tuple): v = next(x for x in v if isinstance(x, dict))
            if not isinstance(v, dict) or not v.get('title'): continue
            try: song = from_popkit(v) if isinstance(v.get('sections'), dict) else from_breakcore(v)
            except Exception as e: print('could not convert', v.get('title'), e); continue
            sid = slug(v['title']); json.dump(song, open(os.path.join(OUT, sid + '.json'), 'w'), separators=(',', ':'))
            index[sid] = dict(file=f'site/looplab/{sid}.json', src=f'code/python/{mod}.py', key=k)
# songs that are already built into Loop Lab (simplified by hand)
html = open(os.path.join(ROOT, 'loop-lab', 'index.html'), encoding='utf-8').read(); i = html.index('const PRESETS=') + 14
for p in json.loads(html[i:html.index(';\n', i)]):
    sid = slug(p['name'])
    if sid not in index: json.dump(p, open(os.path.join(OUT, sid + '.json'), 'w'), separators=(',', ':')); index[sid] = dict(file=f'site/looplab/{sid}.json', src=None, key=None)
json.dump(index, open(os.path.join(OUT, 'index.json'), 'w'), indent=0)
print(len(index), 'songs converted for Loop Lab')
