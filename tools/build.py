#!/usr/bin/env python3
"""Static site generator (stdlib only).

Content lives in src/pages/**.html as HTML fragments with a meta header.
Output is written to the repository root so GitHub Pages can serve it as-is.

    python3 tools/build.py
"""
import html
import json
import pathlib
import re
import sys

import diagrams

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pages"

# All deploy-specific values (site URL, contact profiles, artifact/code links) live in site.config.json.
CONFIG = json.loads((ROOT / "site.config.json").read_text())
SITE_URL = CONFIG.get("site_url", "").rstrip("/")
BASE_PATH = CONFIG.get("base_path", "/") or "/"
CONTACT_ORDER = [("github", "GitHub"), ("email", "Email"), ("linkedin", "LinkedIn"), ("arxiv", "arXiv")]
ARTIFACT_KINDS = [("evidence", "Evidence / Artifact"), ("code", "Code / Reproduce")]

NAV = [("research", "Research", "research/index.html"), ("manuscripts", "Manuscripts", "manuscripts.html"),
       ("evidence", "Evidence", "evidence.html"), ("writing", "Writing", "writing/index.html"), ("about", "About", "about.html")]

FOOTER_NOTE = "Independent Researcher &amp; Technical Builder. Education: BS student, IIT Madras."


def parse(path):
    text = path.read_text()
    m = re.match(r"<!--meta\n(.*?)\n-->\n", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def attrs(s):
    return {k: html.unescape(v) for k, v in re.findall(r'(\w+)="([^"]*)"', s)}


def ev(a):
    val = a["value"]
    neg = " neg" if "neg" in a else ""
    mark = ""
    if "/" in val:
        n, d = val.split("/")
        fig = f'<span data-count="{n}">{n}</span><span class="den">/{d}</span>'
        cls = "dots acc" if not neg else "dots"
        if "cmp" in a:
            cn, cd = a["cmp"].split("/")
            mark = (f'<div class="dots-row"><span>{html.escape(a.get("selflabel", "method"))}</span><div class="{cls}" data-dots="{val}"></div>'
                    f'<span>{html.escape(a["cmplabel"])}</span><div class="dots" data-dots="{a["cmp"]}"></div></div>')
        else:
            mark = f'<div class="{cls}" data-dots="{val}"></div>'
    elif val.endswith("%"):
        num = val[:-1]
        fig = f'<span data-count="{num}">{num}</span><span class="den">%</span>'
        mark = f'<div class="bar"><span style="--w:{max(float(num), 0.6)}%"></span></div>'
    else:
        raw = val.replace(",", "")
        fig = f'<span data-count="{raw}">{val}</span>'
        if "scale" in a:
            mark = f'<div class="bar ink"><span style="--w:{a["scale"]}%"></span></div>'
    return (f'<div class="ev{neg}"><div class="ev-ctx">{html.escape(a["ctx"])}</div>'
            f'<div class="ev-fig" aria-label="{html.escape(val)}">{fig}</div>{mark}'
            f'<p class="ev-label">{a["label"]}</p></div>')


def contact_block():
    rows = []
    for key, label in CONTACT_ORDER:
        val = CONFIG.get("contact", {}).get(key, "").strip()
        if not val:
            continue
        if key == "email":
            href, shown = f"mailto:{val.removeprefix('mailto:')}", val.removeprefix("mailto:")
        else:
            href, shown = val, re.sub(r"^https?://(www\.)?", "", val).rstrip("/")
        ext = "" if key == "email" else ' rel="me noopener" target="_blank"'
        rows.append(f'<a href="{html.escape(href)}"{ext}><span>{label}</span><span class="cv">{html.escape(shown)} <span class="arrow">↗</span></span></a>')
    if rows:
        return "".join(rows)
    return '<span class="pending"><span>Public profiles</span><span>Listed after verification</span></span>'


def artifact_block(project):
    links = CONFIG.get("artifacts", {}).get(project, {})
    out = []
    for key, label in ARTIFACT_KINDS:
        url = links.get(key, "").strip()
        if url:
            out.append(f'<a class="btn" href="{html.escape(url)}" rel="noopener" target="_blank">{label} <span class="arrow">↗</span></a>')
        else:
            out.append(f'<span class="btn is-pending" aria-disabled="true">{label}<span class="pend">Link pending</span></span>')
    return f'<div class="actions artifact-actions" aria-label="Artifacts and code">{"".join(out)}</div>'


def expand(body, r):
    body = re.sub(r"<x-ev ([^>]*)></x-ev>", lambda m: ev(attrs(m.group(1))), body)
    body = re.sub(r"\{\{fig:(\w+)\}\}", lambda m: getattr(diagrams, m.group(1))(), body)
    body = re.sub(r"\{\{glyph:(\w+)\}\}", lambda m: diagrams.glyph(m.group(1)), body)
    body = body.replace("{{contact}}", contact_block())
    body = re.sub(r"\{\{artifacts:([\w-]+)\}\}", lambda m: artifact_block(m.group(1)), body)
    return body.replace("{{root}}", r)


ICON_THEME = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="8" cy="8" r="5.5"/><path d="M8 2.5a5.5 5.5 0 0 0 0 11z" fill="currentColor"/></svg>'
ICON_MENU = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M2 5h12M2 11h12"/></svg>'


def page(meta, body, rel):
    depth = len(rel.parts) - 1
    is404 = rel.name == "404.html"
    r = BASE_PATH if is404 else "../" * depth
    cur = meta.get("nav", "")
    title = meta["title"]
    desc = meta.get("description", "")
    url = f"{SITE_URL}/{rel.as_posix()}".replace("/index.html", "/") if SITE_URL and not is404 else ""
    og_img = f"{SITE_URL}/assets/og.png" if SITE_URL else f"{r}assets/og.png"
    ac = ' aria-current="page"'
    nav = "".join(f'<a href="{r}{href}"{ac if key == cur else ""}>{label}</a>' for key, label, href in NAV)
    canon = f'<link rel="canonical" href="{url}"><meta property="og:url" content="{url}">' if url else ""
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="Saurav Sharma">
<meta property="og:type" content="{meta.get("ogtype", "website")}">
<meta property="og:site_name" content="Saurav Sharma — Independent Researcher">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og_img}">
{'<meta name="robots" content="noindex">' if is404 else ""}
{canon}
<meta name="theme-color" content="#f4f2ed" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0d0f" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{r}assets/fonts/newsreader-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/inter-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/styles.css">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t}}catch(e){{}}}})();</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
<div class="wrap nav">
<a class="brand" href="{r}index.html"><span class="brand-name">Saurav Sharma</span><span class="brand-role">Independent Researcher</span></a>
<nav class="nav-links" id="nav-links" aria-label="Primary">{nav}</nav>
<div class="nav-tools">
<button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle dark theme">{ICON_THEME}</button>
<button class="icon-btn menu-btn" type="button" data-menu aria-expanded="false" aria-controls="nav-links" aria-label="Menu">{ICON_MENU}</button>
</div>
</div>
</header>
<main id="main">
'''
    foot = f'''
</main>
<footer class="site-footer">
<div class="wrap">
<div class="footer-grid">
<div><span class="brand-name">Saurav Sharma</span><p class="footer-note">{FOOTER_NOTE}</p></div>
<div><span class="mono">Research</span><ul>
<li><a href="{r}research/rec.html">Premature Epistemic Action</a></li>
<li><a href="{r}research/microstructure.html">Information Acquisition &amp; the Market</a></li>
<li><a href="{r}research/private-credit.html">Model Error &amp; the Boundary</a></li>
<li><a href="{r}research/aei.html">Autonomous Economic Intelligence</a></li></ul></div>
<div><span class="mono">Site</span><ul>
<li><a href="{r}manuscripts.html">Manuscripts</a></li><li><a href="{r}evidence.html">Evidence ledger</a></li>
<li><a href="{r}writing/index.html">Writing</a></li><li><a href="{r}about.html">About</a></li></ul></div>
</div>
<div class="footer-base"><span>© <span data-year>2026</span> Saurav Sharma</span><span>Independent research</span></div>
</div>
</footer>
<script src="{r}assets/site.js" defer></script>
</body>
</html>
'''
    return head + expand(body, r) + foot


def main():
    urls = []
    for src in sorted(SRC.rglob("*.html")):
        rel = src.relative_to(SRC)
        meta, body = parse(src)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(meta, body, rel))
        if rel.name != "404.html":
            urls.append(rel.as_posix())
        print("built", rel)
    robots = "User-agent: *\nAllow: /\n"
    if SITE_URL:
        items = "\n".join(f"  <url><loc>{SITE_URL}/{u.replace('index.html', '')}</loc></url>" for u in urls)
        (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n')
        robots += f"Sitemap: {SITE_URL}/sitemap.xml\n"
    else:
        print("WARNING: site_url is empty in site.config.json -> no canonical URLs or sitemap.xml emitted", file=sys.stderr)
    (ROOT / "robots.txt").write_text(robots)


if __name__ == "__main__":
    main()
