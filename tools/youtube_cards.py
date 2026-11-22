"""Title cards + 1080p videos for the YouTube gameplay tracks (songs/youtube/).
Needs Playwright with Google Chrome, the Anton font installed, and ffmpeg.
Run from the repo root: python tools/youtube_cards.py"""
import asyncio, os, subprocess, tempfile
from playwright.async_api import async_playwright

SONGS = [  # file name, tempo/feel line, colours (top, mid, bottom, shadow, accent)
    ("Victory Rush", "128 BPM · upbeat", ("#0f4fc4", "#2f86f0", "#7cc4ff", "#0b3f8f", "#ffd53d")),
    ("Storm Closing", "140 BPM · intense", ("#2a0b52", "#6a1fb8", "#c06cff", "#1c0838", "#7ff3ff")),
    ("Lobby Loop", "102 BPM · chill", ("#06545a", "#14a3a0", "#8fe8d6", "#043a3e", "#fff07a")),
    ("Overclocked", "174 BPM · drum & bass", ("#140f2e", "#c2183f", "#ff6a3d", "#0b0820", "#e8ff3a")),
    ("Nobody's Looking", "180 BPM · breakcore", ("#05060d", "#1e2340", "#4d5a8c", "#000000", "#ff9fc8")),
    ("Static Weather", "146 BPM · Vocaloid-style J-rock", ("#1c2a4a", "#4f7fc4", "#bfe0ff", "#13203d", "#fff3a8")),
    ("Lantern Theory", "150 BPM · jazz math rock", ("#2b1608", "#a8501c", "#f2b45c", "#1d0e04", "#fff1d6")),
    ("Channel Plaza", "116 BPM · Wii menu style", ("#1f7fc0", "#4fb0e6", "#c9ecff", "#145a8a", "#ffffff")),
    ("Frosty Podium", "150 BPM · winter games style", ("#0d3b6e", "#3f8fd6", "#d6f0ff", "#0a2c52", "#ffe066")),
    ("Coastal Route", "132 BPM · GBA route style", ("#0b5d7a", "#22a6b3", "#f4d58d", "#083f53", "#ffde59")),
    ("Homebase Rising", "112 BPM · orchestral adventure", ("#1a1033", "#4b2a7a", "#e0742b", "#100820", "#ffc640")),
    ("Determined Steps", "120 BPM · solo piano", ("#000000", "#14141c", "#2a2a3a", "#000000", "#ff2a2a")),
    ("Ringworld Vigil", "Halo style · chant & strings", ("#0b1a12", "#1f4a36", "#7fb39a", "#06100b", "#d9f2e6")),
]
ONLY = None  # set to a song title to rebuild just that one

def card(title, line, c):
    top, mid, bot, sh, acc = c
    return f'''<style>html,body{{margin:0;width:1920px;height:1080px;overflow:hidden}}
body{{background:linear-gradient(180deg,{top},{mid} 55%,{bot});font-family:"Fira Sans",sans-serif;color:#fff;
display:flex;flex-direction:column;justify-content:center;padding:0 150px;box-sizing:border-box;position:relative}}
.rays{{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 70% -20%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg)}}
h1{{font:italic 400 110px/0.95 Anton,sans-serif;text-transform:uppercase;margin:0;text-shadow:0 8px 0 {sh};position:relative}}
.song{{font:italic 400 190px/1 Anton,sans-serif;text-transform:uppercase;color:{acc};margin-top:40px;text-shadow:0 10px 0 {sh};position:relative}}
.sub{{font:600 44px "Fira Sans",sans-serif;letter-spacing:6px;text-transform:uppercase;margin-top:40px;position:relative}}
.foot{{position:absolute;left:150px;bottom:70px;font:600 34px "Fira Sans",sans-serif;opacity:.9}}</style>
<div class="rays"></div><h1>Gameplay Music</h1><div class="song">{title}</div>
<div class="sub">{line} · original · made in code</div><div class="foot">TAziz322</div>'''

async def run():
    os.makedirs("cards", exist_ok=True); os.makedirs("videos", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        for title, line, c in SONGS:
            if ONLY and title not in ([ONLY] if isinstance(ONLY, str) else ONLY): continue
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f: f.write(card(title, line, c))
            await pg.goto("file://" + f.name); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            png = f"cards/YouTube - {title}.png"; await pg.screenshot(path=png); os.remove(f.name)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-i", png,
                            "-i", f"songs/youtube/{title}.mp3", "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                            f"videos/YouTube - {title}.mp4"], check=True)
            print("made", title)
        await b.close()

asyncio.run(run())
