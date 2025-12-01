from __future__ import annotations

import pathlib
from typing import List, Tuple

from PIL import Image

from .generator import SkinGenerator
from .layout import SkinLayout
from .palette import Palette, adjust_color, base_palettes, with_alpha

RGB = Tuple[int, int, int]


def _brightness(color: RGB) -> float:
    r, g, b = color
    return (0.299 * r) + (0.587 * g) + (0.114 * b)


def _central_crop(image: Image.Image, ratio: float = 0.6) -> Image.Image:
    ratio = max(0.05, min(1.0, ratio))
    width, height = image.size
    side = int(min(width, height) * ratio)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def _quantized_colors(image: Image.Image, colors: int = 6) -> List[RGB]:
    reduced = image.convert("RGB").resize((96, 96))
    quantized = reduced.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    palette_data = quantized.getpalette() or []
    histogram = quantized.getcolors() or []

    def color_from_index(index: int) -> RGB:
        base = index * 3
        return (
            palette_data[base],
            palette_data[base + 1],
            palette_data[base + 2],
        )

    ranked: List[RGB] = [color_from_index(idx) for _, idx in sorted(histogram, reverse=True)]
    return ranked


def derive_palette_from_photo(image: Image.Image) -> Palette:
    """Derive a Minecraft-style palette from a portrait photo.

    The algorithm quantizes the picture into a handful of dominant colors and
    assigns them to Minecraft body parts (skin, hair, shirt, pants, accent)
    based on relative brightness. If the image does not provide enough colors,
    it gracefully falls back to the classic palette.
    """

    fallback = base_palettes()["classic"]
    candidates = _quantized_colors(image)
    if len(candidates) < 3:
        return fallback

    by_light = sorted(candidates, key=_brightness)
    hair = by_light[0]
    accent = by_light[-1]
    skin = by_light[len(by_light) // 2]

    remaining = [c for c in by_light if c not in {hair, accent, skin}]
    if len(remaining) >= 2:
        pants, shirt = remaining[0], remaining[-1]
    elif remaining:
        pants = remaining[0]
        shirt = adjust_color(with_alpha(skin, 255), 18)[:3]
    else:
        pants = adjust_color(with_alpha(skin, 255), -18)[:3]
        shirt = adjust_color(with_alpha(skin, 255), 18)[:3]

    return Palette(
        skin=with_alpha(skin),
        hair=with_alpha(hair),
        shirt=with_alpha(shirt),
        pants=with_alpha(pants),
        accent=with_alpha(accent),
    )


def face_tile_from_photo(image: Image.Image, size: int = 8) -> Image.Image:
    """Crop the center of the photo and downscale it to an 8x8 face tile."""

    cropped = _central_crop(image, ratio=0.5)
    return cropped.resize((size, size), Image.LANCZOS).convert("RGBA")


def apply_face_tile(base: Image.Image, face: Image.Image, layout: SkinLayout) -> Image.Image:
    """Place a small face tile onto the head UV of the generated skin."""

    result = base.copy()
    x0, y0, x1, y1 = layout.head["front"]
    tile = face.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.paste(tile, (x0, y0))
    return Image.alpha_composite(result, layer)


class PhotoSkinGenerator:
    """Generate a Minecraft skin from a portrait photo."""

    def __init__(self, photo_path: pathlib.Path, seed: int | None = None) -> None:
        self.photo_path = pathlib.Path(photo_path)
        self.image = Image.open(self.photo_path).convert("RGBA")
        self.palette = derive_palette_from_photo(self.image)
        self.seed = seed

    def generate(self) -> Image.Image:
        base_generator = SkinGenerator(palette=self.palette, seed=self.seed)
        skin = base_generator.generate()
        face = face_tile_from_photo(self.image)
        return apply_face_tile(skin, face, base_generator.layout)


__all__ = [
    "PhotoSkinGenerator",
    "apply_face_tile",
    "derive_palette_from_photo",
    "face_tile_from_photo",
]
