"""Static SVG badge generator — a shields.io-style badge, generated locally
and hosted by whoever runs the tool (no server of ours required). This is
the zero-account distribution mechanic: a site that scores well has a
concrete, embeddable reason to link back, the same way "Deploys on Vercel"
or CI-passing badges spread.
"""
from __future__ import annotations

LABEL = "AI-visible"


def _color_for(score: int) -> str:
    if score >= 80:
        return "#2E8B57"  # allow-green
    if score >= 50:
        return "#E8A23A"  # amber
    return "#C6432E"  # block-red


def _text_width(text: str) -> int:
    # Rough monospace-ish estimate — good enough for a badge, no font
    # metrics library required (this stays stdlib-only by design).
    return max(6, int(len(text) * 6.7)) + 10


def generate_badge_svg(score: int) -> str:
    value_text = f"{score}/100"
    label_text = LABEL
    label_w = _text_width(label_text)
    value_w = _text_width(value_text)
    total_w = label_w + value_w
    color = _color_for(score)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20" role="img" aria-label="{label_text}: {value_text}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#fff" stop-opacity=".08"/>
    <stop offset="1" stop-opacity=".08"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total_w}" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_w}" height="20" fill="#3a3f3c"/>
    <rect x="{label_w}" width="{value_w}" height="20" fill="{color}"/>
    <rect width="{total_w}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{label_w / 2}" y="14">{label_text}</text>
    <text x="{label_w + value_w / 2}" y="14">{value_text}</text>
  </g>
</svg>
'''
