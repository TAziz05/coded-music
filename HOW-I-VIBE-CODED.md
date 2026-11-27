# How I Vibe-Coded Coded Music

*By Towfiq Aziz · last updated November 25, 2026*

## What it is

Coded Music is a library of original songs where **every note is written as code**. There are no samples from other songs and no AI audio generators. I built it with Claude without writing the code myself, starting with the music for my trivia games and growing into **221 songs** for my YouTube videos. It went from a few game songs to over 200 tracks in about a week.

You can listen at [taziz05.github.io/coded-music](https://taziz05.github.io/coded-music/) and make your own songs in [Loop Lab](https://taziz05.github.io/coded-music/loop-lab/).

- **The songs:** menu and gameplay music for Drop-In Daily and Daily Poké Catch, and gameplay tracks for YouTube. Styles include breakcore, hyperpop, drum & bass, K-pop eras, sports anthems and game-world tributes.
- **The website:** search, filters, favorites, "sounds similar" and "similar structure" lists, seamless loops, a loop picker, and extended versions (2 to 20 minutes) you can download as MP3.
- **Loop Lab:** a song maker in the browser. Every song on the site opens in Loop Lab as a simpler version you can remix and export.

## How the songs are made

Each song is a Python script. Claude writes the notes, drums and chords. The script builds every sound from math (sine waves, noise, filters), mixes them and saves an MP3. A YouTube card and a video are made from each song.

Some songs come from other things instead of being composed:

- **Pictures:** a photo is read left to right. Where your eye goes in each column becomes the melody (higher in the picture = higher note), the colors become the chords, and how busy the picture is sets the tempo.
- **Words:** letters become notes (A to G, then around again), Morse code becomes rhythms, and a poem of mine became one note per syllable.
- **Math and science:** the Collatz sequence, prime numbers, Pascal's triangle, Fourier waves, shapes as rhythms, the colors of the rainbow, and a real human gene (beta-globin), where each DNA base is a note.

## How I worked with Claude

I was the listener and the editor. Claude wrote the music and the code.

- **Feedback by timestamp.** Most changes started with a message like "the volume picks up at 1:14" or "the high flute is too piercing", and Claude fixed it and sent the song back.
- **Listen before it goes public.** New songs only go on the website after I've listened and approved them. When something went up before I'd heard it, Claude took it back down.
- **Rules from day one.** No AI-generated audio, every song credited "Coded with Claude (Opus 5.5) by Anthropic", and steady volume between sections.
- **Claude checks its own work.** Before sending a song, Claude measures its loudness second by second to catch jumps, and it tests the website in a phone-sized browser before pushing.
- **Two chats, one repo.** More than one chat works in the repo at once, so Claude always pulls the latest version first and only adds files or makes small edits.

## What went wrong and what I learned

- **Volume jumps.** The biggest problem by far was the music getting louder or quieter when a new section started. The fix was to level each song as a whole instead of section by section, and to check every second for jumps.
- **Everything ended the same way.** I asked why all the songs ended alike, so each song now gets its own ending (an echo, a fade, a tape stop, a final hit, a ringing bell and more), and newer songs vary how they start and how they're built.
- **Breakcore fading under the drums.** The melody disappeared when the breaks came in, so the engine now keeps the music and the drums balanced.
- **Website hiccups.** The website wouldn't publish while the repo was private, and GitHub Pages has a 1 GB limit, so the site now plays lighter copies of the songs while the full-quality files stay in the repo.
- **Too cluttered on phones.** The song pages had too many buttons, so the extras now fold away.

What I'd tell someone else: decide your rules first, listen to everything yourself, give feedback with timestamps, and don't publish what you haven't heard.

## Credits

Coded with Claude (Opus 5.5) by Anthropic. Ideas, song choices, feedback and photos by Towfiq Aziz (TAziz322). Songs are free to use with credit: a link to the site, or the song name and "Coded Music by TAziz322".
