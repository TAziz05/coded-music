"""Renders the website and Loop Lab icons (SVG) to PNG app icons. Run from the repo root: python tools/make_icons.py (needs playwright)."""
import asyncio, os
from playwright.async_api import async_playwright
JOBS = [('site/icons/coded-music.svg', 'site/icons/coded-music'), ('loop-lab/icons/loop-lab.svg', 'loop-lab/icons/loop-lab')]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for svg, out in JOBS:
            src = open(svg).read()
            for size in (32, 180, 192, 512):
                await pg.set_viewport_size({'width': size, 'height': size})
                await pg.set_content(f'<html><body style="margin:0;background:transparent">{src.replace("<svg ", f"<svg width=\"{size}\" height=\"{size}\" ", 1)}</body></html>')
                await pg.screenshot(path=f'{out}-{size}.png', omit_background=True, clip={'x': 0, 'y': 0, 'width': size, 'height': size})
        await b.close()
asyncio.run(main())
