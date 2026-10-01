"""Static link audit: every href/src in generated HTML resolves to a file or in-page id."""
import re, sys
from pathlib import Path
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parent.parent
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.ids=set()
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        for k in ("href", "src"):
            if a.get(k): s.links.append(a[k])
pages = [p for p in ROOT.rglob("*.html") if "src" not in p.parts and "node_modules" not in p.parts]
parsed = {}
for p in pages:
    x = P(); x.feed(p.read_text()); parsed[p.resolve()] = x
bad, ext, n = [], set(), 0
for p, x in parsed.items():
    for l in x.links:
        n += 1
        if re.match(r"^(https?:|mailto:)", l): ext.add(l); continue
        path, _, frag = l.partition("#")
        tgt = ((ROOT / path.lstrip("/")) if path.startswith("/") else (p.parent / path)).resolve() if path else p
        if path.endswith("/"): tgt = tgt / "index.html"
        if not tgt.exists(): bad.append(f"{p.relative_to(ROOT)} -> {l} (missing file)"); continue
        if frag and tgt.suffix == ".html" and frag not in parsed[tgt].ids:
            bad.append(f"{p.relative_to(ROOT)} -> {l} (missing #{frag})")
print(f"pages={len(pages)} links={n} external={sorted(ext)}")
print("\n".join(bad) or "ALL INTERNAL LINKS OK"); sys.exit(1 if bad else 0)
