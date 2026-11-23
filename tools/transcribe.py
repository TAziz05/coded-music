"""Makes Loop Lab versions of songs that weren't built with popkit or the breakcore engine (the early custom-coded songs
and the 8 browser game songs). It 'listens in' on the code instead of the audio: while a song's code runs, every note an
instrument plays and every drum hit is written down, then the notes become Loop Lab chords, melody, bass and drum patterns.
Writes site/looplab/<song-id>.json and adds them to site/looplab/index.json. Run from the repo root: python tools/transcribe.py"""
import importlib, json, os, re, subprocess, sys, collections
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, 'code', 'python'); sys.path.insert(0, PY); os.makedirs('/tmp/transcribe_out', exist_ok=True); os.chdir('/tmp/transcribe_out')   # any audio a song writes lands here, not in the repo
OUT = os.path.join(ROOT, 'site', 'looplab')
def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('é', 'e')).strip('-')

# ---------------- listening in ----------------
EV, DR, PEND, BT = [], [], [], []
import engine
def rec_mtof(orig):
    def f(n, *a, **k):
        try: PEND.append(float(np.mean(n)))
        except Exception: pass
        return orig(n, *a, **k)
    return f
_add = engine.Mix.add
def add(self, bus, t, *a, **k):
    L = len(a[0]) if a and hasattr(a[0], '__len__') else 0
    for n in sorted({round(x, 1) for x in PEND if 20 < x < 110}): EV.append((bus, float(t), n, L))   # every note mixed into this sound (chords too)
    BT.append((bus, float(t))); PEND.clear(); return _add(self, bus, t, *a, **k)
engine.Mix.add = add
DRUMS = ('kick', 'snare', 'clap', 'hat', 'rim', 'crash', 'shaker', 'tom', 'boom_kick', 'boom_snare', 'chipkick', 'chipsnare', 'chiphat', 'ride', 'bayan', 'dayan', 'ka', 'taiko')
def rec_drum(name, orig):
    def f(M, t, *a, **k):
        DR.append((name, float(t))); PEND.clear(); r = orig(M, t, *a, **k); PEND.clear(); return r
    f._rec = True; return f
def patch(mod):
    for name in dir(mod):
        obj = getattr(mod, name)
        if name == 'mtof' and not getattr(obj, '_rec', False): g = rec_mtof(obj); g._rec = True; setattr(mod, name, g)
        if name in DRUMS and callable(obj) and not getattr(obj, '_rec', False): setattr(mod, name, rec_drum(name, obj))
        if name.startswith('render') and callable(obj): setattr(mod, name, lambda *a, **k: None)   # don't write audio files

# ---------------- turning notes into Loop Lab ----------------
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
def best_chord(w):
    best, name = -1, 'C'
    for r in range(12):
        for q, iv in (('', (0, 4, 7)), ('m', (0, 3, 7))):
            sc = sum(w[(r + i) % 12] for i in iv) + .5 * w[r] - .3 * sum(w[(r + i) % 12] for i in ((1, 6) if q == '' else (1, 4)))
            if sc > best: best, name = sc, NAMES[r] + q
    return name
LEADB = ('lead', 'flute', 'mel', 'vox', 'leadf', 'brass', 'gtr', 'syn', 'horn', 'chip', 'piano', 'sax', 'trumpet')
def lead_kind(bus):
    for k, v in (('flute', 'flute'), ('brass', 'brass'), ('horn', 'brass'), ('trumpet', 'trumpet'), ('sax', 'sax'), ('gtr', 'guitar'), ('chip', 'chip'), ('vox', 'voice'), ('piano', 'piano'), ('glock', 'marimba')):
        if k in bus: return v
    return 'soft'
def to_looplab(title, bpm, ev, dr, swing=0., beats_per_bar=4, kit='band', BT=()):
    st = 60 / bpm / 4; spb = 4 * beats_per_bar
    if not ev: raise ValueError('no notes')
    T = max(t for _, t, _, _ in ev); nbars = int(T / (spb * st)) + 1
    buses = collections.defaultdict(list)
    for b, t, n, L in ev: buses[b].append((t, n, L))
    stats = {}
    for b, xs in buses.items():
        ts = collections.Counter(round(t / st) for t, _, _ in xs); poly = sum(c > 1 for c in ts.values()) / max(1, len(ts))
        stats[b] = (len(xs), np.mean([n for _, n, _ in xs]), poly)
    bassb = [b for b, (c, m, p) in stats.items() if m < 50 or any(k in b for k in ('bass', 'sub', 'reese', '808'))]
    cand = [b for b, (c, m, p) in stats.items() if b not in bassb and p < .35 and m > 62 and c >= 8]
    pref = [b for b in cand if any(k in b for k in LEADB)]
    mel_bus = max(pref or cand, key=lambda b: stats[b][0]) if (pref or cand) else None
    if not mel_bus:   # no clean one-note-at-a-time instrument: use the top note of the highest instrument
        hi = [b for b, (c, m, p) in stats.items() if b not in bassb and c >= 8]
        mel_bus = max(hi, key=lambda b: stats[b][1]) if hi else None
    # melody: the highest note of the melody instrument on each 16th step
    mel = {}
    if mel_bus:
        for t, n, L in buses[mel_bus]:
            s = round(t / st)
            if s not in mel or n > mel[s]: mel[s] = n
    if len(mel) < 20:   # too sparse: take the top line of the busiest non-bass instrument instead
        hi = [b for b, (c, m, p) in stats.items() if b not in bassb and c >= 8]
        if hi:
            mel_bus = max(hi, key=lambda b: stats[b][0]); mel = {}
            for t, n, L in buses[mel_bus]:
                s = round(t / st)
                if s not in mel or n > mel[s]: mel[s] = n
    # chords: the pitch classes sounding in each bar
    pcw = np.zeros((nbars, 12))
    for b, xs in buses.items():
        if b in bassb or b == mel_bus: continue
        for t, n, L in xs:
            bar = int(round(t / st) // spb)
            if 0 <= bar < nbars: pcw[bar, int(round(n)) % 12] += 1
    for b in bassb:   # the bass root counts too
        for t, n, L in buses[b]:
            bar = int(round(t / st) // spb)
            if 0 <= bar < nbars: pcw[bar, int(round(n)) % 12] += 1.5
    chords, last = [], 'C'
    for bar in range(nbars):
        if pcw[bar].sum() > 0: last = best_chord(pcw[bar])
        chords.append(last)
    hits = collections.defaultdict(set)
    MAP = {'kick': 'kick', 'boom_kick': 'kick', 'chipkick': 'kick', 'bayan': 'kick', 'taiko': 'kick', 'snare': 'snare', 'boom_snare': 'snare', 'chipsnare': 'snare',
           'clap': 'clap', 'hat': 'hat', 'chiphat': 'hat', 'shaker': 'hat', 'ride': 'hat', 'dayan': 'hat', 'rim': 'rim', 'ka': 'rim', 'tom': 'rim', 'crash': 'crash'}
    for name, t in dr: hits[MAP.get(name, 'hat')].add(round(t / st))
    # chopped breakbeats (sliced drum loops) don't go through the drum functions: write an amen-style pattern where they play
    brk = {int(round(t / st) // spb) for b, t in BT if 'break' in b}
    for bar in brk:
        if sum(1 for k in hits for s in hits[k] if s // spb == bar) > 4: continue
        a = bar * spb
        for s, k in ((0, 'kick'), (2, 'kick'), (10, 'kick'), (11, 'kick'), (4, 'snare'), (7, 'snare'), (9, 'snare'), (12, 'snare'), (15, 'snare')): hits[k].add(a + s)
        for s in range(0, 16, 2): hits['hat'].add(a + s)
    keys_bus = max((b for b in buses if b not in bassb and b != mel_bus), key=lambda b: stats[b][0], default='')
    cstyle = 'piano' if 'piano' in keys_bus else 'arp' if any(k in keys_bus for k in ('arp', 'harp', 'glock', 'koto', 'pluck')) else 'guitar' if 'gtr' in keys_bus else 'ep' if any(k in keys_bus for k in ('keys', 'organ', 'ep')) else 'pad'
    bass_style = 'off' if not bassb else ('long' if np.mean([L for b in bassb for _, _, L in buses[b]] or [0]) > 2 * spb * st * 44100 / 8 else 'root8')
    secs, arrangement, seen = [], [], {}
    for p in range(0, nbars, 8):
        nb = min(8, nbars - p); a0, a1 = p * spb, (p + nb) * spb
        melody = []
        steps = sorted(s for s in mel if a0 <= s < a1)
        for j, s in enumerate(steps):
            nxt = steps[j + 1] if j + 1 < len(steps) else a1
            melody.append([int(s - a0), int(round(mel[s])), int(max(1, min(nxt - s, 8)))])
        drums = {k: ''.join('x' if (a0 + i) in hits[k] else '.' for i in range(nb * spb)) for k in ('kick', 'snare', 'clap', 'rim', 'hat', 'open', 'crash')}
        has_bass = any(a0 <= round(t / st) < a1 for b in bassb for t, _, _ in buses[b])
        sec = dict(name=f'Part {len(secs) + 1}', bars=nb, chords=chords[p:p + nb], melody=melody, drums=drums, chordStyle=cstyle,
                   bass=bass_style if has_bass else 'off', sfx=[])
        key = json.dumps([sec['chords'], sec['melody'], sec['drums']], sort_keys=True)
        if key in seen: arrangement.append(seen[key]); continue
        seen[key] = len(secs); arrangement.append(len(secs)); secs.append(sec)
    root = chords[min(len(chords) - 1, 2)]; m = re.match(r'([A-G][b#]?)(m?)', root)
    return dict(name=title, bpm=int(round(min(bpm, 200))), swing=swing, kit=kit, lead=lead_kind(mel_bus or ''), scaleRoot=m.group(1),
                scale='minor' if m.group(2) else 'major', sections=secs[:24], arrangement=[a for a in arrangement if a < 24], bassSound='synth')

# ---------------- the songs ----------------
PYSONGS = [  # title, module, function (+ args), bpm, beats per bar, swing
 ('Overclocked', 'songs', 'dnb', (), 174, 4, 0), ("Nobody's Looking", 'songs', 'breakcore', (), 180, 4, 0),
 ('Lantern Theory', 'songs2', 'lantern_theory', (), 150, 4, 0), ('Homebase Rising', 'songs3', 'homebase_rising', (), 112, 4, 0),
 ('Ringworld Vigil', 'songs4', 'ringworld_vigil', (), None, 4, 0), ('Boundless Run', 'songs4', 'boundless_run', ('crunch',), 155, 4, 0),
 ('Morning Over the Valley', 'songs5', 'morning_valley', (), 90, 4, 0), ('Shattered Overture', 'songs6', 'shattered_overture', (), None, 4, 0),
 ('Paper Sky', 'songs7', 'paper_sky', (), 170, 4, 0), ('Golden Hour Groove', 'songs9', 'golden_hour', (), 114, 4, 0),
 ('Blue Spark Runaway', 'songs9', 'blue_spark', (), 160, 4, 0), ('Off the Lines', 'songs10', 'cortis_hype', (), 150, 4, 0),
 ('Breeze in the Alley', 'songs10', 'kaze_style', (), 98, 4, .12), ('Riverbank Evening', 'southasia', 'riverbank', (), 96, 4, 0),
 ('Monsoon Breaks', 'southasia', 'monsoon_breaks', (), 172, 4, 0), ('Winds of the World', 'batch_c', 'winds_of_the_world', (), 104, 4, 0),
 ('Coral Waltz', 'mario_worlds', 'coral_waltz', (), 150, 3, 0)]
def bpm_from_source(mod, fn):   # songs whose tempo isn't in the table: read 'bpm = ...' from the function
    import inspect
    m = re.search(r'bpm\s*=\s*(\d+)', inspect.getsource(getattr(mod, fn))); return int(m.group(1)) if m else 120

index = json.load(open(os.path.join(OUT, 'index.json')))
only = sys.argv[1:]
for title, modname, fn, args, bpm, bpb, sw in PYSONGS:
    if only and slug(title) not in only: continue
    EV.clear(); DR.clear(); PEND.clear(); BT.clear()
    try:
        mod = importlib.import_module(modname)
        for m in list(sys.modules.values()):
            if getattr(m, '__file__', '') and os.path.dirname(os.path.abspath(m.__file__)) == PY: patch(m)
        if not hasattr(mod, fn):   # Winds of the World: find the function that renders it
            fn = next(n for n in dir(mod) if 'flute' in n.lower() and callable(getattr(mod, n)))
        bpm = bpm or bpm_from_source(mod, fn)
        getattr(mod, fn)(*args)
        song = to_looplab(title, bpm, EV, DR, sw, bpb, BT=BT)
    except Exception as e: print('could not transcribe', title, '-', e); continue
    sid = slug(title); json.dump(song, open(os.path.join(OUT, sid + '.json'), 'w'), separators=(',', ':'))
    index[sid] = dict(file=f'site/looplab/{sid}.json', src=f'code/python/{modname}.py', key=fn)
    print('transcribed', title, f"({len(EV)} notes, {len(DR)} drum hits, {len(song['sections'])} sections)", flush=True)

# ---------------- the 8 browser game songs (JavaScript): run them in Node with recording stand-ins ----------------
GAME = [('Lobby', 'Drop-In Daily', 'fnMenu'), ('Match', 'Drop-In Daily', 'fn'), ('Mythic Match (OG style)', 'Drop-In Daily', 'fnOGm'),
        ('Endless Summary (OG lobby style)', 'Drop-In Daily', 'fnOG'), ('Route', 'Daily Poké Catch', 'pkMenu'), ('Battle', 'Daily Poké Catch', 'pk'),
        ('Mythic Battle', 'Daily Poké Catch', 'pkB'), ('Town', 'Daily Poké Catch', 'pkTown')]
JS = r"""
const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');const ev=[],dr=[];let T=0;
const hz=n=>440*2**((n-69)/12),midi=f=>69+12*Math.log2(f/440);
const fake=()=>new Proxy(function(){},{get:(o,k)=>k==='currentTime'?0:k==='gain'||k==='frequency'||k==='detune'||k==='Q'?{value:0,setValueAtTime(){},linearRampToValueAtTime(){},exponentialRampToValueAtTime(){},setTargetAtTime(){}}:fake(),apply:()=>fake()});
global.A={currentTime:0,createGain:()=>({gain:{setTargetAtTime(){},setValueAtTime(){},value:1},connect(){}})};global.musBus={};global.SONGS={};
global.ctx=()=>global.A;global.verb=()=>({});
global.tone=({t=0,n,f,type='square',dur=.12,slide,vol})=>{if(slide&&f&&!n&&f<200){dr.push(['kick',T+t]);return}if(n===undefined&&f)n=midi(f);ev.push([type,T+t,n,dur,vol||0])};
global.noise=({t=0,freq=6000,type='highpass',dur=.1})=>{dr.push([freq<800?'kick':freq<3000?'snare':'hat',T+t])};
global.brass=({t=0,n,dur=.4})=>ev.push(['brass',T+t,n,dur,1]);global.flute=({t=0,n,dur=.3})=>ev.push(['flute',T+t,n,dur,1]);global.horn=({t=0,n,dur=.4})=>ev.push(['horn',T+t,n,dur,1]);
global.pluck=(t,n,vol,dur=.3)=>ev.push(['pluck',T+t,n,dur,1]);global.mallet=(t,n)=>ev.push(['mallet',T+t,n,.4,1]);global.glock=(t,n)=>ev.push(['glock',T+t,n,1,1]);
global.strings=({t=0,ns,dur=1})=>ns.forEach(n=>ev.push(['strings',T+t,n,dur,1]));global.aah=({t=0,ns,dur=1})=>ns.forEach(n=>ev.push(['strings',T+t,n,dur,1]));
global.harp=(t,ns)=>ns.forEach(n=>ev.push(['harp',T+t,n,.6,1]));global.stab=(t,ns,v,dur=.16)=>ns.forEach(n=>ev.push(['brass',T+t,n,dur,1]));
global.wub=(t,n,o={})=>ev.push(['bass',T+t,n,o.dur||.22,1]);global.snare=(t)=>dr.push(['snare',T+t]);global.boom=(t)=>dr.push(['kick',T+t]);
global.roll=()=>{};global.swell=()=>{};global.fadeBus=()=>({});
const song=eval('('+src+')');const st=60/song.bpm/4;
for(let r=0;r<2;r++)for(let i=0;i<song.steps;i++){T=(r*song.steps+i)*st;try{song.play(i,0)}catch(e){}}
console.log(JSON.stringify({bpm:song.bpm,steps:song.steps,ev,dr}));
"""
open('/tmp/rec_song.js', 'w').write(JS)
BUS = {'brass': 'brass', 'flute': 'flute', 'horn': 'brass', 'glock': 'glock', 'mallet': 'glock', 'pluck': 'arp', 'harp': 'arp', 'strings': 'pad', 'bass': 'bass',
       'square': 'chip', 'pulse': 'chip', 'pulse2': 'chip', 'triangle': 'keys', 'sawtooth': 'pad', 'sine': 'keys'}
for title, game, key in GAME:
    try:
        r = json.loads(subprocess.run(['node', '/tmp/rec_song.js', os.path.join(ROOT, 'code', 'songs', key + '.js')], capture_output=True, text=True, timeout=60).stdout)
        ev = [(('bass' if n < 50 else BUS.get(typ, 'keys')), t, n, d * 44100) for typ, t, n, d, v in r['ev'] if n is not None]
        song = to_looplab(f'{game}: {title}', r['bpm'], ev, [(n, t) for n, t in r['dr']], kit='chip' if key.startswith('pk') else 'band')
        song['name'] = title
    except Exception as e: print('could not transcribe', title, '-', e); continue
    sid = slug(game + ' ' + title); json.dump(song, open(os.path.join(OUT, sid + '.json'), 'w'), separators=(',', ':'))
    index[sid] = dict(file=f'site/looplab/{sid}.json', src=f'code/songs/{key}.js', key=key)
    print('transcribed', title, f"({len(ev)} notes)", flush=True)
json.dump(index, open(os.path.join(OUT, 'index.json'), 'w'), indent=0)
