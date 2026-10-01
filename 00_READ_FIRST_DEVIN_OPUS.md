# Devin + Opus UI Handoff — READ FIRST

## Objective
Redesign and implement Saurav Sharma's public research portfolio as a high-end, modern, researcher/founder-grade website while preserving the existing content, claims boundaries, anonymity constraints, and AEI IP firewall.

This is primarily a UI/UX + frontend implementation task. Do not rewrite the research claims from memory. Treat the content files in `content/` as canonical.

## Canonical reading order
1. `content/PORTFOLIO_CONTENT.md`
2. `content/CLAIMS_POLICY.md`
3. `index.html`
4. `research/rec.html`
5. `research/microstructure.html`
6. `research/private-credit.html`
7. `research/aei.html`
8. `evidence.html`
9. `manuscripts.html`
10. `about.html`
11. `writing/why-prediction-is-not-enough.html`

## Immutable positioning
Primary identity:
**Saurav Sharma — Independent Researcher & Technical Builder**

Research focus:
**Reliable decision-making under hidden mechanisms, consequential information acquisition, binding constraints, and rare failures.**

Research-first, not research-only.
- IIT Madras appears under Education/background only.
- Research affiliation is Independent Researcher.
- Markets/trading experience is background context and motivation, not the headline credential.
- Do not imply IIT Madras sponsored, supervised, or endorsed the research.
- Do not imply institutional/professional trading employment, audited P&L, AUM, or similar unsupported claims.

## Blind-review / status rules
- Do NOT publicly write `AISTATS 2027 under review` for REC while blind review is active.
- Do NOT use ICAIF workshop names as public prestige signals before anonymity concerns are resolved.
- Public wording: `Research manuscript, 2026`.
- `manuscript` is not `publication`.

## AEI disclosure firewall
Publicly allowed:
- problem framing
- high-level research thesis
- selected safe evidence
- evidence limitations
- broad conceptual pipeline

Keep private:
- exact identification machinery
- probing/acquisition policies
- architecture-selection details
- successor architecture/design
- reconstruction-grade source
- full private evaluation suite

Do not introduce new AEI implementation details.

## Evidence language
- `internally reproducible` != `independently reproduced`
- synthetic mechanism tests != real-world prevalence estimates
- show retained negative results prominently
- do not exaggerate peer-review status
- do not add performance claims that are not already present in canonical content

## Design goal
The site should feel like a high-end independent AI researcher / technical founder portfolio, not:
- a student template
- a startup marketing landing page
- a crypto/AI neon site
- an academic department page from 2015
- a generic GitHub Pages theme

Desired impression in 60 seconds:
1. serious independent researcher
2. coherent multi-project research program
3. unusual experimental rigor and self-falsification
4. economic/market intuition
5. larger private AEI program behind the public branches
6. clear evidence boundaries and no hype

## Visual direction
Use restrained, premium, editorial/scientific design:
- strong typography and hierarchy
- generous but controlled whitespace
- dark or off-white neutral palette with one restrained accent
- subtle motion only where it improves comprehension
- responsive mobile design
- no excessive gradients, glassmorphism, glowing blobs, generic AI imagery, stock photos, or ornamental 3D
- data/evidence should be visually scannable
- research cards should look like serious project records, not SaaS feature cards

Possible reference language: Linear / Vercel-level finish + top independent researcher site + editorial research journal. Do not copy any brand literally.

## Homepage information architecture
Recommended order:
1. Hero — identity + one-line research focus + concise background chips
2. Flagship research — REC, microstructure, private credit
3. AEI — broader private research program
4. Evidence standards / reproducibility / negative results
5. Background — IIT Madras education + markets experience
6. Writing
7. Contact / GitHub

The homepage should not expose every result. It should create a clear path into project pages.

## Flagship project pages
Keep a common structure:
- Question
- Core idea
- Selected result(s)
- Experimental design
- Strongest attack/control or negative result
- What it establishes
- What it does not establish
- Evidence / artifact status
- Back to research

## Implementation requirements
- Static site deployable on GitHub Pages.
- Prefer simple, maintainable HTML/CSS/JS or a static framework only if it materially improves quality and build reliability.
- If migrating to React/Astro/Next static export, ensure GitHub Pages deployment works without server dependencies.
- No backend required.
- Preserve all existing URLs or add redirects if paths change.
- SEO/title/description/OG metadata for major pages.
- Semantic HTML and accessible contrast/focus states.
- Mobile-first responsive behavior.
- Fast load; avoid heavy animation libraries unless justified.
- No external analytics unless explicitly requested.
- Keep content separable from presentation so future copy changes are easy.

## Deliverables
1. redesigned site source
2. deploy instructions for GitHub Pages
3. concise CHANGELOG of content changes vs UI-only changes
4. screenshot(s) of desktop and mobile home page
5. link audit and responsive audit
6. list any claims you changed — ideally NONE without explicit approval

## Non-goals
- Do not write the EV application.
- Do not rewrite AEI architecture.
- Do not invent awards, acceptances, affiliations, publications, citations, job titles, or trading credentials.
- Do not make venue-under-review labels public.
- Do not optimize for flashy animations over credibility.

## Final acceptance test
Before finishing, ask:
- Could a technical referee understand the research program in under 3 minutes?
- Could an EV-style grant reviewer understand why the applicant is unusual in under 60 seconds?
- Is every strong claim traceable to the canonical copy rather than invented?
- Does the site distinguish internal reproducibility from external validation?
- Does the site keep AEI reconstructive IP private?
- Does the design feel senior and credible rather than student-made?

If any answer is no, iterate before declaring the task complete.
