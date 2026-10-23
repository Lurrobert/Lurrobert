"""Builds the profile's SVG cards in a light and a dark version.

Run: python3 assets/make.py   (writes assets/<card>-<theme>.svg)
"""
from pathlib import Path

OUT = Path(__file__).parent
W = 1200
SANS = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'SF Pro Display', Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, monospace"
MONO_EM = 0.6  # advance width of one monospace glyph, in em
GRAD = ["#0894FF", "#C959DD", "#FF2E54", "#FF9004"]

THEMES = {
    "light": dict(bg="#FBFBFA", tile="#FFFFFF", border="#E6E6E3", text="#191919", muted="#6F6E69",
                  faint="#A3A29D", dot="#DCDCD8", glow=0.20),
    "dark": dict(bg="#0A0A0B", tile="#121214", border="#232326", text="#F5F5F7", muted="#8E8E93",
                 faint="#5C5C62", dot="#1E1E22", glow=0.34),
}

STATS = [
    ("STORMY.AI", "$250k", "ARR, scaled solo"),
    ("FOUNDER", "YC", "Y Combinator"),
    ("VIRAL DEMOS", "1.38M", "views across 7 launches"),
    ("OPEN SOURCE", "788", "GitHub stars on 3 repos"),
]

# (number, label, title, body lines, icon, wide)
FOCUS = [
    ("01", "ROBOTICS", "Robots that do real, paid work.",
     ["Sim first, then real arms, grippers and cameras.",
      "An AI runs the rig, predicts each result, then measures it."], "arm", True),
    ("02", "HARNESS", "Models → workers",
     ["Tools, memory, evals and", "sandboxes around the model."], "orbit", False),
    ("03", "GPU", "Close to the metal",
     ["Kernels, benchmarks and", "profiling. Real speed, measured."], "chip", False),
    ("04", "COMPUTE", "Infra for intelligence.",
     ["Scheduling, inference cost and scale for GPU fleets.",
      "Where the next 100x comes from, measured, not guessed."], "rack", True),
]

LINKS = [
    ("x", "@Karmedge on X", 210),
    ("linkedin", "LinkedIn", 150),
    ("telegram", "Telegram", 150),
    ("stormy", "stormy.ai", 150),
]


def mono_len(text, size):
    return round(len(text) * size * MONO_EM, 1)


def defs(extra=""):
    stops = "".join(f'<stop offset="{i / (len(GRAD) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(GRAD))
    return f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>{extra}</defs>'


def svg(h, body, extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
            f'font-family="{SANS}">{defs(extra_defs)}{body}</svg>\n')


def hero(t):
    h = 540
    pill = "ROBERT  ·  YC FOUNDER  ·  SAN FRANCISCO"
    pill_w = mono_len(pill, 14) + 64
    cmd = "$ focus --robotics --harness --gpu --compute"
    cmd_w = mono_len(cmd, 16)
    cmd_x = (W - cmd_w - 18) / 2
    extra = f'''
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{t['dot']}"/></pattern>
<radialGradient id="fade" cx="50%" cy="40%" r="62%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="m"><rect width="{W}" height="{h}" fill="url(#fade)"/></mask>
<filter id="blur" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="70"/></filter>
<clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="28"/></clipPath>
<style>.caret{{animation:blink 1.1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}</style>'''
    body = f'''
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="28" fill="{t['bg']}" stroke="{t['border']}"/>
<g clip-path="url(#card)">
  <rect width="{W}" height="{h}" fill="url(#dots)" mask="url(#m)"/>
  <ellipse cx="600" cy="{h + 40}" rx="460" ry="110" fill="url(#g)" filter="url(#blur)" opacity="{t['glow']}">
    <animate attributeName="opacity" values="{t['glow']};{t['glow'] * 1.6:.2f};{t['glow']}" dur="7s" repeatCount="indefinite"/>
  </ellipse>
</g>
<rect x="{(W - pill_w) / 2}" y="66" width="{pill_w}" height="36" rx="18" fill="{t['tile']}" stroke="{t['border']}"/>
<circle cx="{(W - pill_w) / 2 + 22}" cy="84" r="4.5" fill="url(#g)"/>
<text x="{(W - pill_w) / 2 + 40}" y="88.5" font-family="{MONO}" font-size="14" fill="{t['muted']}"
  textLength="{mono_len(pill, 14)}" lengthAdjust="spacing">{pill}</text>
<text x="600" y="214" text-anchor="middle" font-size="84" font-weight="700" letter-spacing="-3.2" fill="{t['text']}">Robotics. Harnesses.</text>
<text x="600" y="306" text-anchor="middle" font-size="84" font-weight="700" letter-spacing="-3.2" fill="url(#g)">GPUs. Compute.</text>
<text x="600" y="378" text-anchor="middle" font-size="24" fill="{t['muted']}">YC founder. I scaled stormy.ai to $250k ARR, solo.</text>
<text x="600" y="412" text-anchor="middle" font-size="24" fill="{t['muted']}">Now I research the infra under intelligence.</text>
<text x="{cmd_x}" y="474" font-family="{MONO}" font-size="16" fill="{t['faint']}"
  textLength="{cmd_w}" lengthAdjust="spacing">{cmd}</text>
<rect class="caret" x="{cmd_x + cmd_w + 8}" y="460" width="9" height="18" rx="1.5" fill="url(#g)"/>'''
    return svg(h, body, extra)


def stats(t):
    h, gap = 176, 16
    tw = (W - gap * (len(STATS) - 1)) / len(STATS)
    tiles = []
    for i, (label, number, caption) in enumerate(STATS):
        x = i * (tw + gap)
        fill = "url(#g)" if i == 0 else t["text"]
        tiles.append(f'''
<g transform="translate({x:.2f} 0)">
  <rect x="0.5" y="0.5" width="{tw - 1:.2f}" height="{h - 1}" rx="20" fill="{t['tile']}" stroke="{t['border']}"/>
  <text x="26" y="42" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{t['faint']}">{label}</text>
  <text x="24" y="112" font-size="56" font-weight="700" letter-spacing="-2.2" fill="{fill}">{number}</text>
  <text x="26" y="148" font-size="18" fill="{t['muted']}">{caption}</text>
</g>''')
    return svg(h, "".join(tiles))


def icon(kind, t):
    s = f'fill="none" stroke="{t["text"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "arm":
        return f'''<g {s}>
  <rect x="6" y="46" width="26" height="6" rx="2"/><path d="M19 46V33"/><path d="M21.5 28.5L35 17"/>
  <path d="M41 16L48 23M48 23L53 19M48 23L50 29"/></g>
<circle cx="19" cy="30.5" r="3.4" fill="url(#g)"/><circle cx="38" cy="14.5" r="3.4" fill="url(#g)"/>'''
    if kind == "chip":
        pins = "".join(f'<path d="M{18 + i * 7} 4V11M{18 + i * 7} 45V52M4 {18 + i * 7}H11M45 {18 + i * 7}H52"/>' for i in range(3))
        return f'''<g {s}><rect x="11" y="11" width="34" height="34" rx="7"/>{pins}</g>
<rect x="20" y="20" width="16" height="16" rx="3.5" fill="url(#g)"/>'''
    if kind == "orbit":
        nodes = "".join(f'<circle cx="{cx}" cy="{cy}" r="3.6" fill="{t["tile"]}"/>' for cx, cy in ((48, 28), (18, 45.3), (18, 10.7)))
        return f'''<g {s}><circle cx="28" cy="28" r="20" stroke-dasharray="3 4.5"/>{nodes}</g>
<circle cx="28" cy="28" r="7.5" fill="url(#g)"/>'''
    rows = "".join(f'<rect x="7" y="{y}" width="42" height="11" rx="3.5"/><path d="M13 {y + 5.5}H25"/>' for y in (9, 22.5, 36))
    dots = "".join(f'<circle cx="42" cy="{y + 5.5}" r="2" fill="url(#g)"/>' for y in (9, 22.5, 36))
    return f'<g {s}>{rows}</g>{dots}'


def decoration(kind, tw, t):
    if kind == "arm":
        steps, x, out = ["simulate", "predict", "measure"], tw - 28, []
        widths = [mono_len(s, 13) + 28 for s in steps]
        x -= sum(widths) + 2 * 34
        for i, (step, w) in enumerate(zip(steps, widths)):
            stroke = "url(#g)" if i == len(steps) - 1 else t["border"]
            out.append(f'<rect x="{x:.1f}" y="104" width="{w:.1f}" height="32" rx="16" fill="{t["bg"]}" stroke="{stroke}"/>'
                       f'<text x="{x + 14:.1f}" y="124.5" font-family="{MONO}" font-size="13" fill="{t["muted"]}" '
                       f'textLength="{mono_len(step, 13)}" lengthAdjust="spacing">{step}</text>')
            x += w
            if i < len(steps) - 1:
                out.append(f'<path d="M{x + 9:.1f} 120H{x + 25:.1f}M{x + 20:.1f} 115L{x + 25:.1f} 120L{x + 20:.1f} 125" '
                           f'fill="none" stroke="{t["faint"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
                x += 34
        return "".join(out)
    if kind == "rack":
        n, bw, bg = 14, 13, 7
        x0 = tw - 28 - n * bw - (n - 1) * bg
        bars = []
        for i in range(n):
            bh = 6 + 58 * (1.32 ** i - 1) / (1.32 ** (n - 1) - 1)
            bars.append(f'<rect x="{x0 + i * (bw + bg):.1f}" y="{156 - bh:.1f}" width="{bw}" height="{bh:.1f}" rx="3" '
                        f'fill="url(#g)" opacity="{0.25 + 0.75 * i / (n - 1):.2f}"/>')
        return "".join(bars)
    return ""


def focus(t):
    gap, th = 16, 280
    narrow = (W - 2 * gap) / 3
    wide = 2 * narrow + gap
    h = 2 * th + gap
    slots = [(0, 0, wide), (wide + gap, 0, narrow), (0, th + gap, narrow), (narrow + gap, th + gap, wide)]
    tiles = []
    for (num, label, title, lines, kind, _), (x, y, tw) in zip(FOCUS, slots):
        body = "".join(f'<text x="28" y="{218 + i * 28}" font-size="19" fill="{t["muted"]}">{line}</text>' for i, line in enumerate(lines))
        tiles.append(f'''
<g transform="translate({x:.2f} {y})">
  <rect x="0.5" y="0.5" width="{tw - 1:.2f}" height="{th - 1}" rx="22" fill="{t['tile']}" stroke="{t['border']}"/>
  <text x="28" y="48" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{t['faint']}">{num}  {label}</text>
  <g transform="translate({tw - 84:.2f} 24)">{icon(kind, t)}</g>
  {decoration(kind, tw, t)}
  <text x="28" y="188" font-size="28" font-weight="650" letter-spacing="-0.8" fill="{t['text']}">{title}</text>
  {body}
</g>''')
    return svg(h, "".join(tiles))


def link_pill(text, w, t):
    h = 44
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{SANS}">'
            f'{defs()}<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" fill="{t["tile"]}" stroke="{t["border"]}"/>'
            f'<circle cx="22" cy="22" r="4" fill="url(#g)"/>'
            f'<text x="{(w + 18) / 2}" y="27.5" text-anchor="middle" font-size="15" font-weight="500" fill="{t["text"]}">{text}</text></svg>\n')


def main():
    for theme, t in THEMES.items():
        cards = {"hero": hero(t), "stats": stats(t), "focus": focus(t)}
        cards.update({f"link-{key}": link_pill(text, w, t) for key, text, w in LINKS})
        for name, content in cards.items():
            (OUT / f"{name}-{theme}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} svgs to {OUT}")


if __name__ == "__main__":
    main()
