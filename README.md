# Coded Music

Original music and sound effects written entirely as code, made for **[Drop-In Daily](https://taziz05.github.io/drop-in-daily/)** and **[Daily Poké Catch](https://taziz05.github.io/daily-poke-catch/)**.

Every note is written out as instructions (which note, which kind of wave, how long) and played by the browser's Web Audio API. No samples, no recordings of anything else, and no AI audio generators: the audio files here are just recordings of that code playing.

Made by TAziz322 · Coded with Claude (Opus 5.5) by Anthropic

## Website

`index.html` is a song browser for phones and computers (it becomes the site when the repo is published with GitHub Pages). It has:

- search, plus filters for genre, mood, tempo and length, and group chips (Pokémon-style, Sonic-style, Mario-style worlds, BTS eras, breakcore, and more)
- sorting by newest, title, tempo, length, energy or group, plus **Similar sound together** (songs grouped into sound families by their audio) and **Similar structure together** (songs with the same build-up/drop/energy shape next to each other)
- **Credit reminders**: every song page has a ready-to-copy credit line, and downloading an MP3, opening a video or making an extended version shows a reminder to give credit (once per song per visit)
- visitor counts with [GoatCounter](https://www.goatcounter.com/) (no cookies): page views plus play, download and Loop Lab events, on both the site and Loop Lab
- **Favorites**: tap ☆ on any song, then the ★ Favorites chip (saved in your browser)
- for every song: other versions (like the breakcore version), songs that sound similar, songs with a similar structure, and more from the same group
- seamless loop playback with a **loop picker**: the best match, up to three other loop options, or pick your own start and end (snapped to bar lines); your choice is remembered and used for loop playback and extended versions
- **Extended versions**: pick 2 to 20 minutes and your browser builds an MP3 or WAV that plays the start, repeats the seamless loop, then plays the real ending
- four themes (Storm, Neon, Daylight, Game Boy), share links for each song, and a link to Loop Lab

Every song page also has **Open in Loop Lab** and **Copy Loop Lab code**: `python tools/to_looplab.py` turns the Python songs into simplified Loop Lab song code (`site/looplab/`), and `python tools/transcribe.py` does the same for the early hand-coded songs and the browser game songs by writing down every note and drum hit while their code runs, so all songs have a Loop Lab version. Loop Lab can import that code (paste it, open the file, drag it onto the page, or open `loop-lab/?song=...`), change it and export it again. Both pages have app icons (add them to your home screen) and coded button sounds you can switch off.

`python tools/build_site.py` rebuilds `site/songs.json` and `site/thumbs/` after songs are added. It reads this README's song table and the title-card list, then listens to each MP3 to find its loop points, what it sounds like and its energy shape.

## What's here

| Folder | What it is |
|---|---|
| `songs/` | Every song as a 320 kbps MP3: the 8 game songs (about 2 minutes each, with a fade-out) and the 148 YouTube tracks in `songs/youtube/` (1 to 2½ minutes each). |
| `videos/` | The same songs as 1080p videos with a title card, ready to upload to YouTube. |
| `cards/` | The title card images. |
| `loops/` | One seamless loop of each song (see `loops/music.json` for loop lengths). |
| `code/` | The songs themselves: `helpers.js` (the little synthesizers) and one file per song in `code/songs/`. |
| `tools/` | `record.html` + `record.py` record the code into WAVs; `make-files.py` builds the loops and 2-minute versions; `cards.py` draws the title cards. |
| `loop-lab/` | Loop Lab, the in-browser song maker, plus its guide and build tools. |
| `sound-test.html` | Open in a browser to hear every sound effect and song live from code. |

## The songs

8 game songs, plus 148 YouTube gameplay tracks (below): 156 songs in all.

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

## Loop Lab

`loop-lab/index.html` is a song maker that runs in the browser: build songs from sections with chords, a melody, drums and sound effects (built-in coded effects or your own uploads), load TAziz322's songs and tweak them, and save songs as code. See [`loop-lab/GUIDE.md`](loop-lab/GUIDE.md) for how to use it. `loop-lab/tools/make_presets.py` rebuilds the page from `template.html` with the built-in songs.

## YouTube gameplay tracks (148 songs)

Background music for TAziz322's Fortnite gameplay videos, in `songs/youtube/` (320 kbps MP3). They run from 1 to about 2½ minutes; most are around 1½ minutes. These are made with a small Python synthesizer instead of the browser: `code/python/engine.py` holds the instruments, and the songs live in the other files in `code/python/` (see the commands below). Each one also has a 1080p video with a title card in `videos/` (`YouTube - <song>.mp4`) and its card in `cards/`, made by `tools/youtube_cards.py`.

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
| Morning Over the Valley | 90 BPM (3/4) | Cinematic orchestral waltz: harp, strings, woodwinds, horns, timpani | Story edits, calm intros, endings |
| Shattered Overture | 90 → 180 BPM | Starts orchestral, switches to steady breakcore with the orchestra on top, ends back with the orchestra in D major | Montages that build, comeback clips |
| Paper Sky | 170 BPM | Bright, dreamy steady breakcore: shimmering guitars, glockenspiel, 808, half-time breakdown | Happy montages, wins |
| Last Light | 174 BPM | Sad steady breakcore: piano and strings, dusty breaks | Emotional edits, losses |
| First Bloom | 172 BPM | Spring steady breakcore: picked guitars, flute, birdsong | Fresh starts, chill wins |
| Heatwave Arcade | 180 BPM | Summer steady breakcore: bright synths, 808, cicadas | Hype montages |
| Amber Leaves | 168 BPM | Autumn lo-fi breakcore: e-piano, vibraphone, rustling leaves | Relaxed gameplay |
| Frostline | 176 BPM | Winter steady breakcore: harp, glockenspiel, sleigh bells, wind | Winter seasons, festive clips |
| Window Seat | 165 BPM | Rainy lo-fi breakcore: mellow keys, rain on the window | Late-night sessions |
| Lightning Over the City | 185 BPM | Thunderstorm breakcore: heavy breaks, reese bass, thunder | Intense endgames |
| Lantern in the Fog | 160 BPM | Foggy lo-fi breakcore: muffled breaks, foghorn, drone | Mysterious or stealthy moments |
| Kite Season | 178 BPM | Windy steady breakcore: airy guitars, flute, gusts | Mobility plays, gliding |
| Golden Hour Groove | 114 BPM | Disco-pop with brass hooks and strings (in the style of BTS) | Feel-good highlights |
| Blue Spark Runaway | 160 BPM | Emo pop-punk with dreamy synths (in the style of TXT) | Clutches, comebacks |
| Off the Lines | 150 BPM | Hype rage trap: distorted synth riff, heavy 808, hi-hat rolls, beat switch (in the style of CORTIS) | Hype plays, kill montages |
| Breeze in the Alley | 98 BPM | Piano-led J-pop soul with jazzy chords, gospel organ and trap touches (in the style of Fujii Kaze) | Chill highlights, story edits |
| Golden Hour Breaks | 172 BPM | Steady breakcore with funk guitar and brass (BTS style) | Upbeat montages |
| Blue Spark Breaks | 176 BPM | Steady breakcore with dreamy synths and crunchy lead guitar (TXT style) | Emotional clutches |
| Off the Lines Breaks | 170 BPM | Steady breakcore with a rage-synth riff and 808 (CORTIS style) | Hype edits |
| Lanterns and Thunder Drums | 168 BPM | East Asian-themed steady breakcore: koto-style plucks, bamboo-flute lead, taiko, gong | Dramatic moments |
| Breeze Breaks | 172 BPM | Steady breakcore with jazzy piano and a singing synth (Fujii Kaze style) | Smooth highlight reels |
| Schoolyard Riot | 96 BPM | Hard 90s boom-bap, horn stabs, scratches (BTS School trilogy era) | Hype intros |
| Dark and Wild Run | 140 BPM | Rock-rap with crunchy guitars (BTS Dark & Wild era) | Aggressive plays |
| Youth in Bloom | 128 BPM | Emotional synth-pop with piano (BTS The Most Beautiful Moment in Life era) | Montages |
| Velvet Wings | 93 BPM | Dark moombahton, pan flute, strings (BTS Wings era) | Moody clips |
| Double Helix | 128 BPM | Bright pop with acoustic guitar, whistle and future-bass chorus (BTS Love Yourself: Her era) | Happy highlights |
| Fragile Mask | 78 BPM | Emo hip-hop with dark guitar and trap drums (BTS Love Yourself: Tear era) | Emotional edits |
| Eolssu Groove | 126 BPM | Korean traditional instruments over gqom/house (BTS Love Yourself: Answer era) | Big moments |
| Light Up the Persona | 120 BPM | Bright funk-pop (BTS Map of the Soul: Persona era) | Feel-good edits |
| March of Seven | 106 BPM | Marching drums, orchestra and 808 (BTS Map of the Soul: 7 era) | Epic intros |
| Life Goes Slow | 82 BPM | Warm acoustic lo-fi pop (BTS BE era) | Chill streams |
| Yet to Bloom | 90 BPM | Nostalgic mellow hip-hop (BTS Proof era) | Recaps |
| Arirang Dawn | 94 BPM | Temple bell, gayageum, 808, vocoder, guitar surge (BTS ARIRANG era) | Comebacks |
| Riverbank Evening | 96 BPM | Bengali Baul-folk style: dotara, ektara, harmonium, bansuri, tabla, tihai ending | Calm intros, story edits |
| Monsoon Breaks | 172 BPM | Steady breakcore with tabla, harmonium and bansuri | Upbeat montages |
| Sky-Piercing Promise | 176 BPM | Fast J-rock anime-opening style: piano runs, strings, crunchy guitars, last chorus up a key | Intros, hype montages |
| Sky-Piercing Breaks | 180 BPM | Steady breakcore with the anime hook on strings and crunch guitar | Montages |
| Arcade Heartbreak 2005 | 150 BPM | Y2K pop-punk with nu-metal chugs and glitchy synths (in the style of South Arcade) | Hype plays, funny clips |
| Iron Storm Rising | 168 BPM | Heavy metal: double kick, chugs, tremolo picking, guitar solo | Intense endgames |
| Iron Storm Breaks | 176 BPM | Steady breakcore with metal guitars and reese bass | Aggressive montages |
| Respawn Lounge | 84 BPM | Laid-back lo-fi: e-piano, guitar, boom-bap | Commentary, chill streams |
| Final Circle | 140 BPM | Dark trap-EDM with heavy 808 and synth drops | Endgames, clutch moments |
| Pallet Path | 132 BPM | Route music crunched to Game Boy quality (in the style of Pokémon Gen 1) | Exploring, looting |
| Johto Morning | 128 BPM | Bright Game Boy Color route (in the style of Pokémon Gen 2) | Exploring, chill rotations |
| Snowpoint Trail | 120 BPM | DS-quality route with trumpet and strings (in the style of Pokémon Gen 4) | Winter maps, exploring |
| Island Breeze | 104 BPM | Relaxed tropical route: steel drum, ukulele, jazzy chords (in the style of Pokémon Gen 7) | Chill gameplay |
| Stadium Highlands | 128 BPM | Brass and marching drums with crowd hey chants (in the style of Pokémon Gen 8) | Big wins, tournaments |
| Sunlit Plaza | 132 BPM | Spanish guitar, trumpet and castanets (in the style of Pokémon Gen 9) | Upbeat exploring |
| Emerald Shore Zone | 142 BPM | FM-synth lead and slap bass crunched to 16-bit (in the style of classic Genesis Sonic) | Speedy plays |
| Time Warp Zone | 126 BPM | 90s Japanese house with organ stabs and shouts (in the style of Sonic CD) | Rotations, movement clips |
| Treasure Hunt Flow | 92 BPM | Boom-bap with scratches and horn stabs (in the style of Sonic Adventure 2) | Looting, chill highlights |
| Rush Hour Boost | 152 BPM | Breakbeat jazz-funk with slap bass and shouts (in the style of Sonic Rush) | Fast-paced clips |
| Moonlit Night Stage | 140 BPM | Swinging jazz with sax and walking bass (in the style of Sonic Unleashed night stages) | Stealthy or night clips |
| Starlight Carnival Run | 128 BPM | Bright EDM-pop with bells and future-bass chords (in the style of Sonic Colors) | Happy highlights |
| Lime Green Afterparty | 132 BPM | Abrasive club pop: distorted rave stabs, heavy 808, vocoder hook (in the style of Charli xcx’s Brat era) | Hype edits |
| Red 40 Sugar Rush | 162 BPM | Hyperpop: chipmunk vocal chops, glitchy synths, distorted 808, cartoon sound effects | Chaotic or funny clips |
| Padma to Kyoto | 100 BPM | Bangladesh meets Japan: koto, harmonium, ektara, tabla and taiko, bansuri and shakuhachi trading phrases | Calm intros, story edits |
| Arcade Heartbreak Breaks | 172 BPM | Steady breakcore with the pop-punk hook; ends with a tape stop | Hype montages |
| Boulevard Café | 116 BPM | Accordion over jazzy piano and walking bass (in the style of Pokémon Gen 6) | Chill exploring |
| Highway Escape | 160 BPM | Fast punk rock with strings and pads behind the guitars (in the style of Sonic Adventure) | Chases, fast clips |
| Titan Undefeated | 150 BPM | Epic rock boss theme with strings and piano (in the style of Sonic Frontiers) | Boss fights, final circles |
| Winds of the World | 104 BPM | A tour of flutes from different cultures, each with its own instruments and rhythm | Calm intros, travel edits |
| Sugar Cloud Smile | 128 BPM | Happy future bass with bright chords and vocal chops (in the style of Marshmello) | Happy highlights |
| Sugar Cloud Breaks | 172 BPM | Steady breakcore with the future-bass hook; instruments drop out one by one at the end | Montages |
| Lime Green Breaks | 176 BPM | Steady breakcore with rave stabs and 808; winds down and stops | Hype edits |
| Padma to Kyoto Breaks | 172 BPM | Steady breakcore with tabla, taiko and flutes; ends with a traditional tihai | Upbeat montages |
| Grassland Hop | 150 BPM | Bouncy grassland world with steel drum, stride piano, bongos and "bah!" hits (in the style of New Super Mario Bros. Wii) | Fun, lighthearted clips |
| Desert Dunes | 120 BPM | Desert world with oud, oboe and darbuka | Desert maps, exploring |
| Snowcap Slide | 112 BPM | Snow world with celesta, pizzicato strings and sleigh bells | Winter maps |
| Coconut Cove | 124 BPM | Beach world: steel drum, ukulele, congas | Chill gameplay |
| Mushroom Woods | 116 BPM | Forest world with clarinet, marimba and pizzicato | Sneaky or funny clips |
| Cliffside Climb | 132 BPM | Heroic mountain world with brass and strings | Climbs, comebacks |
| Cloudtop Athletic | 160 BPM | Light, bouncy sky world with flute, strings and tuba | Movement clips |
| Magma Fortress | 132 BPM | Lava world: organ, choir, brass and timpani | Boss fights, endgames |
| Starry Road | 140 BPM | Sparkly star world with celesta and bright synths | Big wins |
| Pipe Cavern | 120 BPM | Underground: slap bass, xylophone and "bah!" hits | Sneaky clips |
| Coral Waltz | 150 BPM | Underwater waltz in 3/4 with harp, strings, flute and celesta | Calm moments, water maps |
| Haunted Manor | 96 BPM | Spooky swing with theremin and harpsichord | Spooky or funny clips |
| Shellfire Castle | 112 BPM | Castle theme with organ, choir and timpani | Final circles, boss fights |
| Glitter Overload | 136 BPM | Bubblegum hyperpop: glossy bell synths, metallic clanks, chipmunk hooks | Funny, chaotic clips |
| Bitcrushed Daydream | 150 BPM | Glitchcore: crushed, stuttering synths over emo guitar verses | Montages, edits |
| Static Tears | 140 BPM | Sad acoustic verses that blow up into a huge distorted chorus | Emotional edits |
| Nightcore Rush | 172 BPM | Nightcore: sped-up trance energy, gated supersaws, four on the floor | Hype montages |
| Menu Drift | 100 BPM | Calm, steady background music with soft bells and pads | Commentary, menus, chill streams |
| Skyscraper Sprint | 150 BPM | Fast city route with synth lead and trumpet (in the style of Pokémon Gen 5) | Fast-paced clips |
| Red 40 Breaks | 178 BPM | Steady breakcore with glitches, chipmunk chops and cartoon sound effects | Chaotic montages |
| Aqua Tomorrow | 116 BPM | Optimistic late-2000s pop-rock with glossy bells and bubbles (Meet the Robinsons / Frutiger Aero style) | Happy highlights, intros |
| Aqua Tomorrow Breaks | 172 BPM | Steady breakcore with plucks, bells and bubbles | Upbeat montages |
| Pixel Heart DnB | 174 BPM | Hyper drum & bass with chipmunk hooks and supersaw chords | Fast montages |
| Midnight Drift | 130 BPM | Drift phonk: cowbell melody, distorted 808, triplet hats, dark shouts | Edits, montages, clutch plays |
| Neon Horizon | 104 BPM | Synthwave: gated snares, 16th arpeggios, big 80s saw lead | Driving, retro edits |
| Turbo Corner | 156 BPM | Eurobeat: racing lead, supersaw stabs, offbeat octave bass | Fast rotations, chases |
| Checkerboard Skank | 168 BPM | Ska: offbeat guitar, horn section, fast walking bass | Funny, upbeat clips |
| Island Time | 76 BPM | Reggae: one-drop drums, skank and organ bubble, melodica-style lead | Chill gameplay |
| Log Drum Sunset | 112 BPM | Amapiano: log drum bass, shakers, jazzy piano and sax | Chill, groovy clips |
| Holler Hoedown | 150 BPM | Bluegrass: banjo rolls, fiddle, boom-chuck guitar | Funny clips, farming maps |
| Tokyo Sunset Drive | 112 BPM | City pop: Rhodes chords, slap bass, funky guitar, brass | Chill highlights |
| Squeak Sprint | 140 BPM | Jersey club: bouncing kicks, bed squeaks, vocal chops | Hype edits |
| Indigo Fields | 86 BPM | Warm alt-folk hip-hop with acoustic guitar and muted trumpet (in the style of RM’s solo work) | Chill, reflective clips |
| Starlit Orbit | 126 BPM | Anthemic pop-rock with driving piano and a soaring chorus (in the style of Jin’s solo work) | Big wins, highlights |
| Street Neuron | 100 BPM | Old-school funky hip-hop with horns and scratches; ends with a tape stop (in the style of j-hope’s solo work) | Dance emotes, upbeat clips |
| Velvet Layover | 76 BPM | Late-night jazzy R&B with Rhodes and muted trumpet (in the style of V’s solo work) | Chill streams, night clips |
| Infinite Series | 120 BPM | A song built from math: pi and e as melodies, Fibonacci bass, Euclidean drums, prime-number bells, a Zeno ending | Smart plays, building, puzzles |
| Level Up Rush | 124 BPM | Upbeat house-pop with plucks and a future-bass chorus | Intros, upbeat rotations |
| Royal Procession | 102 BPM | Hard hip-hop over haegeum, gayageum, janggu and a royal-procession horn (in the style of SUGA / Agust D) | Hype plays, boss moments |
| Oops Again | 150 BPM | Goofy polka with tuba, clarinet, xylophone and slide whistles; ends with a sad wah-wah | Funny fails, bloopers |
| Tiptoe Heist | 104 BPM | Tiptoe jazz with walking bass, pizzicato and finger snaps | Sneaky plays, stealth |
| Final Zone Countdown | 120 BPM | Ticking clock and low strings building through trailer brass hits to a climax | Clutch final circles, intense endgames |
| See You Next Drop | 120 BPM | Short, upbeat funky piece for the end of a video | End screens, subscribe moments |
| Midnight Mirage | 118 BPM | Glossy 80s synth-pop with a falsetto lead (in the style of Jimin’s solo work) | Smooth highlights, night clips |
| Gold Rush Garage | 126 BPM | Sleek UK-garage pop with funky guitar; ends on vocal chops (in the style of Jung Kook’s solo work) | Upbeat highlights |
| Breakcore Squared | 186 BPM | Two breakbeats at once with steady 32nd-note rolls; the breaks go solo, then the piano ends it | Intense montages |
| Comeback Rising | 128 BPM | Starts as sad piano and builds into a triumphant orchestral chorus with a key change | Comebacks, emotional wins |
| Bass Quake | 140 BPM | Dubstep: build-ups, then half-time drops with a wobble bass and a pluck melody | Hype edits, montages |
| Infinite Series Breaks | 174 BPM | Steady breakcore with pi and e as melodies, prime-number bells and a Zeno ending | Smart plays, montages |
| Breakcore Cubed | 190 BPM | Three breakbeats at once, each in its own range; the layers leave one at a time at the end | Intense montages |
| Golazo Anthem | 128 BPM | Samba drums, stadium chants and brass; ends with three final whistles and a roaring crowd | Soccer clips, wins |
| Full Court Press | 94 BPM | Hip-hop with ball bounces and sneaker squeaks; ends on a buzzer beater | Highlights, trick shots |
| Fourth and Goal | 112 BPM | Marching drumline and fight-song brass with hey chants | Big plays, intros |
| Seventh Inning Swing | 120 BPM | Swinging stadium organ with the charge riff, bat cracks and crowd claps | Fun, laid-back clips |
| Ice Time | 140 BPM | Rock and stadium organ with skate swooshes; ends with a goal horn | Hype plays |
| Beach Spike | 116 BPM | Tropical house with steel drum and ukulele; ends with a spike and a whistle | Chill highlights |
| Powder Run | 132 BPM | Racing winter eurobeat with sleigh bells and ski swooshes | Winter maps, fast clips |
| Shuttle Rally | 150 BPM | Quick, bright rally with light shuttle hits panning left and right | Quick clips |
| Huck It | 160 BPM | Upbeat indie-punk with ukulele and flying-disc swooshes | Upbeat highlights |
| Stride 176 | 176 BPM | Drum & bass at a running pace, a footstep on every beat; ends with a sprint finish | Running, fast montages |
| Easy Pace | 160 BPM | Light acoustic pop at a jogging pace, a footstep on every beat | Chill movement clips |
| Fourier Rise | 110 BPM | The lead is built from sine waves, adding harmonics until it is a square wave, then taking them away | Building, smart plays |
| Spelled in Notes | 120 BPM | Words turned into melodies, one note per letter (CODED MUSIC, TAZIZ322, GG, VICTORY ROYALE) | Intros, channel moments |
| Match Point | 118 BPM | Bright funk with ball hits bouncing left and right; ends on a final point and applause | Rallies, chill highlights |
| Sunday Stroll | 112 BPM | Easygoing ukulele pop with soft footsteps on the beat | Relaxed clips, exploring |
| Collatz Climb | 128 BPM | The melody follows the Collatz sequence from 27 as it climbs and falls; it ends on 4, 2, 1 echoing away | Climbing, building moments |
| Sierpinski Steps | 136 BPM | The drums follow Pascal's triangle with the odd numbers marked (a Sierpinski fractal); the melody follows the Thue-Morse sequence | Puzzles, smart plays |
| Rainbow Spectrum | 116 BPM | Each color of the rainbow is a section in the key of its light frequency (red to violet), gliding from one color into the next | Colorful, upbeat clips |

```
pip install numpy scipy
cd code/python && python songs.py 1   # 1 = Victory Rush, 2 = Storm Closing, 3 = Lobby Loop, 4 = Overclocked, 5 = Nobody's Looking (needs ffmpeg)
python songs2.py 6  # 6 = Static Weather, 7 = Lantern Theory  (instruments in instruments2.py)
python songs3.py 9  # 8 = Determined Steps, 9 = Channel Plaza, 10 = Frosty Podium, 11 = Coastal Route, 12 = Homebase Rising
python songs4.py 13 # 13 = Boundless Run (13c = clean-guitar version), 14 = Ringworld Vigil
python songs5.py 15 # 15 = Morning Over the Valley
python songs6.py 16 # 16 = Shattered Overture
python songs7.py 17 # 17 = Paper Sky
python seasons.py all  # the nine steady breakcores (engine: breakcore_engine.py)
python songs9.py bts  # bts = Golden Hour Groove, txt = Blue Spark Runaway
python songs10.py cortis  # Off the Lines (kaze = Breeze in the Alley)
python bts_albums.py all  # the 12 BTS-era songs (engine: popkit.py)
python southasia.py song  # Riverbank Evening (breaks = Monsoon Breaks)
python styles_breakcore.py all  # Golden Hour Breaks, Blue Spark Breaks, Off the Lines Breaks, Lanterns and Thunder Drums, Breeze Breaks
python batch_a.py all  # anime, anime_bc, south, south_bc, metal, metal_bc (Sky-Piercing, Arcade Heartbreak, Iron Storm)
python bgm.py all  # lounge, levelup, menu, final (YouTube / gaming BGM)
python pokemon_gens.py all  # g1 g2 g4 g5 g6 g7 g8 g9 route-style songs (Gen 3 = Coastal Route)
python sonic_styles.py all  # genesis cd adventure hiphop rush jazz colors frontiers
python batch_c.py all  # flutes (Winds of the World), mello, mello_bc, charli, charli_bc
python batch_d.py all  # red, red_bc, aero, aero_bc, bdjp, bdjp_bc
python mario_worlds.py all  # w1-w9 worlds, under, water (Coral Waltz), ghost, castle (styles in newstyles.py)
python hyperpop2.py all  # bubble glitch dnb emo nightcore
python genres.py all  # phonk synthwave dubstep eurobeat ska reggae amapiano bluegrass citypop jersey
python bts_solos.py all  # rm jin suga jhope jimin v jk
python mathsong.py  # Infinite Series: a song built from pi, e, Fibonacci, Euclidean rhythms and more
```

## Re-recording

```
pip install playwright numpy
python tools/record.py      # needs Google Chrome; writes build/*-raw.wav
python tools/make-files.py  # needs ffmpeg; rebuilds loops/ and songs/
```

Unofficial fan projects. Fortnite and Pokémon names belong to their owners; the music is original.
