# Coded Music

Original music and sound effects written entirely as code, made for **[Drop-In Daily](https://taziz05.github.io/drop-in-daily/)** and **[Daily Poké Catch](https://taziz05.github.io/daily-poke-catch/)**.

Every note is written out as instructions (which note, which kind of wave, how long) and played by the browser's Web Audio API. No samples, no recordings of anything else, and no AI audio generators: the audio files here are just recordings of that code playing.

Made by TAziz322 · Coded with Claude (Opus 5.5) by Anthropic

## What's here

| Folder | What it is |
|---|---|
| `songs/` | About 2-minute versions of every song with a fade-out (320 kbps MP3). Good for videos. |
| `videos/` | The same songs as 1080p videos with a title card, ready to upload to YouTube. |
| `cards/` | The title card images. |
| `loops/` | One seamless loop of each song (see `loops/music.json` for loop lengths). |
| `code/` | The songs themselves: `helpers.js` (the little synthesizers) and one file per song in `code/songs/`. |
| `tools/` | `record.html` + `record.py` record the code into WAVs; `make-files.py` builds the loops and 2-minute versions; `cards.py` draws the title cards. |
| `sound-test.html` | Open in a browser to hear every sound effect and song live from code. |

## The songs

| Song | Game | Plays during |
|---|---|---|
| Lobby | Drop-In Daily | Menus |
| Match | Drop-In Daily | Questions |
| Mythic Match (OG style) | Drop-In Daily | Mythic-only questions |
| Endless Summary (OG lobby style) | Drop-In Daily | The Endless run summary |
| Route | Daily Poké Catch | Menus |
| Battle | Daily Poké Catch | Questions |
| Mythic Battle | Daily Poké Catch | Mythic-only questions |
| Town | Daily Poké Catch | The Endless run summary |

## YouTube gameplay tracks

Background music for TAziz322's Fortnite gameplay videos, in `songs/youtube/` (320 kbps MP3, each about 2 to 2.5 minutes with a fade-out). These are made with a small Python synthesizer instead of the browser: `code/python/engine.py` holds the instruments and `code/python/songs.py` holds the songs. Each one also has a 1080p video with a title card in `videos/` (`YouTube - <song>.mp4`) and its card in `cards/`, made by `tools/youtube_cards.py`.

| Song | Tempo | Feel | Good for |
|---|---|---|---|
| Victory Rush | 128 BPM | Upbeat, heroic brass | Wins, highlights, montages |
| Storm Closing | 140 BPM | Tense, minor key, driving | Late-game fights |
| Lobby Loop | 102 BPM | Chill electric-piano groove | Intros, looting, commentary |
| Overclocked | 174 BPM | Drum & bass: fast breakbeat, rolling reese bass | Fast-paced fights, edits with lots of cuts |
| Nobody's Looking | 180 BPM | Breakcore: sad piano over chopped, stuttering breakbeats | Clutch moments, emotional edits, losses |
| Static Weather | 146 BPM | Vocaloid-style J-rock (in the style of inabakumori): chorused guitars, singing synth lead | Chill wins, recap edits |
| Lantern Theory | 150 BPM | Instrumental jazz / math rock (in the style of Nouvelle Story): 7/8 tapped guitar, sax | Creative builds, highlight reels |
| Channel Plaza | 116 BPM | Bossa nova with e-piano and marimba (in the style of Wii menu music) | Menus, chill commentary |
| Frosty Podium | 150 BPM | Winter sports fanfare with sleigh bells, crunched to DS quality (in the style of Mario & Sonic Winter Games DS) | Wins, upbeat edits |
| Coastal Route | 132 BPM | Route music with a GBA trumpet lead, crunched to GBA quality (in the style of Pokémon Ruby/Sapphire) | Exploring, looting |
| Homebase Rising | 112 BPM | Orchestral adventure: string ostinato, horns, choir (in the style of Fortnite Save the World) | Big moments, intros |
| Determined Steps | 120 BPM | Solo piano (in the style of Undertale) | Calm moments, story edits |
| Ringworld Vigil | 72 → 120 BPM | Monk-style choir chant, then driving strings, guitars and drums (in the style of Halo) | Epic intros, final circles |
| Boundless Run | 155 BPM | Upbeat rock with crunchy guitars and a key change (in the style of Sonic Unleashed's "Endless Possibility") | Speedy plays, montages |

```
pip install numpy scipy
cd code/python && python songs.py 1   # 1 = Victory Rush, 2 = Storm Closing, 3 = Lobby Loop, 4 = Overclocked, 5 = Nobody's Looking (needs ffmpeg)
python songs2.py 6  # 6 = Static Weather, 7 = Lantern Theory  (instruments in instruments2.py)
python songs3.py 9  # 8 = Determined Steps, 9 = Channel Plaza, 10 = Frosty Podium, 11 = Coastal Route, 12 = Homebase Rising
python songs4.py 13 # 13 = Boundless Run (13c = clean-guitar version), 14 = Ringworld Vigil
```

## Re-recording

```
pip install playwright numpy
python tools/record.py      # needs Google Chrome; writes build/*-raw.wav
python tools/make-files.py  # needs ffmpeg; rebuilds loops/ and songs/
```

Unofficial fan projects. Fortnite and Pokémon names belong to their owners; the music is original.
