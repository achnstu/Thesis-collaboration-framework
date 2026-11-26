"""Arrange existing demo previews in an evenly spaced README gallery.

Requires Pillow >= 10.1. Run from any directory with Python. Source plots
retain their aspect ratios and all labels; only the surrounding layout changes.
"""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "python-figures"
PANELS = (
    ("paired", "Paired comparison"),
    ("roc", "ROC curves"),
    ("volcano", "Volcano plot"),
    ("dotplot", "Dot plot"),
    ("marginal", "Marginal distributions"),
)
CARD_WIDTH, CARD_HEIGHT = 660, 680
MARGIN, GAP, HEADER = 28, 28, 72


def make_card(name, title):
    """Fit a full source image inside a fixed-size card without cropping."""
    card = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), "white")
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, CARD_WIDTH - 1, HEADER), fill="#f6f8fa")
    draw.line((0, HEADER, CARD_WIDTH, HEADER), fill="#d8dee4", width=2)
    draw.text(
        (24, HEADER // 2),
        title,
        font=ImageFont.load_default(size=32),
        fill="#24292f",
        anchor="lm",
    )
    with Image.open(ASSETS / f"{name}.png") as source:
        preview = ImageOps.contain(
            source.convert("RGB"),
            (CARD_WIDTH - 40, CARD_HEIGHT - HEADER - 40),
            Image.Resampling.LANCZOS,
        )
    x = (CARD_WIDTH - preview.width) // 2
    y = HEADER + (CARD_HEIGHT - HEADER - preview.height) // 2
    card.paste(preview, (x, y))
    draw.rectangle((0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1), outline="#d8dee4", width=2)
    return card


def main():
    width = 2 * MARGIN + 3 * CARD_WIDTH + 2 * GAP
    height = 2 * MARGIN + 2 * CARD_HEIGHT + GAP
    gallery = Image.new("RGB", (width, height), "white")
    positions = (
        (MARGIN, MARGIN),
        (MARGIN + CARD_WIDTH + GAP, MARGIN),
        (MARGIN + 2 * (CARD_WIDTH + GAP), MARGIN),
        (MARGIN + (CARD_WIDTH + GAP) // 2, MARGIN + CARD_HEIGHT + GAP),
        (MARGIN + 3 * (CARD_WIDTH + GAP) // 2, MARGIN + CARD_HEIGHT + GAP),
    )
    for (name, title), position in zip(PANELS, positions, strict=True):
        gallery.paste(make_card(name, title), position)
    output = ASSETS / "templates.png"
    gallery.save(output, optimize=True)

    path = ASSETS / "provenance.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    record["files"][output.name] = hashlib.sha256(output.read_bytes()).hexdigest()
    record["gallery_layout"] = {
        "builder": "../../scripts/build_python_gallery.py",
        "arrangement": "Three equal cards above two centered equal cards",
        "card_size_px": [CARD_WIDTH, CARD_HEIGHT],
        "gap_px": GAP,
        "source_images": "Existing exported previews, uncropped and aspect-preserved",
    }
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built {output.name}: {width} x {height}, {len(PANELS)} equal cards")


if __name__ == "__main__":
    main()
