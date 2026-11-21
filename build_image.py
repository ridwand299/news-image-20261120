"""Sum up 20 November 2026 world news in one image.

Deterministic, offline, no network, no clock, no randomness.
Writes one 1024x1024 PNG to /output/entry.png when /output exists,
otherwise to entry.png next to this file. Both runs write identical bytes.
Requires only Pillow (present in the make.fun Python 3.13 runtime image
via the standard library + Pillow; fonts are DejaVu, bundled here by path
with a Pillow-default fallback).
"""
import os
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (11, 18, 42)          # dark navy
PANEL = (21, 32, 64)
GOLD = (245, 184, 65)
WHITE = (255, 255, 255)
MUTED = (203, 213, 225)
CHIPS = [(245, 184, 65), (56, 189, 248), (52, 211, 153), (244, 114, 182), (167, 139, 250)]

STORIES = [
    ("01", "SHENZHEN SUMMIT",
     "Trump, Xi and Putin issue a joint peace declaration",
     "Three nuclear powers agree further nuclear-risk talks."),
    ("02", "UKRAINE",
     "Russia fires 400+ drones and 110 missiles at Kyiv",
     "8 killed, ~30 hurt; two missiles also fall in Poland."),
    ("03", "JUSTICE",
     "ICJ: Myanmar responsible for genocide of the Rohingya",
     "Landmark ICJ ruling on Myanmar and the Rohingya."),
    ("04", "EUROPE",
     "EU-UK summit in Brussels; Germany rejects a Yalta deal",
     "Europe insists on a seat at the table on Ukraine."),
    ("05", "TECH & MARKETS",
     "Anthropic's record IPO; US Senate passes energy bill",
     "Record Nasdaq debut; California subpoenas Nvidia."),
]


def _font(bold, size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render():
    # Deterministic render: fixed 1024x1024 canvas, fixed DejaVu fonts,
    # colours, story text and layout; no clock, network, or randomness,
    # so re-running produces a byte-identical PNG.
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_title = _font(True, 56)
    f_sub = _font(True, 26)
    f_tag = _font(True, 22)
    f_head = _font(True, 28)
    f_body = _font(False, 21)
    f_num = _font(True, 38)
    f_foot = _font(False, 19)

    # Header
    d.text((56, 28), "20 NOVEMBER 2026", font=f_title, fill=WHITE)
    d.text((56, 96), "THE WORLD IN ONE IMAGE", font=f_sub, fill=GOLD)
    d.rectangle([56, 132, 968, 136], fill=GOLD)

    # Five stories
    y = 150
    row_h, gap = 156, 10
    for i, (num, tag, head, body) in enumerate(STORIES):
        d.rounded_rectangle([56, y, 968, y + row_h], radius=14, fill=PANEL)
        d.rectangle([56, y + 14, 66, y + row_h - 14], fill=CHIPS[i])
        d.text((88, y + 18), num, font=f_num, fill=CHIPS[i])
        d.text((168, y + 20), tag, font=f_tag, fill=CHIPS[i])
        head_lines = _wrap(d, head, f_head, 968 - 168 - 24)
        hy = y + 48
        for line in head_lines[:2]:
            d.text((168, hy), line, font=f_head, fill=WHITE)
            hy += 34
        body_lines = _wrap(d, body, f_body, 968 - 168 - 24)
        by = y + 48 + len(head_lines[:2]) * 34 + 6
        for line in body_lines[:1]:
            d.text((168, by), line, font=f_body, fill=MUTED)
        y += row_h + gap

    d.text((56, 986), "Sources: Open Chronicle, KLZ, IANS  |  20 Nov 2026  |  Figures may be revised",
           font=f_foot, fill=MUTED)
    return img


def main():
    out = Path("/output/entry.png") if Path("/output").is_dir() else Path(__file__).resolve().parent / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    render().save(out, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
