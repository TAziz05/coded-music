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
    ("Boundless Run", "155 BPM · upbeat rock, Sonic style", ("#0a2a8c", "#1f5fe0", "#6fc3ff", "#071d60", "#ffd400")),
    ("Morning Over the Valley", "90 BPM · orchestral waltz", ("#3a2a12", "#c27a2c", "#ffd9a0", "#2a1c08", "#fff6e0")),
    ("Shattered Overture", "orchestral → breakcore", ("#14060a", "#5a1024", "#d23b4f", "#0a0306", "#ffe6c7")),
    ("Paper Sky", "170 BPM · bright breakcore", ("#123a6b", "#3f86d1", "#ffd3e8", "#0b2648", "#fff4a3")),
    ('Last Light', '174 BPM · sad breakcore', ('#0d0d1a', '#2b2b4f', '#7a7ab8', '#05050d', '#c9c9ff')),
    ('First Bloom', '172 BPM · spring breakcore', ('#1f5c2e', '#5fbf6a', '#ffe0ef', '#123a1c', '#fff7b0')),
    ('Heatwave Arcade', '180 BPM · summer breakcore', ('#7a1500', '#ff5a1f', '#ffd23f', '#4d0d00', '#ffffff')),
    ('Amber Leaves', '168 BPM · autumn lo-fi breakcore', ('#3d1a05', '#b5531a', '#f2b56b', '#2a1204', '#fff0d9')),
    ('Frostline', '176 BPM · winter breakcore', ('#0b2a4a', '#5aa7e0', '#eaf6ff', '#071c33', '#ffffff')),
    ('Window Seat', '165 BPM · rainy lo-fi breakcore', ('#1b2530', '#46586b', '#9fb2c4', '#10171e', '#e3eef8')),
    ('Lightning Over the City', '185 BPM · thunderstorm breakcore', ('#07060f', '#2a1f4f', '#8a6cff', '#030208', '#fff36b')),
    ('Lantern in the Fog', '160 BPM · foggy breakcore', ('#2a2e33', '#6b737c', '#c9ced3', '#1a1d20', '#ffd27a')),
    ('Kite Season', '178 BPM · windy breakcore', ('#0b4f6c', '#40a8c4', '#d9f3ff', '#073446', '#ffe14d')),
    ('Golden Hour Groove', '114 BPM · BTS-style disco-pop', ('#4a1f00', '#d6801c', '#ffd27a', '#2e1300', '#ffffff')),
    ('Blue Spark Runaway', '160 BPM · TXT-style pop-punk', ('#071a3d', '#2753b8', '#8fd0ff', '#040f26', '#ffe6f5')),
    ("Off the Lines", "150 BPM · CORTIS-style rage trap", ("#0a1f0a", "#1f7a1f", "#7dff4f", "#051005", "#f2ff3d")),
    ('Breeze in the Alley', '98 BPM · Fujii Kaze-style J-pop soul', ('#2b1d10', '#8a5a2b', '#e8c99a', '#1b1209', '#ffffff')),
    ('Golden Hour Breaks', '172 BPM · BTS-style breakcore', ('#4a1f00', '#d6801c', '#ffd27a', '#2e1300', '#fff3c4')),
    ('Blue Spark Breaks', '176 BPM · TXT-style breakcore', ('#071a3d', '#2753b8', '#8fd0ff', '#040f26', '#ffffff')),
    ('Off the Lines Breaks', '170 BPM · CORTIS-style breakcore', ('#0a1f0a', '#1f7a1f', '#7dff4f', '#051005', '#ffffff')),
    ('Lanterns and Thunder Drums', '168 BPM · East Asian breakcore', ('#3a0606', '#b3201c', '#f2c14e', '#220303', '#fff4d6')),
    ('Breeze Breaks', '172 BPM · Fujii Kaze-style breakcore', ('#2b1d10', '#8a5a2b', '#e8c99a', '#1b1209', '#fff7e8')),
    ('Schoolyard Riot', '96 BPM · BTS School-era boom-bap', ('#1a0b0b', '#6b1a1a', '#d94141', '#0d0505', '#ffd23f')),
    ('Dark and Wild Run', '140 BPM · BTS Dark & Wild-era rock-rap', ('#050505', '#3a0d0d', '#a31f1f', '#000000', '#ffffff')),
    ('Youth in Bloom', '128 BPM · BTS HYYH-era synth-pop', ('#3a1a4d', '#c25a9b', '#ffc2d9', '#240f30', '#ffffff')),
    ('Velvet Wings', '93 BPM · BTS Wings-era moombahton', ('#0a0a14', '#2b1f4a', '#7a5fb3', '#05050a', '#f2d7ff')),
    ('Double Helix', '128 BPM · BTS LY Her-era pop', ('#0f3d5c', '#4fb0d9', '#ffd1e6', '#08263a', '#ffffff')),
    ('Fragile Mask', '78 BPM · BTS LY Tear-era emo hip-hop', ('#0d0d1a', '#2a2a4a', '#6b6bb3', '#05050d', '#ff9fb3')),
    ('Eolssu Groove', '126 BPM · BTS LY Answer-era gugak x gqom', ('#1a0f05', '#a3361c', '#f2b23d', '#0d0702', '#ffffff')),
    ('Light Up the Persona', '120 BPM · BTS MOTS Persona-era funk-pop', ('#5c1a4d', '#ff6fa8', '#ffe08a', '#3a0f30', '#ffffff')),
    ('March of Seven', '106 BPM · BTS MOTS 7-era march', ('#0b0b0b', '#3a3a3a', '#9a9a9a', '#000000', '#ffd23f')),
    ('Life Goes Slow', '82 BPM · BTS BE-era acoustic lo-fi', ('#2b2014', '#8a6a45', '#e8d2b0', '#1a130b', '#ffffff')),
    ('Yet to Bloom', '90 BPM · BTS Proof-era mellow hip-hop', ('#1f2a3d', '#5a78a8', '#d9e6ff', '#121a26', '#fff3c4')),
    ('Arirang Dawn', '94 BPM · BTS ARIRANG-era', ('#0b1622', '#2e5a7a', '#f0c987', '#060d14', '#ffffff')),
    ('Riverbank Evening', '96 BPM · Bengali folk style', ('#0d3b2e', '#2f8f6b', '#f2d16b', '#06241b', '#ffffff')),
    ('Monsoon Breaks', '172 BPM · Bengali breakcore', ('#0d2433', '#2f6f8f', '#bfe3f2', '#061520', '#ffe48a')),
    ('Sky-Piercing Promise', '176 BPM · anime opening style', ('#0b1d4a', '#2a5bd7', '#ffb3c7', '#060f2a', '#ffffff')),
    ('Sky-Piercing Breaks', '180 BPM · anime breakcore', ('#140b3a', '#5a2ad7', '#ffd1e0', '#0a0620', '#ffffff')),
    ('Arcade Heartbreak 2005', '150 BPM · South Arcade-style pop-punk', ('#1a0a2e', '#7a1fa8', '#39ff14', '#0d0518', '#ffffff')),
    ('Iron Storm Rising', '168 BPM · heavy metal', ('#0a0a0a', '#3a3a3a', '#c0c0c0', '#000000', '#ff3b2f')),
    ('Iron Storm Breaks', '176 BPM · metal breakcore', ('#120404', '#5a0f0f', '#ff4f2f', '#080202', '#ffffff')),
    ('Respawn Lounge', '84 BPM · chill lo-fi BGM', ('#1d2433', '#4a5a7a', '#d9c7a6', '#10141d', '#ffffff')),
    ('Final Circle', '140 BPM · trap EDM BGM', ('#1a0510', '#7a0f3a', '#ff5fa2', '#0d0208', '#ffffff')),
    ('Pallet Path', '132 BPM · Game Boy route style', ('#2f3d1f', '#8bac0f', '#e0f8d0', '#1a2310', '#0f380f')),
    ('Johto Morning', '128 BPM · Game Boy Color route style', ('#3a1f4a', '#c06fd9', '#ffe08a', '#200f2a', '#ffffff')),
    ('Snowpoint Trail', '120 BPM · DS route style', ('#123a5c', '#5fa8d9', '#eaf6ff', '#0a2238', '#ffffff')),
    ('Island Breeze', '104 BPM · tropical route style', ('#0b4a5c', '#1fb3c9', '#ffe7a3', '#062a35', '#ffffff')),
    ('Stadium Highlands', '128 BPM · stadium march style', ('#3a0b0b', '#b32a2a', '#ffd23f', '#200505', '#ffffff')),
    ('Sunlit Plaza', '132 BPM · Spanish guitar route style', ('#5c2a0b', '#d9772a', '#ffe0a3', '#351705', '#ffffff')),
    ('Emerald Shore Zone', '142 BPM · 16-bit FM zone style', ('#0b3a2a', '#1fb36f', '#7fe0ff', '#06221a', '#ffffff')),
    ('Time Warp Zone', '126 BPM · 90s house zone style', ('#2a0b4a', '#8a2ad9', '#5fffd7', '#16052a', '#ffffff')),
    ('Treasure Hunt Flow', '92 BPM · hip-hop stage style', ('#2a1a05', '#a8701f', '#ffd27f', '#170e02', '#ffffff')),
    ('Rush Hour Boost', '152 BPM · breakbeat jazz-funk', ('#4a0b0b', '#e03a1f', '#ffd400', '#2a0505', '#ffffff')),
    ('Moonlit Night Stage', '140 BPM · swing jazz stage style', ('#0b0f2a', '#2a3a7a', '#f2d16b', '#05071a', '#ffffff')),
    ('Starlight Carnival Run', '128 BPM · space carnival EDM-pop', ('#1a0b4a', '#6f2ad9', '#ffd1ff', '#0d052a', '#ffffff')),
    ('Lime Green Afterparty', '132 BPM · Charli xcx Brat-style club', ('#0f1a05', '#5a8a0f', '#8ace00', '#070d02', '#000000')),
    ('Red 40 Sugar Rush', '162 BPM · sugar-rush hyperpop', ('#4a0505', '#e01f1f', '#ffd1d1', '#2a0202', '#ffffff')),
    ('Padma to Kyoto', '100 BPM · Bangladesh x Japan', ('#0b3a2e', '#2f8f6b', '#ffb3a7', '#06221b', '#ffffff')),
    ('Arcade Heartbreak Breaks', '172 BPM · pop-punk breakcore', ('#1a0a2e', '#5a1f8a', '#39ff14', '#0d0518', '#ffffff')),
    ('Boulevard Café', '116 BPM · French café route style', ('#3a1f0b', '#a8602a', '#ffe3b3', '#200f05', '#ffffff')),
    ('Highway Escape', '160 BPM · punk-rock stage style', ('#0b1a3a', '#1f4fb3', '#ff3b2f', '#050d20', '#ffffff')),
    ('Titan Undefeated', '150 BPM · epic rock boss style', ('#1a0505', '#7a1a0f', '#ffb347', '#0d0202', '#ffffff')),
    ('Winds of the World', '104 BPM · world flutes', ('#0b3a3a', '#2a8f8f', '#f2e6b3', '#062020', '#ffffff')),
    ('Sugar Cloud Smile', '128 BPM · Marshmello-style future bass', ('#2a1a4a', '#8a6fe0', '#ffffff', '#150d2a', '#ffc7f0')),
    ('Sugar Cloud Breaks', '172 BPM · future-bass breakcore', ('#1a0d3a', '#6f4fd0', '#ffe0ff', '#0d0620', '#ffffff')),
    ('Lime Green Breaks', '176 BPM · club breakcore', ('#0a1405', '#3a6a0a', '#8ace00', '#050a02', '#000000')),
    ('Padma to Kyoto Breaks', '172 BPM · Bangladesh x Japan breakcore', ('#06221b', '#1f6f55', '#ffb3a7', '#03140f', '#ffffff')),
    ('Grassland Hop', '150 BPM · NSMB Wii World 1 style', ('#0f3a0b', '#3fae2a', '#ffe14d', '#082005', '#ffffff')),
    ('Desert Dunes', '120 BPM · NSMB Wii World 2 style', ('#5c3a0b', '#d99a2a', '#fff0b3', '#352005', '#ffffff')),
    ('Snowcap Slide', '112 BPM · NSMB Wii World 3 style', ('#123a5c', '#7fc4f2', '#ffffff', '#0a2238', '#1f4f8f')),
    ('Coconut Cove', '124 BPM · NSMB Wii World 4 style', ('#0b4a5c', '#1fc9b3', '#ffe7a3', '#062a35', '#ffffff')),
    ('Mushroom Woods', '116 BPM · NSMB Wii World 5 style', ('#2a0b3a', '#6f2a8f', '#9fff6f', '#150520', '#ffffff')),
    ('Cliffside Climb', '132 BPM · NSMB Wii World 6 style', ('#3a2a1a', '#8f6f4a', '#ffd27f', '#20150a', '#ffffff')),
    ('Cloudtop Athletic', '160 BPM · NSMB Wii World 7 style', ('#1f5fb3', '#7fc4ff', '#ffffff', '#0f3060', '#ffe14d')),
    ('Magma Fortress', '132 BPM · NSMB Wii World 8 style', ('#2a0505', '#b32a0b', '#ffb000', '#150202', '#ffffff')),
    ('Starry Road', '140 BPM · NSMB Wii World 9 style', ('#0b0b3a', '#4a2ab3', '#ffe14d', '#05051f', '#ffffff')),
    ('Pipe Cavern', '120 BPM · NSMB Wii underground style', ('#0b1a1a', '#1f4a4a', '#5fd9ff', '#050d0d', '#ffffff')),
    ('Coral Waltz', '150 BPM · NSMB Wii underwater style', ('#062a4a', '#1f6fb3', '#9ff2ff', '#03152a', '#ffffff')),
    ('Haunted Manor', '96 BPM · NSMB Wii ghost house style', ('#1a0b2a', '#4a2a6f', '#c7ffd9', '#0d0515', '#ffffff')),
    ('Shellfire Castle', '112 BPM · NSMB Wii castle style', ('#1a0505', '#5a0f0f', '#ff6f2f', '#0d0202', '#ffd27f')),
    ('Glitter Overload', '136 BPM · bubblegum hyperpop', ('#4a0b3a', '#e02ab3', '#ffe0ff', '#2a0520', '#ffffff')),
    ('Bitcrushed Daydream', '150 BPM · glitchcore hyperpop', ('#0b1a2a', '#2a5a8f', '#c7e0ff', '#050d15', '#ffffff')),
    ('Static Tears', '140 BPM · emo hyperpop', ('#1a0b1f', '#5a2a6f', '#ffc7d9', '#0d0510', '#ffffff')),
    ('Nightcore Rush', '172 BPM · nightcore', ('#1a0b4a', '#8a2ae0', '#7ff2ff', '#0d052a', '#ffffff')),
    ('Menu Drift', '100 BPM · calm menu BGM', ('#1d2a3a', '#4a6f9a', '#d9ecff', '#0f1720', '#ffffff')),
    ('Skyscraper Sprint', '150 BPM · city route style', ('#1a1a2a', '#4a4a7a', '#ffd23f', '#0d0d15', '#ffffff')),
    ('Red 40 Breaks', '178 BPM · hyperpop breakcore', ('#2a0202', '#a80f0f', '#ffd1d1', '#150101', '#ffffff')),
    ('Aqua Tomorrow', '116 BPM · Frutiger Aero pop-rock', ('#0b4a7a', '#3fb3f2', '#e0ffff', '#06284a', '#ffffff')),
    ('Aqua Tomorrow Breaks', '172 BPM · Frutiger Aero breakcore', ('#06284a', '#1f8fd9', '#c7f7ff', '#03152a', '#ffffff')),
    ('Pixel Heart DnB', '174 BPM · hyperpop drum & bass', ('#2a0b4a', '#c02ae0', '#ffd1f7', '#15052a', '#ffffff')),
    ('Midnight Drift', '130 BPM · drift phonk', ('#0a0a12', '#2a1a3a', '#b38fff', '#050508', '#ffffff')),
    ('Neon Horizon', '104 BPM · synthwave', ('#1a0533', '#e02a8f', '#ffb347', '#0d021a', '#ffffff')),
    ('Turbo Corner', '156 BPM · eurobeat', ('#2a0505', '#e0471f', '#ffe14d', '#150202', '#ffffff')),
    ('Checkerboard Skank', '168 BPM · ska', ('#111111', '#555555', '#ffffff', '#000000', '#ff3b2f')),
    ('Island Time', '76 BPM · reggae', ('#0b3a0b', '#e0b31f', '#ff3b2f', '#052005', '#ffffff')),
    ('Log Drum Sunset', '112 BPM · amapiano', ('#3a1a05', '#d9772a', '#ffe0b3', '#200d02', '#ffffff')),
    ('Holler Hoedown', '150 BPM · bluegrass', ('#3a2a0b', '#a8802a', '#fff0c7', '#201505', '#ffffff')),
    ('Tokyo Sunset Drive', '112 BPM · city pop', ('#3a0b2a', '#e06f8f', '#ffd9a3', '#200515', '#ffffff')),
    ('Squeak Sprint', '140 BPM · jersey club', ('#0b0b2a', '#2a2ae0', '#ffffff', '#05051a', '#ff5fa2')),
    ('Indigo Fields', '86 BPM · RM solo style', ('#0b1a3a', '#2a4a8f', '#c7d9ff', '#050d20', '#ffffff')),
    ('Starlit Orbit', '126 BPM · Jin solo style', ('#0b0b3a', '#3a5fd9', '#ffd1f7', '#05051f', '#ffffff')),
    ('Street Neuron', '100 BPM · j-hope solo style', ('#3a0b0b', '#d9472a', '#ffe14d', '#200505', '#ffffff')),
    ('Velvet Layover', '76 BPM · V solo style', ('#1a0b1a', '#5a2a4a', '#f2c7a3', '#0d050d', '#ffffff')),
    ('Infinite Series', '120 BPM · built from math', ('#0b1a1a', '#1f5a5a', '#9fffe0', '#050d0d', '#ffffff')),
    ('Level Up Rush', '124 BPM · upbeat EDM BGM', ('#0b2a4a', '#1f8fe0', '#ffe14d', '#05152a', '#ffffff')),
    ('Royal Procession', '102 BPM · SUGA solo style', ('#1a0505', '#8f1f1f', '#ffd27f', '#0d0202', '#ffffff')),
    ('Oops Again', '150 BPM · funny-fail polka', ('#3a2a05', '#e0a81f', '#ff5fa2', '#201505', '#ffffff')),
    ('Tiptoe Heist', '104 BPM · sneaky stealth jazz', ('#0b0b1a', '#2a2a5a', '#c7c7ff', '#05050d', '#ffffff')),
    ('Final Zone Countdown', '120 BPM · clutch countdown', ('#1a0505', '#3a0b0b', '#ff3b2f', '#0d0202', '#ffffff')),
    ('See You Next Drop', '120 BPM · end screen outro', ('#2a0b4a', '#e02a8f', '#ffe14d', '#15052a', '#ffffff')),
    ('Midnight Mirage', '118 BPM · Jimin solo style', ('#1a0b3a', '#8a2ae0', '#ffc7f0', '#0d051f', '#ffffff')),
    ('Gold Rush Garage', '126 BPM · Jung Kook solo style', ('#2a1a05', '#d9a82a', '#fff0c7', '#150d02', '#ffffff')),
    ('Breakcore Squared', '186 BPM · double breakcore', ('#05050a', '#3a0b5a', '#ff2bd6', '#020205', '#ffffff')),
    ('Comeback Rising', '128 BPM · comeback anthem', ('#0b1a3a', '#3a5fd9', '#ffd23f', '#050d20', '#ffffff')),
    ('Bass Quake', '140 BPM · dubstep', ('#1a0533', '#5a0fa8', '#00f0ff', '#0d021a', '#ffffff')),
    ('Infinite Series Breaks', '174 BPM · math breakcore', ('#051a1a', '#0f5a5a', '#9fffe0', '#020d0d', '#ffffff')),
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
