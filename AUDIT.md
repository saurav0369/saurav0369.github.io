# Audit report

## Claims audit (against content/PORTFOLIO_CONTENT.md, content/CLAIMS_POLICY.md, original pages)
| Claim on site | Canonical source | Status |
|---|---|---|
| REC 15/15 exact action match, frozen 15-state diagnostic | research/rec.html, PORTFOLIO_CONTENT | verbatim |
| REC ablations 0/6 (timing), 0/6 (consequence) | research/rec.html | verbatim |
| Negative result: exact depth-3 expectimax 27/27; no generic-planner novelty claim | rec.html, evidence.html | verbatim, shown on home, REC, evidence |
| RFQ: 10,080 environments; fresh 5,000 IID holdout; 83.2% inquiry mismatch; 0.0% routing mismatch under common-response control | research/microstructure.html | verbatim; labelled stylized, not leakage frequency |
| Credit: 14/20 nominal-plan failures; 0/20 stressed optimum; 51.3% mean normalized achievable value; 0/20 line-cut control | research/private-credit.html | verbatim; labelled synthetic |
| Credit follow-up: 14/20, 17/20, 40/40; not hash-continuous with original | private-credit.html, evidence.html | verbatim |
| AEI 11/12 vs 0/12; 22/24 vs ≤11/24; 100% controlled crash-rarity (20/5/1%); 41-claim audit | research/aei.html | verbatim; all labelled "internal", synthetic/stylized |
| Status "Research manuscript · 2026"; manuscripts ≠ publications | CLAIMS_POLICY | complied |
| No AISTATS / ICAIF / venue names, no "under review" | CLAIMS_POLICY | grep: 0 occurrences |
| IIT Madras = education; independent affiliation; no sponsorship | CLAIMS_POLICY | complied (home, about, footer) |
| Markets = context; no employment/P&L/AUM claim | CLAIMS_POLICY | complied; grep: 0 occurrences |
| AEI: only framing, thesis, labelled evidence, limits, conceptual pipeline public | CLAIMS_POLICY firewall | complied; private list shown as names only |
| Internally reproducible ≠ independently reproduced; synthetic ≠ prevalence | CLAIMS_POLICY | stated on home, evidence, each page |

## Link audit (`python3 tools/audit_links.py`)
12 pages, 321 internal href/src references, 0 external links, 0 broken files or anchors.

## Responsive audit (`python3 tools/shoot.py`, Chromium)
All 12 pages at 1440×900 (desktop) and 390×844 (mobile), plus dark theme spot checks: 0 horizontal overflow, 0 console/page errors.
- Desktop: two-column hero, sticky TOC sidebar, 4-up evidence grid.
- Breakpoints at 1060 / 960 / 900 / 860 / 760 / 700 / 680px progressively stack the hero, hide the TOC, and reduce grids to 2-up then 1-up.
- ≤760px: hamburger menu (aria-expanded), single-column records, ledger table → labelled cards, figures scale to width.
- `prefers-reduced-motion`: all transitions/SMIL removed, content shown immediately.


## v3.1 final-pass audit
- Links: 12 pages, 321 internal links/anchors OK; 0 external URLs in output (none supplied).
- Browser: all 12 pages at 1440px and 390px (+ dark on 3) — no console/page errors, no horizontal overflow; reduced-motion run on all pages at both widths — all reveal content visible.
- Numbers: every number in src/pages exists in canonical content (scripted check). 83.2% / 5,000 / 10,080 / 0.0% unchanged from canonical.
- Disclosure grep: 0 hits for AISTATS, ICAIF, "under review", "reviewer", submission IDs, accepted/published status.
- IIT Madras: appears only as "Education: BS student" (footer, home, about, meta description).
- AEI: research/aei.html and its diagram unchanged in this pass; no artifact/code buttons.
- SEO verified with a throwaway site_url (sitemap, canonical, robots Sitemap line, contact + active artifact rendering), then config reverted to empty.
