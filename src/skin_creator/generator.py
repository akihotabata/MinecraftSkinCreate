from __future__ import annotations

import random
from typing import Dict, Iterable

from PIL import Image, ImageDraw

from .layout import SkinLayout, Box
from .palette import Palette, adjust_color


def fill(draw: ImageDraw.ImageDraw, box: Box, color) -> None:
    draw.rectangle(box, fill=color)


def draw_cube(draw: ImageDraw.ImageDraw, faces: Dict[str, Box], color: Palette) -> None:
    fill(draw, faces["top"], color.lighter.skin)
    fill(draw, faces["bottom"], color.darker.skin)
    fill(draw, faces["front"], color.skin)
    fill(draw, faces["back"], color.skin)
    fill(draw, faces["left"], color.darker.skin)
    fill(draw, faces["right"], color.lighter.skin)


def draw_hair(draw: ImageDraw.ImageDraw, faces: Dict[str, Box], palette: Palette) -> None:
    accent = adjust_color(palette.hair, -10)
    fill(draw, faces["top"], palette.hair)
    fill(draw, faces["back"], accent)
    # fringe
    x0, y0, x1, y1 = faces["front"]
    draw.rectangle((x0, y1 - 2, x1, y1), fill=palette.hair)


def draw_face(draw: ImageDraw.ImageDraw, faces: Dict[str, Box], palette: Palette) -> None:
    x0, y0, x1, y1 = faces["front"]
    # eyes
    eye = adjust_color(palette.accent, -20)
    draw.point((x0 + 2, y0 + 3), fill=eye)
    draw.point((x0 + 5, y0 + 3), fill=eye)
    # mouth
    draw.line((x0 + 2, y0 + 6, x0 + 5, y0 + 6), fill=adjust_color(palette.hair, 10))


def draw_torso(draw: ImageDraw.ImageDraw, faces: Dict[str, Box], palette: Palette) -> None:
    fill(draw, faces["top"], palette.darker.shirt)
    fill(draw, faces["bottom"], palette.darker.shirt)
    fill(draw, faces["front"], palette.shirt)
    fill(draw, faces["back"], palette.darker.shirt)
    fill(draw, faces["left"], palette.lighter.shirt)
    fill(draw, faces["right"], palette.lighter.shirt)

    # belt line
    belt = adjust_color(palette.pants, 8)
    x0, y0, x1, y1 = faces["front"]
    draw.rectangle((x0, y1 - 3, x1, y1), fill=belt)


def draw_limb(draw: ImageDraw.ImageDraw, faces: Dict[str, Box], palette: Palette, *, use_pants: bool) -> None:
    fabric = palette.pants if use_pants else palette.shirt
    darker = adjust_color(fabric, -10)
    lighter = adjust_color(fabric, 12)
    fill(draw, faces["top"], lighter)
    fill(draw, faces["bottom"], darker)
    fill(draw, faces["front"], fabric)
    fill(draw, faces["back"], darker)
    fill(draw, faces["left"], darker)
    fill(draw, faces["right"], lighter)


def draw_boots(draw: ImageDraw.ImageDraw, faces: Dict[str, Box], palette: Palette) -> None:
    boot = adjust_color(palette.pants, -25)
    x0, y0, x1, y1 = faces["front"]
    draw.rectangle((x0, y1 - 4, x1, y1), fill=boot)


def draw_gloves(draw: ImageDraw.ImageDraw, faces: Dict[str, Box], palette: Palette) -> None:
    glove = adjust_color(palette.shirt, -20)
    x0, y0, x1, y1 = faces["front"]
    draw.rectangle((x0, y1 - 3, x1, y1), fill=glove)


def scatter_accent(
    draw: ImageDraw.ImageDraw,
    boxes: Iterable[Box],
    palette: Palette,
    rng: random.Random,
    probability: float = 0.08,
) -> None:
    accent = palette.accent
    for box in boxes:
        x0, y0, x1, y1 = box
        for x in range(x0, x1):
            for y in range(y0, y1):
                if rng.random() < probability:
                    draw.point((x, y), fill=accent)


class SkinGenerator:
    def __init__(self, palette: Palette, seed: int | None = None) -> None:
        self.palette = palette
        self.random = random.Random(seed)
        self.layout = SkinLayout()

    def generate(self) -> Image.Image:
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Base skin
        draw_cube(draw, self.layout.head, self.palette)
        draw_face(draw, self.layout.head, self.palette)
        draw_torso(draw, self.layout.body, self.palette)
        draw_limb(draw, self.layout.right_arm, self.palette, use_pants=False)
        draw_limb(draw, self.layout.left_arm, self.palette, use_pants=False)
        draw_limb(draw, self.layout.right_leg, self.palette, use_pants=True)
        draw_limb(draw, self.layout.left_leg, self.palette, use_pants=True)

        draw_boots(draw, self.layout.right_leg, self.palette)
        draw_boots(draw, self.layout.left_leg, self.palette)
        draw_gloves(draw, self.layout.right_arm, self.palette)
        draw_gloves(draw, self.layout.left_arm, self.palette)

        # Overlays
        draw_hair(draw, self.layout.head_overlay, self.palette)
        self._draw_cloak(draw)
        self._draw_straps(draw)

        # Scatter accent pixels for texture
        scatter_accent(
            draw,
            [
                self.layout.body["front"],
                self.layout.right_arm["front"],
                self.layout.left_arm["front"],
                self.layout.right_leg["front"],
                self.layout.left_leg["front"],
            ],
            self.palette,
            self.random,
            probability=0.04,
        )

        return img

    def _draw_cloak(self, draw: ImageDraw.ImageDraw) -> None:
        overlay = self.layout.body_overlay
        fill(draw, overlay["top"], adjust_color(self.palette.shirt, -10))
        fill(draw, overlay["front"], adjust_color(self.palette.shirt, -14))
        fill(draw, overlay["back"], adjust_color(self.palette.shirt, -20))
        fill(draw, overlay["left"], adjust_color(self.palette.shirt, -16))
        fill(draw, overlay["right"], adjust_color(self.palette.shirt, -12))

    def _draw_straps(self, draw: ImageDraw.ImageDraw) -> None:
        accent = adjust_color(self.palette.accent, -12)
        for part in [self.layout.body, self.layout.left_arm, self.layout.right_arm]:
            front = part["front"]
            x0, y0, x1, y1 = front
            draw.rectangle((x0 + 1, y0 + 1, x0 + 3, y1 - 1), fill=accent)


__all__ = ["SkinGenerator"]
