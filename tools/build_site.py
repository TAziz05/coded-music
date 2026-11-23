"""Builds the song website data: site/songs.json and site/thumbs/.
For every song it reads the README table and title-card list, then listens to the MP3 to work out:
  - a seamless loop (two bar lines where the music is the same, so it can jump back without a seam)
  - what it sounds like (timbre, brightness, busyness) -> 'sounds similar' lists
  - its energy shape over time -> 'similar structure' lists
Run from the repo root: python tools/build_site.py   (needs ffmpeg, numpy, scipy)"""
import ast, json, os, re, subprocess, sys
import numpy as np, scipy.signal as ss

SR = 22050
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); os.makedirs('site/thumbs', exist_ok=True)

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('é', 'e')).strip('-')

# ---------------- song list ----------------
src = open('tools/youtube_cards.py', encoding='utf-8').read(); i = src.index('SONGS'); st = src.index('[', i); d = 0
for k, ch in enumerate(src[st:]):
    d += ch == '['; d -= ch == ']'
    if d == 0: CARDS = ast.literal_eval(src[st:st + k + 1]); break
card = {t: (s, c) for t, s, c in CARDS}
rows = []
for line in open('README.md', encoding='utf-8').read().split('## YouTube gameplay tracks')[1].split('\n## ')[0].split('\n'):
    if line.startswith('| ') and not line.startswith('| Song') and line.count('|') == 5:
        rows.append([x.strip() for x in line.strip('|').split('|')])
GAME = [('Lobby', 'Drop-In Daily', 'Menus', 'songs/drop-in-daily/Drop-In Daily - Lobby.mp3', 'fnMenu'),
        ('Match', 'Drop-In Daily', 'Questions', 'songs/drop-in-daily/Drop-In Daily - Match.mp3', 'fn'),
        ('Mythic Match (OG style)', 'Drop-In Daily', 'Mythic-only questions', 'songs/drop-in-daily/Drop-In Daily - Mythic Match (OG style).mp3', 'fnOGm'),
        ('Endless Summary (OG lobby style)', 'Drop-In Daily', 'The Endless run summary', 'songs/drop-in-daily/Drop-In Daily - Endless Summary (OG lobby style).mp3', 'fnOG'),
        ('Route', 'Daily Poké Catch', 'Menus', 'songs/daily-poke-catch/Daily Poke Catch - Route (Menus).mp3', 'pkMenu'),
        ('Battle', 'Daily Poké Catch', 'Questions', 'songs/daily-poke-catch/Daily Poke Catch - Battle.mp3', 'pk'),
        ('Mythic Battle', 'Daily Poké Catch', 'Mythic-only questions', 'songs/daily-poke-catch/Daily Poke Catch - Mythic Battle.mp3', 'pkB'),
        ('Town', 'Daily Poké Catch', 'The Endless run summary', 'songs/daily-poke-catch/Daily Poke Catch - Town (Endless Summary).mp3', 'pkTown')]
LOOPJ = json.load(open('loops/music.json'))

# ---------------- tags ----------------
def has(text, *words): return any(w in text for w in words)
def groups_for(t, style, feel):
    s = (style + ' ' + feel).lower(); g = []
    if t.endswith('Breaks') or 'breakcore' in s: g.append('Breakcore')
    if t in ('First Bloom', 'Heatwave Arcade', 'Amber Leaves', 'Frostline', 'Window Seat', 'Lightning Over the City', 'Lantern in the Fog', 'Kite Season'): g.append('Seasons & weather')
    if 'pokémon' in s or t == 'Coastal Route': g.append('Pokémon-style')
    if 'sonic' in s: g.append('Sonic-style')
    if 'nsmb' in s: g.append('Mario-style worlds')
    if 'bts' in s and 'era' in s: g.append('BTS album eras')
    if 'solo style' in s: g.append('BTS solo styles')
    if has(s, 'bts', 'txt', 'cortis', 'fujii kaze', 'inabakumori', 'anime', 'j-pop', 'j-rock', 'solo style'): g.append('K-pop & J-pop styles')
    if has(s, 'undertale', 'wii', 'winter games', 'fortnite', 'halo', 'pokémon', 'sonic', 'nsmb', 'game boy', 'gba', '16-bit') or t == 'Coastal Route': g.append('Video game styles')
    if has(s, 'bgm', 'menu') or t in ('Lobby Loop',): g.append('Background music')
    if has(s, 'hyperpop', 'nightcore', 'glitchcore'): g.append('Hyperpop')
    if has(s, 'bengali', 'bangladesh', 'flutes', 'east asian', 'amapiano', 'reggae', 'gugak', 'korean traditional', 'koto', 'tabla'): g.append('World music')
    if has(s, 'orchestral', 'waltz', 'orchestra', 'choir'): g.append('Orchestral & cinematic')
    if has(s, 'math'): g.append('Math')
    if t in ('Oops Again', 'Tiptoe Heist', 'Final Zone Countdown', 'Comeback Rising', 'See You Next Drop'): g.append('Gameplay moments')
    return g
def genres_for(style, feel):
    s = (style + ' ' + feel).lower(); g = []
    rules = [('Breakcore', ('breakcore',)), ('Drum & bass', ('drum & bass', 'dnb')), ('Hyperpop', ('hyperpop', 'nightcore', 'glitchcore')),
             ('Pop', ('pop', 'disco', 'city pop')), ('Rock & metal', ('rock', 'metal', 'punk', 'guitar solo')), ('Hip-hop & trap', ('hip-hop', 'boom-bap', 'trap', 'rap', 'phonk', 'drill')),
             ('Electronic & dance', ('edm', 'house', 'eurobeat', 'synthwave', 'dubstep', 'future bass', 'club', 'jersey', 'gqom', 'moombahton', 'trance', 'garage')),
             ('Jazz, funk & soul', ('jazz', 'funk', 'soul', 'swing', 'bossa', 'r&b', 'ska')), ('Orchestral & cinematic', ('orchestral', 'waltz', 'orchestra', 'choir', 'fanfare', 'march')),
             ('Lo-fi & chill', ('lo-fi', 'chill', 'calm', 'menu', 'mellow')), ('World & folk', ('folk', 'bengali', 'world', 'flute', 'reggae', 'amapiano', 'bluegrass', 'koto', 'gugak', 'spanish', 'tropical', 'steel drum', 'accordion')),
             ('Chiptune & retro', ('game boy', 'gba', '16-bit', 'ds quality', 'crunched', 'chip')), ('Piano', ('piano',))]
    for name, words in rules:
        if any(w in s for w in words): g.append(name)
    return g or ['Other']
MOODS = [('Hype', ('hype', 'intense', 'aggressive', 'fast', 'chase', 'fights', 'endgame', 'boss', 'speedy', 'rage', 'kill')),
         ('Chill', ('chill', 'calm', 'relaxed', 'lo-fi', 'commentary', 'menus', 'looting', 'exploring', 'mellow', 'late-night')),
         ('Emotional', ('emotional', 'sad', 'story', 'reflective', 'recap', 'losses', 'comeback')),
         ('Happy', ('happy', 'upbeat', 'feel-good', 'bright', 'wins', 'fun', 'optimistic')),
         ('Funny', ('funny', 'chaotic', 'goofy')),
         ('Spooky & sneaky', ('spooky', 'stealth', 'sneaky', 'mysterious', 'night')),
         ('Epic', ('epic', 'big moments', 'final circle', 'boss', 'heroic', 'tournament', 'dramatic'))]
def moods_for(feel, good):
    s = (feel + ' ' + good).lower(); return [m for m, w in MOODS if any(x in s for x in w)]

# ---------------- audio analysis ----------------
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)
NFFT, HOP = 4096, 512
fr = np.fft.rfftfreq(NFFT, 1 / SR)
EDGES = np.geomspace(40, 10000, 17)
BANDS = [(fr >= EDGES[k]) & (fr < EDGES[k + 1]) for k in range(16)]
pc = np.full(len(fr), -1); ok = (fr > 60) & (fr < 4000); pc[ok] = np.round(12 * np.log2(fr[ok] / 440.) + 69).astype(int) % 12
def analyse(x, bpm, beats_per_bar=4, game_L=None):
    _, _, Z = ss.stft(x, SR, nperseg=NFFT, noverlap=NFFT - HOP, boundary=None); P = np.abs(Z) ** 2
    band = np.log10(np.array([P[b].sum(0) for b in BANDS]) + 1e-10)        # 16 x frames
    chroma = np.array([P[pc == k].sum(0) for k in range(12)]); chroma /= chroma.sum(0) + 1e-12
    flux = np.maximum(np.diff(np.log10(P + 1e-10), axis=1), 0).mean(0); flux = np.concatenate([[0], flux])
    rms = np.sqrt((P.sum(0) + 1e-12)); T = len(x) / SR; nfr = band.shape[1]; tfr = np.arange(nfr) * HOP / SR
    body = (tfr > 3) & (tfr < T - 5); body = body if body.any() else np.ones(nfr, bool)
    cen = (fr[:, None] * P).sum(0) / (P.sum(0) + 1e-12)
    loud = 20 * np.log10(rms + 1e-9)
    timbre = np.concatenate([band[:, body].mean(1) - band[:, body].mean(), band[:, body].std(1), [np.log(cen[body].mean()), flux[body].mean() * 10, loud[body].std() / 10]])
    if not bpm:                                    # estimate tempo from the onset envelope
        o = flux - flux.mean(); ac = np.correlate(o, o, 'full')[len(o) - 1:]; lags = np.arange(len(ac)) * HOP / SR
        sel = (lags > 60 / 190) & (lags < 60 / 70); bpm = 60 / lags[sel][np.argmax(ac[sel])]
    # energy shape: loudness in 16 slices of the song
    seg = np.array_split(rms, 16); arc = np.array([s.mean() for s in seg]); arc = arc / (arc.max() + 1e-12)
    # ---- loop: two bar lines where the next few bars sound the same ----
    if game_L:
        a, b = game_L, 2 * game_L
    else:
        bar = beats_per_bar * 60 / bpm; nb = int(T / bar)
        F = np.vstack([chroma * 3, (band - band.mean(1, keepdims=True)) / (band.std(1, keepdims=True) + 1e-9)])
        def feat(k, w=2):
            m = (tfr >= k * bar) & (tfr < (k + w) * bar)
            if m.sum() < 4: return None
            v = np.concatenate([c.mean(1) for c in np.array_split(F[:, m], 8, axis=1)]); v = v - v.mean()   # 8 slices in order, so the melody's shape counts
            return v / (np.linalg.norm(v) + 1e-9)
        last = int((T - 6) / bar) - 2
        fv = {k: feat(k) for k in range(0, max(last, 1))}
        best = []
        for a_ in range(1, last):
            if fv.get(a_) is None: continue
            for b_ in range(a_ + 8, last):
                if fv.get(b_) is None: continue
                best.append((float(fv[a_] @ fv[b_]), a_, b_))
        if best:
            top = max(s for s, _, _ in best); good = [(b_ - a_, -a_, s, a_, b_) for s, a_, b_ in best if s >= top - .07]   # the longest loop that is still nearly as seamless as the best one
            _, _, sim, ka, kb = max(good); a, b = ka * bar, kb * bar
        else: a, b = 0, T - 2; sim = 0
        # fine-tune the jump by a few milliseconds so the waveforms line up
        w = int(.05 * SR); ia, ib = int(a * SR), int(b * SR); R = int(.012 * SR)
        if ib + w + R < len(x):
            ref = x[ia:ia + w]; scores = [np.dot(ref, x[ib + d:ib + d + w]) for d in range(-R, R)]; b = (ib + int(np.argmax(scores)) - R) / SR
    return dict(timbre=timbre, arc=arc, loop=[round(a, 4), round(b, 4)], bpm=bpm, dur=T)

songs = []
for n, (t, tempo, feel, good) in enumerate(rows):
    style, colors = card.get(t, ('', ('#222', '#555', '#fff', '#111', '#fff')))
    style = style.split('·', 1)[1].strip() if '·' in style else style
    m = re.match(r'(\d+) BPM', tempo); bpm = int(m.group(1)) if m else None
    songs.append(dict(id=slug(t), title=t, file=f'songs/youtube/{t}.mp3', video=f'videos/YouTube - {t}.mp4', card=f'cards/YouTube - {t}.png',
                      tempo=bpm, style=style, feel=feel, good=good, colors=list(colors), order=n + 9,
                      groups=groups_for(t, style, feel), genres=genres_for(style, feel), moods=moods_for(feel, good), _bar=3 if t == 'Coral Waltz' else 4))
for n, (t, game, during, f, key) in enumerate(GAME):
    fn = os.path.basename(f)[:-4]
    songs.append(dict(id=slug(game + ' ' + t), title=t, file=f, video=f'videos/{fn}.mp4', card=f'cards/{fn}.png', tempo=None, style=f'{game} theme',
                      feel=f'Plays during: {during}', good='Menus, quizzes, background', colors=['#140b2a', '#4a2a8f', '#ffd23f', '#0a0515', '#ffffff'],
                      order=n, groups=['Game themes (' + game + ')'], genres=['Chiptune & retro'], moods=['Chill' if 'Menu' in during or 'summary' in during else 'Hype'],
                      _bar=4, _gameL=LOOPJ[key]['L']))

for k, s in enumerate(songs):
    x = load(s['file']); r = analyse(x, s['tempo'], s.pop('_bar'), s.pop('_gameL', None))
    s.update(duration=round(r['dur'], 1), loop=r['loop'], _timbre=r['timbre'], _arc=r['arc'])
    if not s['tempo']: s['tempo_est'] = round(r['bpm'])
    s['energy'] = round(float(np.mean(r['arc'])), 3)
    th = f"site/thumbs/{s['id']}.jpg"
    if not os.path.exists(th) and os.path.exists(s['card']):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', s['card'], '-vf', 'scale=480:-2', '-q:v', '5', th])
    s['thumb'] = th if os.path.exists(th) else None
    print(f"{k + 1}/{len(songs)} {s['title']}: loop {s['loop'][0]:.1f}-{s['loop'][1]:.1f}s of {s['duration']}s", flush=True)

# ---------------- relations ----------------
Tm = np.array([s['_timbre'] for s in songs]); Tm = (Tm - Tm.mean(0)) / (Tm.std(0) + 1e-9)
tempo = np.array([np.log2(s.get('tempo') or s.get('tempo_est') or 120) for s in songs]); tempo = (tempo - tempo.mean()) / tempo.std()
V = np.hstack([Tm, tempo[:, None] * 1.5]); V /= np.linalg.norm(V, axis=1, keepdims=True)
A = np.array([s['_arc'] for s in songs]); A = A - A.mean(1, keepdims=True); A /= np.linalg.norm(A, axis=1, keepdims=True) + 1e-9
def jac(a, b): a, b = set(a), set(b); return len(a & b) / max(1, len(a | b))
TAG = np.array([[jac(p['genres'] + p['moods'], q['genres'] + q['moods']) for q in songs] for p in songs])
SIM, SHAPE = .6 * (V @ V.T) + .4 * TAG, A @ A.T   # 'sounds similar' = how it sounds (60%) + shared genre/mood tags (40%)
for i, s in enumerate(songs):
    s['similar'] = [songs[j]['id'] for j in np.argsort(-SIM[i]) if j != i][:6]
    s['shape'] = [songs[j]['id'] for j in np.argsort(-SHAPE[i]) if j != i][:6]
    base = s['title'].split()[0]
    s['versions'] = [o['id'] for o in songs if o is not s and o['title'].split()[0] == base and (o['title'].endswith('Breaks') != s['title'].endswith('Breaks'))]
    s['arc'] = [round(float(v), 2) for v in s['_arc']]
for s in songs: s.pop('_timbre'); s.pop('_arc')
songs.sort(key=lambda s: s['order'])
json.dump(dict(count=len(songs), songs=songs), open('site/songs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('wrote site/songs.json with', len(songs), 'songs')
