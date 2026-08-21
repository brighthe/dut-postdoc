#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace Fig. 1 inside the anonymous 1-5 Flat OPC docx and update drawing size."""

from __future__ import annotations

import base64
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
PNG = HERE / "assets" / "fig1_technical_route.png"
DOCX = HERE / "80th-2026-项目信息(1-5部分).docx"

# Keep the template insertion width (EMU). 5471795 ≈ 15.18 cm.
CX = 5471795


def main() -> None:
    png_bytes = PNG.read_bytes()
    with Image.open(PNG) as im:
        width_px, height_px = im.size
    cy = int(round(CX * height_px / width_px))
    b64 = base64.b64encode(png_bytes).decode("ascii")

    text = DOCX.read_text(encoding="utf-8")
    if "/word/media/image1.png" not in text:
        raise SystemExit("image1.png part not found in docx")

    # Replace the image payload: binaryData of the image1.png part only.
    pattern = (
        r'(<pkg:part pkg:name="/word/media/image1.png"[^>]*>\s*'
        r"<pkg:binaryData>)(.*?)(</pkg:binaryData>)"
    )
    text, n = re.subn(pattern, r"\1" + b64 + r"\3", text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"expected 1 image payload replacement, got {n}")

    # Update both drawing extents (wp:extent and a:ext).
    text = re.sub(
        r'(<wp:extent cx=")5471795(" cy=")\d+("/>)',
        rf"\g<1>{CX}\g<2>{cy}\g<3>",
        text,
        count=1,
    )
    text = re.sub(
        r'(<a:ext cx=")5472000(" cy=")\d+("/>)',
        rf"\g<1>5472000\g<2>{cy}\g<3>",
        text,
        count=1,
    )

    DOCX.write_text(text, encoding="utf-8")
    print(f"[png] {width_px}×{height_px} px")
    print(f"[docx] width {CX} EMU, height {cy} EMU "
          f"({CX/360000:.2f} cm × {cy/360000:.2f} cm)")
    print(f"[out] {DOCX}")


if __name__ == "__main__":
    main()
