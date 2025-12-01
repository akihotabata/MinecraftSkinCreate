from __future__ import annotations

import argparse
import pathlib

from . import SkinGenerator, base_palettes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a ready-to-upload 64x64 Minecraft skin PNG that works "
            "with editors like minecraftskins.com and Novaskin."
        )
    )
    parser.add_argument(
        "--palette",
        choices=sorted(base_palettes().keys()),
        default="classic",
        help="Palette style to apply (defaults to classic).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional RNG seed to keep accent placement deterministic.",
    )
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        required=True,
        help="Output PNG path. The parent directory is created if needed.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    palettes = base_palettes()
    palette = palettes[args.palette]

    generator = SkinGenerator(palette=palette, seed=args.seed)
    image = generator.generate()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.out, format="PNG")
    print(f"Saved skin to {args.out.resolve()}")


if __name__ == "__main__":
    main()
