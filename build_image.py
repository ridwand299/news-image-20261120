"""Render the 20 November 2026 world-news poster.

Deterministic render: fixed 1024x1024 canvas, fixed fonts, colours,
text and layout. No network, no clock, no randomness, so running this
script twice writes identical bytes to entry.png.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 48

NAVY = (15, 30, 51)
NAVY_LIGHT = (27, 51, 84)
GOLD = (201, 162, 39)
PAPER = (247, 244, 238)
INK = (18, 24, 33)
GREY = (90, 98, 110)
RED = (178, 44, 36)
BLUE = (31, 92, 168)
GREEN = (31, 122, 76)
PURPLE = (98, 62, 158)
TEAL = (14, 122, 122)

STORIES = [
    (
        "01",
        RED,
        "Trump, Xi and Putin issue joint peace declaration",
        "The three leaders meet at the Shenzhen summit and agree a joint declaration on peace.",
    ),
    (
        "02",
        BLUE,
        "Russia fires 400+ drones and 110 missiles at Kyiv",
        "The overnight barrage on the Ukrainian capital kills 8 people.",
    ),
    (
        "03",
        PURPLE,
        "ICJ: Myanmar responsible for Rohingya genocide",
        "The World Court finds Myanmar responsible for genocide against the Rohingya.",
    ),
    (
        "04",
        GREEN,
        "EU and UK leaders meet in Brussels",
        "Brussels hosts a summit as the EU and the UK discuss closer cooperation.",
    ),
    (
        "05",
        TEAL,
        "Anthropic in record IPO as US Senate passes energy bill",
        "The AI firm debuts in a record listing while the Senate passes a major energy bill.",
    ),
]


def load_font(bold=False, size=24):
    """Load a DejaVu font, falling back to Pillow's built-in font."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default(size=size)


def wrap(draw, text, font, max_width):
    """Wrap text to fit max_width, returning a list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main():
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)

    # Header band.
    draw.rectangle([0, 0, W, 196], fill=NAVY)
    draw.rectangle([0, 196, W, 202], fill=GOLD)
    date_font = load_font(bold=True, size=26)
    title_font = load_font(bold=True, size=58)
    sub_font = load_font(size=24)
    draw.text((MARGIN, 30), "FRIDAY  •  20 NOVEMBER 2026", font=date_font, fill=GOLD)
    draw.text((MARGIN, 66), "The World in One Image", font=title_font, fill=(255, 255, 255))
    draw.text(
        (MARGIN, 140),
        "Five stories that shaped the day, in a single picture.",
        font=sub_font,
        fill=(205, 214, 226),
    )

    # Story blocks.
    y = 232
    block_h = 138
    num_font = load_font(bold=True, size=30)
    head_font = load_font(bold=True, size=27)
    body_font = load_font(size=21)
    for number, colour, headline, summary in STORIES:
        # Number circle.
        cx, cy = MARGIN + 28, y + 30
        draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=colour)
        draw.text((cx, cy), number, font=num_font, fill=(255, 255, 255), anchor="mm")

        text_x = MARGIN + 84
        text_w = W - MARGIN - text_x
        lines = wrap(draw, headline, head_font, text_w)
        line_y = y
        for line in lines[:2]:
            draw.text((text_x, line_y), line, font=head_font, fill=INK)
            line_y += 34
        summary_lines = wrap(draw, summary, body_font, text_w)
        for line in summary_lines[:2]:
            draw.text((text_x, line_y + 4), line, font=body_font, fill=GREY)
            line_y += 28

        y += block_h
        if number != "05":
            draw.line([MARGIN, y - 14, W - MARGIN, y - 14], fill=(214, 209, 198), width=2)

    # Footer.
    foot_font = load_font(size=20)
    small_font = load_font(size=18)
    draw.rectangle([0, 948, W, 1024], fill=NAVY_LIGHT)
    draw.text(
        (MARGIN, 962),
        "Sources: Open Chronicle  •  KLZ  •  IANS",
        font=foot_font,
        fill=(255, 255, 255),
    )
    draw.text(
        (MARGIN, 990),
        "Figures may be revised as reporting develops.",
        font=small_font,
        fill=(180, 192, 206),
    )

    out = Path(__file__).resolve().parent / "entry.png"
    image.save(out, format="PNG")
    print(f"Wrote {out} ({image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
