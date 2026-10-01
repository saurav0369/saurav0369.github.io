import asyncio, sys
from playwright.async_api import async_playwright
PAGES = ["index.html","research/index.html","research/rec.html","research/microstructure.html","research/private-credit.html","research/aei.html","evidence.html","manuscripts.html","about.html","writing/index.html","writing/why-prediction-is-not-enough.html","404.html"]
async def main(out):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        errs=[]
        for name,vp,theme in [("desktop",{"width":1440,"height":900},"light"),("mobile",{"width":390,"height":844},"light"),("dark",{"width":1440,"height":900},"dark")]:
            ctx = await b.new_context(viewport=vp, device_scale_factor=1, color_scheme=theme)
            pg = await ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
            for path in PAGES if name!="dark" else PAGES[:3]:
                await pg.goto(f"http://localhost:8080/{path}")
                await pg.wait_for_timeout(400)
                # scroll through to trigger reveals
                h = await pg.evaluate("document.body.scrollHeight")
                for y in range(0, h, 500):
                    await pg.evaluate(f"scrollTo(0,{y})"); await pg.wait_for_timeout(60)
                await pg.wait_for_timeout(3500)
                await pg.evaluate("scrollTo(0,0)"); await pg.wait_for_timeout(300)
                ow = await pg.evaluate("document.documentElement.scrollWidth > innerWidth")
                if ow: errs.append(f"OVERFLOW {name} {path}")
                fn = path.replace("/","_").replace(".html","")
                await pg.screenshot(path=f"{out}/{name}-{fn}.png", full_page=True)
            await ctx.close()
        await b.close()
        print("\n".join(errs) or "no errors")
asyncio.run(main(sys.argv[1]))
