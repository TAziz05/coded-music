import asyncio,math,os
from playwright.async_api import async_playwright
FD={"fn":"/home/claude/drop-in-daily/twitch/fonts/","pk":"/home/claude/daily-poke-catch/twitch/fonts/"}
songs=[("fn","Drop-In Daily - Lobby","Lobby"),("fn","Drop-In Daily - Match","Match"),("fn","Drop-In Daily - Mythic Match (OG style)","Mythic Match"),("fn","Drop-In Daily - Endless Summary (OG lobby style)","Endless Summary"),
 ("pk","Daily Poke Catch - Route (Menus)","Route"),("pk","Daily Poke Catch - Battle","Battle"),("pk","Daily Poke Catch - Mythic Battle","Mythic Battle"),("pk","Daily Poke Catch - Town (Endless Summary)","Town")]
def fn_card(t):
    return f'''<link rel="stylesheet" href="fonts.css"><style>html,body{{margin:0;width:1920px;height:1080px;overflow:hidden}}body{{background:linear-gradient(180deg,#0f4fc4,#2f86f0 55%,#7cc4ff);font-family:Barlow,"Barlow Condensed",sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 150px;box-sizing:border-box;position:relative}}
    .rays{{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 70% -20%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg)}}
    h1{{font:italic 400 150px/0.95 Anton,sans-serif;text-transform:uppercase;margin:0;text-shadow:0 10px 0 #0b3f8f;position:relative}}h1 span{{color:#ffd53d}}
    .song{{font:italic 400 120px/1 Anton,sans-serif;text-transform:uppercase;color:#ffd53d;margin-top:60px;text-shadow:0 8px 0 #0b3f8f;position:relative}}
    .sub{{font:600 44px "Barlow Condensed",sans-serif;letter-spacing:6px;text-transform:uppercase;margin-top:30px;position:relative}}
    .foot{{position:absolute;left:150px;bottom:70px;font:600 34px "Barlow Condensed",sans-serif;opacity:.9}}</style>
    <div class="rays"></div><h1>Drop-In <span>Daily</span></h1><div class="song">{t}</div><div class="sub">Original soundtrack · made in code</div><div class="foot">TAziz322</div>'''
def pk_card(t):
    cols=["#EE8130","#6390F0","#F7D02C","#7AC74C","#F95587","#A33EA1"]
    segs="".join(f'<path d="M{150+140*math.cos(a0):.1f} {150+140*math.sin(a0):.1f}A140 140 0 0 1 {150+140*math.cos(a1):.1f} {150+140*math.sin(a1):.1f}L{150+92*math.cos(a1):.1f} {150+92*math.sin(a1):.1f}A92 92 0 0 0 {150+92*math.cos(a0):.1f} {150+92*math.sin(a0):.1f}Z" fill="{c}"/>' for i,c in enumerate(cols) for a0,a1 in [(-math.pi/2+i*math.pi/3+.05,-math.pi/2+(i+1)*math.pi/3-.05)])
    ring=f'<svg width="300" height="300" viewBox="0 0 300 300"><circle cx="150" cy="150" r="148" fill="#0c1640"/>{segs}<circle cx="150" cy="150" r="92" fill="#ffcb05"/><text x="150" y="200" text-anchor="middle" font-family="Lilita One" font-size="140" fill="#1f4fae">?</text></svg>'
    stars="".join(f'<i style="left:{(i*137)%1900}px;top:{(i*71)%760}px;opacity:{.3+(i%5)/8}"></i>' for i in range(70))
    tips=",".join(f"{x}% {0 if j%2 else 30}%" for j,x in enumerate(range(0,101,2)))
    return f'''<link rel="stylesheet" href="fonts.css"><style>html,body{{margin:0;width:1920px;height:1080px;overflow:hidden}}body{{background:linear-gradient(180deg,#0b1640,#1b3384 70%,#2a4fa8);font-family:Nunito,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 150px;box-sizing:border-box;position:relative}}
    i{{position:absolute;width:4px;height:4px;background:#fff;border-radius:50%}}
    .grass{{position:absolute;left:0;right:0;bottom:0;height:120px;background:repeating-linear-gradient(90deg,#2f7d3a 0 18px,#3c9447 18px 36px);clip-path:polygon({tips},100% 100%,0 100%)}}
    .row{{display:flex;align-items:center;gap:50px;position:relative}}
    h1{{font:400 130px/1 "Lilita One",sans-serif;margin:0;color:#ffcb05;text-shadow:0 8px 0 #1f4fae}}h1 span{{color:#fff}}
    .song{{font:400 64px/1 "Press Start 2P",monospace;color:#fff;margin-top:70px;position:relative;text-shadow:0 6px 0 #1f4fae}}
    .sub{{font:800 38px Nunito,sans-serif;letter-spacing:5px;text-transform:uppercase;margin-top:40px;position:relative}}
    .foot{{position:absolute;left:150px;bottom:150px;font:800 30px Nunito,sans-serif;opacity:.9}}</style>
    {stars}<div class="row">{ring}<h1>Daily Poké <span>Catch</span></h1></div><div class="song">{t}</div><div class="sub">Original soundtrack · made in code</div><div class="foot">TAziz322</div><div class="grass"></div>'''
async def run():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=await b.new_page(viewport={"width":1920,"height":1080})
        for g,file,t in songs:
            path=FD[g]+"_card.html";open(path,"w").write(fn_card(t) if g=="fn" else pk_card(t))
            await pg.goto("file://"+path);await pg.evaluate("document.fonts.ready");await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"/home/claude/ytv/{file}.png");os.remove(path)
        await b.close()
asyncio.run(run())
