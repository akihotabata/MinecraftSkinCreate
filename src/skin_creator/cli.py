from __future__ import annotations

import argparse
import pathlib

from . import PhotoSkinGenerator, SkinGenerator, base_palettes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a ready-to-upload 64x64 Minecraft skin PNG that works "
            "with editors like minecraftskins.com and Novaskin."
        )
    )
    parser.add_argument(
        "--palette",
        choices=["auto"] + sorted(base_palettes().keys()),
        default="classic",
        help=(
            "Palette style to apply. Use 'auto' to sample dominant colors "
            "from the given photo."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional RNG seed to keep accent placement deterministic.",
    )
    parser.add_argument(
        "--photo",
        type=pathlib.Path,
        help="Photo file to derive a palette and face tile from.",
    )
    parser.add_argument(
        "--skip-face",
        action="store_true",
        help="When a photo is provided, skip overlaying the sampled 8x8 face tile.",
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

    palette_key = args.palette
    if palette_key == "auto" and not args.photo:
        palette_key = "classic"
    if args.photo and palette_key == "classic":
        # When a photo is supplied without an explicit palette, prioritize auto derivation.
        palette_key = "auto"

    if args.photo and palette_key == "auto":
        generator = PhotoSkinGenerator(photo_path=args.photo, seed=args.seed)
        image = generator.generate()
        if args.skip_face:
            # Regenerate with the same palette minus the extracted face tile.
            image = SkinGenerator(generator.palette, seed=args.seed).generate()
    else:
        palette = palettes[palette_key]
        generator = SkinGenerator(palette=palette, seed=args.seed)
        image = generator.generate()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.out, format="PNG")
    print(f"Saved skin to {args.out.resolve()}")


if __name__ == "__main__":
    main()
