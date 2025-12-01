from __future__ import annotations

from typing import Dict, Tuple

Box = Tuple[int, int, int, int]


class SkinLayout:
    """Maps Minecraft skin UV positions for a 64x64 classic skin.

    Coordinates are expressed as (left, top, right, bottom) with the right and
    bottom values being *exclusive* to align with Pillow's box handling.
    """

    def __init__(self) -> None:
        self.head = self._cube((0, 0))
        self.head_overlay = self._cube((32, 0))
        self.body = self._body((16, 16))
        self.body_overlay = self._body((16, 32))
        self.right_arm = self._limb((40, 16))
        self.right_arm_overlay = self._limb((40, 32))
        self.right_leg = self._limb((0, 16))
        self.right_leg_overlay = self._limb((0, 32))
        self.left_leg = self._limb((16, 48))
        self.left_leg_overlay = self._limb((0, 48))
        self.left_arm = self._limb((32, 48))
        self.left_arm_overlay = self._limb((48, 48))

    def _cube(self, origin: Tuple[int, int]) -> Dict[str, Box]:
        x, y = origin
        return {
            "top": (x + 8, y, x + 16, y + 8),
            "bottom": (x + 16, y, x + 24, y + 8),
            "right": (x, y + 8, x + 8, y + 16),
            "front": (x + 8, y + 8, x + 16, y + 16),
            "left": (x + 16, y + 8, x + 24, y + 16),
            "back": (x + 24, y + 8, x + 32, y + 16),
        }

    def _body(self, origin: Tuple[int, int]) -> Dict[str, Box]:
        x, y = origin
        return {
            "top": (x + 4, y, x + 12, y + 4),
            "bottom": (x + 12, y, x + 20, y + 4),
            "right": (x, y + 4, x + 4, y + 16),
            "front": (x + 4, y + 4, x + 12, y + 16),
            "left": (x + 12, y + 4, x + 16, y + 16),
            "back": (x + 16, y + 4, x + 24, y + 16),
        }

    def _limb(self, origin: Tuple[int, int]) -> Dict[str, Box]:
        x, y = origin
        return {
            "top": (x + 4, y, x + 8, y + 4),
            "bottom": (x + 8, y, x + 12, y + 4),
            "right": (x, y + 4, x + 4, y + 16),
            "front": (x + 4, y + 4, x + 8, y + 16),
            "left": (x + 8, y + 4, x + 12, y + 16),
            "back": (x + 12, y + 4, x + 16, y + 16),
        }
