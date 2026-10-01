"""Inline SVG diagrams. All diagrams are schematic illustrations of mechanisms
described in the canonical copy; none of them plot experimental data."""


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3))


def hatch(pid):
    return (f'<defs><pattern id="{pid}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="8" style="stroke:var(--accent);stroke-opacity:.18;stroke-width:1"/></pattern></defs>')


def hero():
    shared = ((60, 300), (140, 282), (220, 222), (300, 176))
    a = ((300, 176), (370, 140), (440, 102), (525, 72))
    b = ((300, 176), (372, 158), (432, 232), (525, 332))
    thr = 268
    # crossing of B with threshold
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        if _bez(*b, m)[1] < thr:
            lo = m
        else:
            hi = m
    cx, cy = _bez(*b, lo)
    jit = [6, -5, 3, -7, 5, -3, 7, -4, 2, -6, 4, -2, 6]
    pts = []
    for i, j in enumerate(jit):
        x, y = _bez(*shared, 0.04 + i * 0.077)
        pts.append(f'<circle class="pop f-ink" style="--d:{0.15 + i * 0.07:.2f}s" cx="{x:.1f}" cy="{y + j:.1f}" r="2.6"/>')
    P = lambda c: "M{} {} C {} {}, {} {}, {} {}".format(*[v for p in c for v in p])
    return f'''<svg class="dg" viewBox="0 0 560 400" role="img" aria-labelledby="hero-t hero-d">
<title id="hero-t">Schematic: two mechanisms agree on observed data and diverge in the decision region</title>
<desc id="hero-d">Data points follow a single curve in the observed region. Beyond it, mechanism A rises while mechanism B falls through a feasibility boundary.</desc>
{hatch("h-hero")}
<g class="grid">{"".join(f'<line x1="50" x2="535" y1="{y}" y2="{y}"/>' for y in (60, 120, 180, 240, 300))}</g>
<rect x="50" y="40" width="250" height="310" fill="url(#h-hero)" class="fade" style="--d:.05s"/>
<line class="ax" x1="50" y1="350" x2="535" y2="350"/><line class="ax" x1="50" y1="40" x2="50" y2="350"/>
<line class="ax dash" x1="300" y1="40" x2="300" y2="350"/>
<text x="60" y="30">OBSERVED SO FAR</text><text x="310" y="30">WHERE THE ACTION IS TAKEN</text>
<line class="s-acc dash fade" style="--d:1.6s" x1="50" y1="{thr}" x2="535" y2="{thr}"/>
<text class="t-acc fade" style="--d:1.7s" x="438" y="{thr + 16}" text-anchor="end">FEASIBILITY BOUNDARY</text>
{"".join(pts)}
<path class="s-ink draw" style="--d:.2s" pathLength="1" d="{P(shared)}"/>
<path id="mechB" class="s-ink draw" style="--d:1.25s" pathLength="1" d="{P(b)}"/>
<path class="s-mut draw" style="--d:1.25s" pathLength="1" d="{P(a)}"/>
<text class="t-serif fade" style="--d:2.2s" x="440" y="70">Mechanism A</text>
<text class="t-serif fade" style="--d:2.2s" x="420" y="342">Mechanism B</text>
<circle class="f-acc pulse" style="--d:2.6s" cx="{cx:.1f}" cy="{cy:.1f}" r="7" opacity="0"/>
<circle class="f-acc pop" style="--d:2.4s" cx="{cx:.1f}" cy="{cy:.1f}" r="4.5"/>
<text class="t-acc fade" style="--d:2.5s" x="{cx - 14:.1f}" y="{cy + 34:.1f}" text-anchor="end">action infeasible under B</text>
<circle r="4" class="f-bg" style="stroke:var(--ink);stroke-width:1.5" opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.92;1" dur="7s" begin="3s" repeatCount="indefinite"/><animateMotion dur="7s" begin="3s" repeatCount="indefinite" path="{P(shared)} {P(b).split(' ', 2)[2]}"/></circle>
<text x="535" y="370" text-anchor="end">STATE / EXPOSURE →</text>
</svg>'''


def rec():
    xs = [80 + i * 120 for i in range(7)]
    bx = xs[4]
    out = [f'<svg class="dg" viewBox="0 0 900 300" role="img" aria-labelledby="rec-t rec-d"><title id="rec-t">Schematic: probing early versus probing at the boundary</title>'
           '<desc id="rec-d">Two lanes of decision states. In lane A information is acquired early and the consequence changes all later states. In lane B acquisition is delayed until the probe boundary.</desc>']
    out.append(f'<line class="s-acc dash fade" style="--d:.1s" x1="{bx}" y1="40" x2="{bx}" y2="275"/><text class="t-acc fade" style="--d:.2s" x="{bx + 8}" y="40">PROBE BOUNDARY</text>')
    # lane A
    ya, yb = 115, 225
    out.append(f'<text x="40" y="{ya - 34}" class="t-ink">A · PROBE EARLY</text><text x="40" y="{yb - 34}" class="t-ink">B · PROBE AT THE BOUNDARY</text>')
    out.append(f'<line class="s-ink draw" pathLength="1" style="--d:.2s" x1="{xs[0]}" y1="{ya}" x2="{xs[1]}" y2="{ya}"/>')
    out.append(f'<path class="s-acc dash fade" style="--d:1.1s" d="M{xs[1]} {ya} C {xs[1]+60} {ya-26}, {xs[2]-60} {ya+26}, {xs[2]} {ya} S {xs[3]-60} {ya+26}, {xs[3]} {ya} S {xs[5]-60} {ya+26}, {xs[6]} {ya}"/>')
    for i, x in enumerate(xs):
        if i <= 1:
            out.append(f'<circle class="pop f-ink" style="--d:{.2+i*.1:.1f}s" cx="{x}" cy="{ya}" r="6"/>')
        else:
            out.append(f'<circle class="pop f-bg" style="--d:{1.2+i*.12:.2f}s;stroke:var(--accent);stroke-width:1.5" cx="{x}" cy="{ya}" r="6"/>')
    out.append(f'<rect class="pop f-acc" style="--d:.8s" x="{xs[1]-7}" y="{ya-31}" width="14" height="14" transform="rotate(45 {xs[1]} {ya-24})"/>')
    out.append(f'<text class="t-acc fade" style="--d:.9s" x="{xs[1]+16}" y="{ya-20}">acquire now</text>')
    out.append(f'<text class="fade" style="--d:1.8s" x="{xs[2]}" y="{ya+40}">consequence propagates: dynamics, constraints, costs, feasible actions change</text>')
    # lane B
    out.append(f'<line class="s-ink draw" pathLength="1" style="--d:.3s" x1="{xs[0]}" y1="{yb}" x2="{xs[6]}" y2="{yb}"/>')
    for i, x in enumerate(xs):
        out.append(f'<circle class="pop f-ink" style="--d:{.3+i*.12:.2f}s" cx="{x}" cy="{yb}" r="6"/>')
    out.append(f'<rect class="pop f-acc" style="--d:1.5s" x="{bx-7}" y="{yb-31}" width="14" height="14" transform="rotate(45 {bx} {yb-24})"/>')
    out.append(f'<text class="t-acc fade" style="--d:1.6s" x="{bx+16}" y="{yb-20}">acquire at boundary</text>')
    for y in (ya, yb):
        out.append(f'<circle r="9" fill="none" style="stroke:var(--ink);stroke-width:1.2" opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.06;.94;1" dur="6s" begin="2.2s" repeatCount="indefinite"/><animateMotion dur="6s" begin="2.2s" repeatCount="indefinite" path="M{xs[0]} {y} L{xs[6]} {y}"/></circle>')
    out.append(f'<text x="{xs[0]}" y="290">STATE 1</text><text x="{xs[6]}" y="290" text-anchor="end">STATE 7 · TIME →</text></svg>')
    return "".join(out)


def micro():
    def panel(ox, title, sub, endo):
        tx, ty = ox + 50, 175
        ys = [70, 138, 206, 274]
        dx = ox + 230
        c0 = [70, 46, 58, 84]
        c1 = [96, 88, 60, 104]
        best0, best1 = 1, 2
        s = [f'<text x="{ox}" y="22" class="t-ink">{title}</text><text x="{ox}" y="40">{sub}</text>']
        s.append(f'<circle class="pop f-ink" style="--d:.1s" cx="{tx}" cy="{ty}" r="14"/><text x="{tx}" y="{ty + 34}" text-anchor="middle">TRADER</text>')
        for k, y in enumerate(ys):
            path = f"M{tx + 14} {ty} L{dx - 8} {y}"
            s.append(f'<path class="s-mut draw" pathLength="1" style="--d:{.2 + k * .08:.2f}s" d="{path}"/>')
            s.append(f'<circle r="3" class="f-acc" opacity="0"><animate attributeName="opacity" values="0;1;0" dur="2.4s" begin="{.8 + k * .12:.2f}s" repeatCount="indefinite"/><animateMotion dur="2.4s" begin="{.8 + k * .12:.2f}s" repeatCount="indefinite" path="{path}"/></circle>')
            s.append(f'<rect class="pop f-bg" style="--d:{.3 + k * .08:.2f}s;stroke:var(--ink);stroke-width:1.3" x="{dx - 8}" y="{y - 8}" width="16" height="16"/>')
            s.append(f'<text x="{dx}" y="{y - 14}" text-anchor="middle">D{k + 1}</text>')
            w0 = c0[k]
            if endo:
                sc = c1[k] / c0[k]
                s.append(f'<rect class="grow" style="--s:{sc:.3f};--d:{1.6 + k * .1:.2f}s;fill:var(--faint)" x="{dx + 18}" y="{y - 5}" width="{w0}" height="10"/>')
            else:
                s.append(f'<rect class="fade" style="--d:{.6 + k * .1:.2f}s;fill:var(--faint)" x="{dx + 18}" y="{y - 5}" width="{w0}" height="10"/>')
        if endo:
            s.append(f'<path class="s-acc fadeout" style="stroke-width:2.4;--d:2.3s" d="M{tx + 14} {ty} L{dx - 8} {ys[best0]}"/>')
            s.append(f'<path class="s-acc fade" style="stroke-width:2.4;--d:2.6s" d="M{tx + 14} {ty} L{dx - 8} {ys[best1]}"/>')
            s.append(f'<text class="t-acc fade" style="--d:2.8s" x="{ox}" y="330">route changes → passive and endogenous are not equivalent</text>')
        else:
            s.append(f'<path class="s-acc fade" style="stroke-width:2.4;--d:1.2s" d="M{tx + 14} {ty} L{dx - 8} {ys[best0]}"/>')
            s.append(f'<text class="fade" style="--d:1.4s" x="{ox}" y="330">quotes held fixed while information is valued</text>')
        s.append(f'<text x="{dx + 18}" y="58">QUOTED COST</text>')
        return "".join(s)
    body = panel(20, "PASSIVE VALUE OF INFORMATION", "downstream execution held fixed", False) + \
        '<line class="ax dash" x1="455" y1="10" x2="455" y2="335"/>' + \
        panel(490, "ENDOGENOUS VALUE OF INFORMATION", "inquiry changes downstream action values", True)
    return ('<svg class="dg" viewBox="0 0 900 345" role="img" aria-labelledby="mi-t mi-d"><title id="mi-t">Schematic: passive versus endogenous value of information in RFQ execution</title>'
            '<desc id="mi-d">Left: a trader requests quotes from four dealers and quotes stay fixed. Right: the inquiry changes dealer quotes and the best route switches to a different dealer.</desc>'
            + body + '</svg>')


def credit():
    x0, x1, yT = 80, 860, 228
    n = 8
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    nominal = [150, 138, 160, 186, 208, 196, 172, 158]
    shocked = [150, 156, 192, 230, 266, 254, 226, 206]
    opt = [150, 132, 146, 164, 186, 178, 160, 148]

    def pth(v):
        return "M" + " L".join(f"{x:.0f} {y}" for x, y in zip(xs, v))
    s = ['<svg class="dg" viewBox="0 0 900 340" role="img" aria-labelledby="pc-t pc-d"><title id="pc-t">Schematic: an omitted stress mechanism moves a reached feasibility boundary</title>'
         '<desc id="pc-d">A nominal cash plan stays above a minimum-cash constraint. Under an omitted working-capital drain the same plan falls through the constraint, while a stressed optimum remains feasible.</desc>',
         hatch("h-pc")]
    s.append('<g class="grid">' + "".join(f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}"/>' for y in (100, 150, 200, 250, 300)) + '</g>')
    s.append(f'<rect x="{x0}" y="{yT}" width="{x1 - x0}" height="{300 - yT}" fill="url(#h-pc)" class="fade" style="--d:.1s"/>')
    s.append(f'<line class="s-acc" x1="{x0}" y1="{yT}" x2="{x1}" y2="{yT}"/><text class="t-acc" x="{x0 + 6}" y="{yT + 18}">MINIMUM-CASH CONSTRAINT · INFEASIBLE BELOW</text>')
    s.append(f'<line class="ax" x1="{x0}" y1="300" x2="{x1}" y2="300"/><line class="ax" x1="{x0}" y1="60" x2="{x0}" y2="300"/>')
    for i, x in enumerate(xs):
        s.append(f'<text x="{x:.0f}" y="320" text-anchor="middle">T{i + 1}</text>')
    s.append(f'<text x="{x0 - 10}" y="70" text-anchor="end">CASH</text>')
    s.append(f'<path class="s-ink draw" pathLength="1" style="--d:.2s" d="{pth(nominal)}"/>')
    s.append(f'<path class="s-ink draw dash-solid" pathLength="1" style="--d:1.3s;stroke-width:2.2" d="{pth(shocked)}"/>')
    s.append(f'<path class="s-mut dash fade" style="--d:2.6s;stroke:var(--ok);stroke-width:1.8" d="{pth(opt)}"/>')
    fx = xs[4]
    s.append(f'<g class="pop" style="--d:2.2s"><line x1="{fx - 7}" y1="{266 - 7}" x2="{fx + 7}" y2="{266 + 7}" class="s-acc" style="stroke-width:2.4"/><line x1="{fx + 7}" y1="{266 - 7}" x2="{fx - 7}" y2="{266 + 7}" class="s-acc" style="stroke-width:2.4"/></g>')
    s.append(f'<circle class="f-acc pulse" style="--d:2.4s" cx="{fx:.0f}" cy="266" r="8" opacity="0"/>')
    s.append(f'<text class="t-acc fade" style="--d:2.3s" x="{fx + 16:.0f}" y="286">constraint failure</text>')
    # legend
    lg = [("s-ink", "", "nominal plan, encoded model"), ("s-ink", "stroke-width:2.6", "same plan + omitted working-capital drain"), ("s-mut dash", "stroke:var(--ok);stroke-width:1.8", "exact stressed optimum")]
    for k, (c, st, t) in enumerate(lg):
        y = 26 + k * 0
        x = (60, 300, 640)[k]
        s.append(f'<line class="{c}" style="{st}" x1="{x}" y1="26" x2="{x + 26}" y2="26"/><text x="{x + 34}" y="30">{t}</text>')
    s.append('</svg>')
    return "".join(s)


# ---------- small record glyphs (decorative, aria-hidden) ----------
def glyph(kind):
    head = '<svg class="dg" viewBox="0 0 220 140" aria-hidden="true" focusable="false">'
    if kind == "rec":
        xs = [20 + i * 36 for i in range(6)]
        g = [f'<line class="s-acc dash" x1="{xs[4]}" y1="14" x2="{xs[4]}" y2="128"/>',
             f'<line class="s-ink draw" pathLength="1" x1="{xs[0]}" y1="46" x2="{xs[1]}" y2="46"/>',
             f'<path class="s-acc dash fade" style="--d:.6s" d="M{xs[1]} 46 Q {xs[1] + 18} 30 {xs[2]} 46 T {xs[3]} 46 T {xs[5]} 46"/>',
             f'<line class="s-ink draw" pathLength="1" style="--d:.2s" x1="{xs[0]}" y1="100" x2="{xs[5]}" y2="100"/>']
        g += [f'<circle class="pop {"f-ink" if i < 2 else "f-bg"}" style="--d:{.1 * i:.1f}s;{"" if i < 2 else "stroke:var(--accent);stroke-width:1.3"}" cx="{x}" cy="46" r="4.5"/>' for i, x in enumerate(xs)]
        g += [f'<circle class="pop f-ink" style="--d:{.1 * i + .2:.1f}s" cx="{x}" cy="100" r="4.5"/>' for x in xs for i in [xs.index(x)]]
        g += [f'<rect class="pop f-acc" style="--d:.5s" x="{xs[1] - 5}" y="26" width="10" height="10" transform="rotate(45 {xs[1]} 31)"/>',
              f'<rect class="pop f-acc" style="--d:.9s" x="{xs[4] - 5}" y="80" width="10" height="10" transform="rotate(45 {xs[4]} 85)"/>']
    elif kind == "micro":
        ys = [24, 56, 88, 120]
        g = ['<circle class="pop f-ink" cx="34" cy="72" r="9"/>']
        for k, y in enumerate(ys):
            p = f"M43 72 L150 {y}"
            g.append(f'<path class="s-mut draw" pathLength="1" style="--d:{k * .08:.2f}s" d="{p}"/>')
            g.append(f'<circle r="2.5" class="f-acc" opacity="0"><animate attributeName="opacity" values="0;1;0" dur="2.2s" begin="{k * .15:.2f}s" repeatCount="indefinite"/><animateMotion dur="2.2s" begin="{k * .15:.2f}s" repeatCount="indefinite" path="{p}"/></circle>')
            g.append(f'<rect class="pop f-bg" style="--d:{.2 + k * .08:.2f}s;stroke:var(--ink);stroke-width:1.2" x="146" y="{y - 5}" width="10" height="10"/>')
            g.append(f'<rect class="grow" style="--s:{[1.3, 1.6, 1.0, 1.25][k]};--d:{.8 + k * .1:.1f}s;fill:var(--faint)" x="164" y="{y - 3}" width="{[26, 18, 22, 30][k]}" height="6"/>')
        g.append('<path class="s-acc fade" style="--d:1.4s;stroke-width:2" d="M43 72 L146 88"/>')
    elif kind == "credit":
        xs = [16 + i * 27 for i in range(8)]
        v = [40, 36, 52, 74, 104, 96, 80, 70]
        o = [40, 32, 40, 50, 64, 60, 52, 46]
        g = [hatch("h-g"), '<rect x="10" y="90" width="200" height="40" fill="url(#h-g)"/>', '<line class="s-acc" x1="10" y1="90" x2="210" y2="90"/>',
             '<path class="s-ink draw" pathLength="1" style="stroke-width:2" d="M' + " L".join(f"{x} {y}" for x, y in zip(xs, v)) + '"/>',
             '<path class="s-mut dash fade" style="--d:1s;stroke:var(--ok)" d="M' + " L".join(f"{x} {y}" for x, y in zip(xs, o)) + '"/>',
             f'<g class="pop" style="--d:1.2s"><line class="s-acc" style="stroke-width:2" x1="{xs[4] - 5}" y1="99" x2="{xs[4] + 5}" y2="109"/><line class="s-acc" style="stroke-width:2" x1="{xs[4] + 5}" y1="99" x2="{xs[4] - 5}" y2="109"/></g>']
    else:  # aei
        xs = [22 + i * 35 for i in range(6)]
        g = [hatch("h-a"), '<rect x="8" y="88" width="204" height="40" fill="url(#h-a)" style="stroke:var(--line-2);stroke-dasharray:3 4"/>',
             '<line class="ax" x1="22" y1="48" x2="197" y2="48"/>',
             '<line class="s-acc draw" pathLength="1" style="stroke-width:1.8;--d:.1s" x1="22" y1="48" x2="197" y2="48"/>']
        g += [f'<circle class="pop f-ink" style="--d:{i * .18:.2f}s" cx="{x}" cy="48" r="5"/>' for i, x in enumerate(xs)]
        g += ['<circle r="3.5" class="f-acc"><animateMotion dur="3.2s" repeatCount="indefinite" path="M22 48 L197 48"/></circle>']
        g += [f'<line class="s-mut dash" x1="{x}" y1="54" x2="{x}" y2="88"/>' for x in xs[1:5]]
    return head + "".join(g) + "</svg>"
