"""Records each song from its code into a raw WAV (three loops long) using headless Chrome + Playwright.
Needs: pip install playwright, and Chrome. Output goes to build/. Then run make-files.py."""
import asyncio,base64,json,wave,os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','build');os.makedirs(OUT,exist_ok=True)
from playwright.async_api import async_playwright
names=["fnMenu","fn","fnOGm","fnOG","pkMenu","pkB","pk","pkTown"]
async def run():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome");pg=await b.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file://"+os.path.abspath(os.path.join(os.path.dirname(__file__),"record.html")));meta={}
        for n in names:
            r=await pg.evaluate(f"render('{n}')")
            raw=base64.b64decode(r.pop("b64"))
            with wave.open(os.path.join(OUT,f"{n}-raw.wav"),"wb") as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(44100);w.writeframes(raw)
            meta[n]=r;print(n,"L",round(r["L"],4),"f",round(r["f"],3),"loop mismatch",round(r["diff"],5))
        json.dump(meta,open(os.path.join(OUT,"meta.json"),"w"));print(errs);await b.close()
asyncio.run(run())
