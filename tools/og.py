import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1200,"height":630})
        await pg.emulate_media(reduced_motion="reduce")
        await pg.goto("http://localhost:8080/index.html"); await pg.wait_for_timeout(800)
        await pg.screenshot(path="assets/og.png"); await b.close()
asyncio.run(main())
