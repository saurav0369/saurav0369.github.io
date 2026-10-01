# Changelog — v3 redesign

## UI changes
- New design system: warm paper / ink palette with a single burnt-orange accent; full dark theme (system-preference aware + manual toggle, persisted).
- Editorial typography: Newsreader (display/serif), Inter (body), JetBrains Mono (labels/metadata), self-hosted WOFF2 — no external font or CDN requests.
- Animated schematic SVG figures (draw-on lines, travelling probes, growing bars), each labelled "Schematic · illustrative, not experimental data":
  Fig. 0 prediction vs. identification (home, essay); Fig. 1 probe-now vs. probe-at-boundary (REC); Fig. 2 passive vs. endogenous RFQ inquiry (microstructure); Fig. 3 omitted drain moves a reached constraint (private credit); conceptual AEI pipeline; small research-record glyphs.
- Evidence cards: every metric rendered with its denominator, a unit dot-grid / comparison bars, and its scope label beside it; negative results visually tagged and hatched, never de-emphasised.
- Research pages restructured to the brief's template (question → core idea → selected results → design → strongest attack / negative result → covers → does not establish → artifact status) with sticky "On this page" TOC, status sidebar, breadcrumbs, prev/next.
- Home IA per brief: hero → flagship research records → AEI (dark band with public/private boundary panel) → selected evidence → methods → background → writing → contact.
- Evidence ledger becomes a responsive table that stacks into labelled cards on mobile.
- Motion: word-by-word heading reveal, scroll reveals, count-ups, reading-progress bar; looping SVG motion pauses off-screen; everything disabled under `prefers-reduced-motion`.
- Accessibility: semantic landmarks, skip link, `aria-current`, `aria-expanded` mobile menu, visible focus rings, `role="img"` + title/desc on figures, decorative glyphs `aria-hidden`.
- New styled 404, S-monogram favicon, OG image, `robots.txt`, `.nojekyll`; optional sitemap/canonical via `SITE_URL`.
- Build: Python stdlib generator (`tools/build.py`) + link audit (`tools/audit_links.py`); no npm, no framework, no analytics.
- URLs: all original routes preserved unchanged (`/`, `/research/{index,rec,microstructure,private-credit,aei}.html`, `/evidence.html`, `/manuscripts.html`, `/about.html`, `/writing/{index,why-prediction-is-not-enough}.html`).

## Copy changes
No claims were added, removed, or strengthened. Every number on the site appears in the canonical files (automated check: zero non-canonical numerals other than section indices).
Non-claim editorial additions only:
- Section headings / short kickers (e.g. "Whether, and when.", "Context, not credential.", "Results are presented with their failure boundaries.").
- Figure captions describing the schematics, each restating mechanisms already in canonical copy and marked illustrative.
- Short evidence-card captions that restate canonical results with their scope (e.g. "REC exact action match on the frozen diagnostic").
- Navigation microcopy ("On this page", "Research summary →", "Listed after verification").
Please review these if you want headings verbatim from `content/PORTFOLIO_CONTENT.md`.

## Claims changed
None.

## v3.1 — Final polish pass (no redesign)

### Copy changes
- Home evidence card (microstructure): now headlines `83.2%` — "inquiry-breadth policy mismatch on the fresh 5,000-world holdout; stylized exact-model experiments, not an estimate of real-market prevalence" (was a `5,000` environments headline).
- Home background intro: replaced the defensive sentence with "Research affiliation: Independent Researcher."
- Home/About profile cards: "Independent Researcher — The research on this site is conducted independently." / "Education — BS student, Indian Institute of Technology Madras." / "Background — Experience studying and trading financial markets shaped my interest in execution, liquidity, credit constraints, tail risk, and decision-making under uncertainty." Removed "I do not present this as institutional trading employment…".
- About: added "Research affiliation remains Independent Researcher."
- Home: new "Current priority" block (user-supplied copy) + CTA "Research discussion · Reproduction · Collaboration" (also on About contact).
- Writing intro: "Notes on the reasoning behind the research program."
- Manuscripts intro: "Current research manuscripts, each linked to a summary of its question, evidence, and limits."; closing callout "Preprint links will be added here when available."; repeated "manuscripts are not publications" warnings removed.
- REC status: "Research manuscript · 2026."
- "REC reviewer artifact" → "REC paper-scoped offline artifact" (Evidence); "Paper-scoped reviewer artifact…" → "Paper-scoped artifact…" (Manuscripts).

### UI / config changes
- `site.config.json`: single source for `site_url`, `base_path`, contact (GitHub, Email, LinkedIn, arXiv) and artifact URLs. Empty = hidden contact row / disabled "Link pending" artifact button.
- REC, Microstructure, Private Credit: `Evidence / Artifact` and `Code / Reproduce` actions in the hero and in the reproducibility section. AEI has none.
- SEO: canonical URLs, OpenGraph + Twitter tags, `sitemap.xml` and `robots.txt` Sitemap line (when `site_url` set), `noindex` on 404.
- Reduced motion: reveal content is shown immediately (no scroll-gated opacity).

## v3.2 — Pre-deployment micro-fix
- README: configuration section now points to `site.config.json` (`site_url`, `base_path`, `contact.*`, `artifacts.*`); removed stale `SITE_URL` / `BASE_PATH` / `CONTACT_LINKS` in `tools/build.py` instructions.
- About heading: "Enough for scrutiny." → "Public evidence boundary."
- Home background heading: "Research-first, but not context-free." → "Background."
- No other copy, claims, numbers, layout, or AEI content changed.
