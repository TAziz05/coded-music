# Loop Lab guide

Loop Lab lets you build whole songs by tapping: sections, chords, a melody, drums and sound effects. Every sound is made in code: no samples, no recordings and no AI audio. Open `index.html` in any modern browser (Chrome, Edge, Safari or Firefox) and it works with no install.

Made by TAziz322 · Coded with Claude (Opus 5.5) by Anthropic

## Quick start (2 minutes)

1. Tap **Play song** to hear the song that's loaded. Tap it again to stop.
2. Under **Songs**, tap another song (like *Channel Plaza*) to load it.
3. In **Sections**, tap the section you want to change, like *Chorus*.
4. Tap **Loop section** so that section repeats while you edit it.
5. Tap cells in the **Melody** grid to add notes, and tap the **Drums** grid to add or remove hits. You hear changes right away.
6. Tap **Make the full song** to turn the whole thing into one audio track you can play.
7. Copy the **Song code** at the bottom to save your song.

## How a song is put together

A song is made of **sections** (intro, verse, chorus and so on). Each section is 1 to 8 bars long and has its own chords, melody, drums, sound effects, chord style and bass pattern.

The **song order** is the list of sections in the order they play. The same section can appear more than once, which is how a chorus repeats without rebuilding it.

Every bar has 16 steps, so each step is a 16th note.

## The screen, top to bottom

### Screen and play buttons

| Part | What it does |
|---|---|
| Song name | Tap the name on the dark screen to rename the song. |
| Lights | One light per bar of the current section. The lit one is the bar playing now. |
| Play song | Plays every section in the song order once, then stops. The view follows along. |
| Loop section | Repeats only the section you're editing. Best while you're making changes. |

### Songs

Tap a song to load it so you can tweak it. **New song** starts you with one empty 4-bar section. Loading a song replaces the one that's open, but **Undo** brings it back.

The built-in songs are versions of TAziz322's coded songs: Victory Rush, Storm Closing, Lobby Loop, Channel Plaza, Frosty Podium, Coastal Route, Determined Steps and Static Weather. Loop Lab's instruments are simpler than the ones used for the full MP3s, so they sound a little lighter.

### Song order

- Tap a section in the strip to select it (and edit it below).
- **Add section** + **Add to end** adds another copy of any section to the end of the song.
- **Move left** / **Move right** moves the selected one.
- **Remove from song** takes it out of the order. The section itself is kept in Sections.

### Sections

| Control | What it does |
|---|---|
| New | Adds an empty 4-bar section to the end of the song. |
| Duplicate | Copies the current section, handy for a "Chorus 2" with small changes. |
| Delete | Deletes the section everywhere it's used. |
| Undo | Steps back through your last 60 changes. |
| Name | Renames the section. |
| Length | 1, 2, 4 or 8 bars. Making it longer repeats the drums to fill the new bars. Making it shorter cuts notes past the end. |
| Chord style | How the chords are played (see the table below). |
| Bass pattern | How the bass follows the chords (see the table below). |

**Chord styles**

| Style | Sounds like |
|---|---|
| Pad (held) | Soft synth strings holding each chord for the whole bar |
| Brass stabs | Short punchy brass hits |
| E-piano bossa | Electric piano in a relaxed bossa nova rhythm |
| Piano broken chords | Piano playing the chord one note at a time |
| Picked guitar | Clean guitar picking through the chord |
| Strummed guitar | Guitar strums in a pop rhythm |
| Synth arpeggio | Fast plucky notes running up and down the chord |
| Chiptune arpeggio | The same, with a retro game sound |
| Off | No chords |

**Bass patterns**

| Pattern | Sounds like |
|---|---|
| Steady 8ths | Root note on every 8th note |
| Octave bounce | Jumps between low and high root |
| Offbeat pump | Dance style, hits between the beats |
| Driving 16ths | Fast and intense |
| Bossa | Root and fifth, bossa nova rhythm |
| Funky | Syncopated with octave and seventh |
| Walk (quarters) | Root, fifth, octave, fifth on each beat |
| Long notes | One long note per bar |
| Off | No bass |

### Chords

Each box is one bar. Tap it, then choose the **Root** (C, D, Eb…) and **Type** (major, minor, 7, maj7, m7, sus4, sus2, dim, add9, maj9, m9, 6). You hear the chord when you change it. Tap **Done** to close the picker.

### Bar

The Melody, Drums and Sound effects grids show one bar at a time. Tap a bar number to edit that bar. While a section plays, the view follows the music.

### Melody

- Each row is a note, labelled on the left (C5, D5…). Rows in the song's key are shaded, so sticking to shaded rows always sounds right.
- Pick a note length first (**1/16**, **1/8**, **1/4**, **1/2** or **Whole**), then tap a cell to add a note there. Long notes show as a bar that continues to the right.
- Tap any part of a note to remove it.
- **Lower** and **Higher** show other octaves. Notes outside the view still play.
- You can stack notes in the same column to play a chord.

### Drums

Seven rows: Kick, Snare, Clap, Rim, Hi-hat, Open hat and Crash. Tap a cell to add or remove a hit. Darker columns mark the beats (1, 2, 3, 4). On a phone, swipe sideways to see the whole bar. The melody, drum and effect grids scroll together.

### Sound effects

1. Tap an effect in the list to pick it (you hear a preview).
2. Tap a step in the **Effects** row to place it there. The cell shows a short label (Ri, Im, Co…).
3. Tap a placed effect to remove it.

Built-in effects (all made in code): Riser, Impact, Whoosh, Downlifter, Reverse cymbal, Laser, Coin, Power-up, Jump, Explosion, Scratch, Air horn, Sleigh bells, Pop and Glitch.

**Upload your own:** tap it and choose one or more audio files (MP3, WAV and most others work). Each file is added to the list with its file name, and you place it the same way. Uploaded sounds stay while the page is open but are **not** saved in the song code, so add them again after reloading a song.

Tips: put a **Riser** at the start of the bar before a chorus and an **Impact** on the chorus's first step. A **Downlifter** or **Reverse cymbal** works well going into a quiet part.

### Sound

| Control | What it does |
|---|---|
| Melody instrument | Brass, Handheld trumpet, Square lead, Chiptune, Soft lead, Singing synth, Flute, Sax, Piano, Guitar or Marimba |
| Bass sound | Synth bass, Warm bass, Chiptune bass or Piano left hand |
| Drum kit | Band kit or Chiptune kit |
| Key (for the grid) | Changes which melody rows are shaded. It doesn't change any notes. |
| Tempo | 60 to 200 BPM |
| Swing | Pushes every other 16th note later for a laid-back, bouncy feel |
| Drums, Bass, Chords, Melody, Sound effects | Volume of each part |

**Make the full song** turns the whole song order into an audio track that plays on the page. **Clear this section's melody** removes every melody note in the current section (Undo brings them back).

### Song code

The box at the bottom is your whole song written as code (JSON). It updates as you edit.

- **Copy** puts the code on your clipboard, so you can paste it into a note or a file to save it.
- **Load this code** opens whatever code is in the box. Paste a song someone sent you, then press it.
- **Open a file** loads a saved song file (.json or .txt).

If the code has a typo, Loop Lab says so and keeps your current song. Your last song is also remembered in your browser.

## Making a song from scratch

1. Tap **New song**, rename it, and set the **Tempo**.
2. Set the chords for the first section, then choose a **Chord style** and **Bass pattern**.
3. Tap **Loop section** and build a drum beat.
4. Add a melody using the shaded rows.
5. **Duplicate** the section, rename it "Chorus", and make it bigger: busier drums, a higher melody, Brass stabs.
6. Make a short quiet **Intro** (Pad chords, no drums) and use **Add to end** to arrange: Intro, Verse, Chorus, Verse, Chorus.
7. Add a Riser and an Impact going into each chorus.
8. Press **Make the full song** to listen to the whole thing, then **Copy** the code to save it.

## Song code reference

```json
{
  "name": "My song",
  "bpm": 120,
  "swing": 0,
  "kit": "band",
  "lead": "brass",
  "bassSound": "synth",
  "scaleRoot": "C",
  "scale": "major",
  "sections": [
    {
      "name": "Verse",
      "bars": 4,
      "chords": ["C", "G", "Am", "F"],
      "melody": [[0,72,4], [4,74,2]],
      "drums": { "kick": "x...x...x...x...", "snare": "....x.......x...", "...": "one character per step" },
      "chordStyle": "pad",
      "bass": "root8",
      "sfx": [[0,"impact"], [48,"riser"]]
    }
  ],
  "arrangement": [0, 0],
  "mix": { "drums": 0.8, "bass": 0.8, "chords": 0.8, "melody": 0.8, "sfx": 0.8 }
}
```

| Field | Meaning |
|---|---|
| `melody` | List of notes as `[step, note, length]`. Step 0 is the first 16th of the section, note is a MIDI number (60 = middle C), and length is in 16ths. |
| `drums` | One string per drum (`kick`, `snare`, `clap`, `rim`, `hat`, `open`, `crash`), one character per step: `x` = hit, `.` = rest. |
| `sfx` | List of `[step, effect]`. Effects: `riser`, `impact`, `whoosh`, `drop`, `revcym`, `laser`, `coin`, `power`, `jump`, `boom`, `scratch`, `horn`, `bells`, `pop`, `glitch`. |
| `arrangement` | Song order as section numbers, starting at 0. |
| `chordStyle` | `off`, `pad`, `stabs`, `ep`, `piano`, `guitar`, `strum`, `arp`, `chip` |
| `bass` | `off`, `root8`, `octave`, `offbeat`, `pump16`, `bossa`, `funky`, `walk`, `long` |
| `lead` | `brass`, `trumpet`, `square`, `chip`, `soft`, `voice`, `flute`, `sax`, `piano`, `guitar`, `marimba` |
| `bassSound` | `synth`, `finger`, `chip`, `piano` |
| `kit` | `band`, `chip` |

Anything missing or out of range is filled in with a safe default when the song loads.

## Good to know

- Audio starts after your first tap, because browsers block sound until you interact with the page.
- On some hosted pages (like a claude.ai link) downloads are blocked, so the full song plays on the page instead of downloading. Opened directly from this repo, your browser's audio player usually offers a download in its menu.
- The built-in songs are simplified versions. Songs that use chopped breakbeats, 7/8 time or distorted guitars (Overclocked, Nobody's Looking, Lantern Theory, Boundless Run) aren't included yet.
