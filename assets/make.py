"""Builds the profile header SVG in a light and a dark version.

Run: python3 assets/make.py   (writes assets/hero-<theme>.svg)
"""
from pathlib import Path

OUT = Path(__file__).parent
W, H = 1200, 400
SANS = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'SF Pro Display', Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, monospace"
MONO_EM = 0.6  # advance width of one monospace glyph, in em

THEMES = {
    "light": dict(bg="#F7F7F4", border="#E3E3DE", text="#141414", muted="#8F8F89", faint="#A6A6A0"),
    "dark": dict(bg="#0E0E0E", border="#242424", text="#EDEDED", muted="#6B6B6B", faint="#5A5A5A"),
}

LABEL = "ROBERT  ·  SAN FRANCISCO"
LINES = ["Robotics. Harnesses.", "GPUs. Compute."]
CMD = "$ research --robotics --harness --gpu --compute"


def mono_len(text, size):
    return round(len(text) * size * MONO_EM, 1)


def hero(t):
    cmd_w = mono_len(CMD, 17)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">
<style>.caret{{animation:blink 1.1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="20" fill="{t['bg']}" stroke="{t['border']}"/>
<text x="64" y="92" font-family="{MONO}" font-size="15" fill="{t['muted']}" textLength="{mono_len(LABEL, 15)}" lengthAdjust="spacing">{LABEL}</text>
<text x="60" y="192" font-size="72" font-weight="600" letter-spacing="-1.6" fill="{t['text']}">{LINES[0]}</text>
<text x="60" y="272" font-size="72" font-weight="600" letter-spacing="-1.6" fill="{t['muted']}">{LINES[1]}</text>
<text x="64" y="342" font-family="{MONO}" font-size="17" fill="{t['faint']}" textLength="{cmd_w}" lengthAdjust="spacing">{CMD}</text>
<rect class="caret" x="{64 + cmd_w + 8}" y="327" width="9" height="19" fill="{t['text']}"/>
</svg>
'''


def main():
    for theme, t in THEMES.items():
        (OUT / f"hero-{theme}.svg").write_text(hero(t), encoding="utf-8")
    print(f"wrote hero-light.svg and hero-dark.svg to {OUT}")


if __name__ == "__main__":
    main()
