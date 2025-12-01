from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

Color = Tuple[int, int, int, int]


def clamp(value: int) -> int:
    return max(0, min(255, value))


def adjust_color(color: Color, delta: int) -> Color:
    r, g, b, a = color
    return (clamp(r + delta), clamp(g + delta), clamp(b + delta), a)


def with_alpha(color: Tuple[int, int, int], alpha: int = 255) -> Color:
    r, g, b = color
    return (r, g, b, alpha)


@dataclass
class Palette:
    skin: Color
    hair: Color
    shirt: Color
    pants: Color
    accent: Color

    @property
    def darker(self) -> "Palette":
        return Palette(
            skin=adjust_color(self.skin, -12),
            hair=adjust_color(self.hair, -15),
            shirt=adjust_color(self.shirt, -16),
            pants=adjust_color(self.pants, -16),
            accent=adjust_color(self.accent, -18),
        )

    @property
    def lighter(self) -> "Palette":
        return Palette(
            skin=adjust_color(self.skin, 16),
            hair=adjust_color(self.hair, 8),
            shirt=adjust_color(self.shirt, 12),
            pants=adjust_color(self.pants, 12),
            accent=adjust_color(self.accent, 12),
        )


def base_palettes() -> Dict[str, Palette]:
    return {
        "classic": Palette(
            skin=with_alpha((216, 181, 154)),
            hair=with_alpha((84, 57, 45)),
            shirt=with_alpha((52, 126, 197)),
            pants=with_alpha((57, 82, 111)),
            accent=with_alpha((236, 190, 91)),
        ),
        "forest": Palette(
            skin=with_alpha((196, 170, 140)),
            hair=with_alpha((66, 51, 40)),
            shirt=with_alpha((58, 112, 80)),
            pants=with_alpha((66, 81, 71)),
            accent=with_alpha((198, 223, 170)),
        ),
        "tech": Palette(
            skin=with_alpha((202, 206, 214)),
            hair=with_alpha((70, 92, 118)),
            shirt=with_alpha((74, 90, 140)),
            pants=with_alpha((54, 67, 94)),
            accent=with_alpha((108, 221, 255)),
        ),
    }
