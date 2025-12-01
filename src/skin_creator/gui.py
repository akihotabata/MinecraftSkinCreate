from __future__ import annotations

import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from . import (
    PhotoSkinGenerator,
    SkinGenerator,
    apply_face_tile,
    base_palettes,
    face_tile_from_photo,
)


class SkinGuiApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Minecraft スキン作成 GUI")

        self.photo_path = tk.StringVar()
        self.output_path = tk.StringVar(value=str(pathlib.Path("build/photo_skin.png")))
        self.palette_choice = tk.StringVar(value="auto")
        self.include_face = tk.BooleanVar(value=True)
        self.status = tk.StringVar(value="写真を選んでから生成してください")
        self.preview_image = None

        self._build_layout()

    def _build_layout(self) -> None:
        frame = tk.Frame(self.root, padx=16, pady=16)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="1. 写真ファイル").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.photo_path, width=38).grid(
            row=1, column=0, sticky="we", padx=(0, 8)
        )
        tk.Button(frame, text="参照...", command=self._select_photo).grid(row=1, column=1)

        tk.Label(frame, text="2. 色味/パレット").grid(row=2, column=0, sticky="w", pady=(8, 0))
        palette_names = ["auto"] + sorted(base_palettes().keys())
        tk.OptionMenu(frame, self.palette_choice, *palette_names).grid(
            row=3, column=0, sticky="w"
        )
        tk.Checkbutton(frame, text="顔も写真から 8x8 で取り込み", variable=self.include_face).grid(
            row=3, column=1, sticky="w"
        )

        tk.Label(frame, text="3. 出力先ファイル").grid(row=4, column=0, sticky="w", pady=(8, 0))
        tk.Entry(frame, textvariable=self.output_path, width=38).grid(
            row=5, column=0, sticky="we", padx=(0, 8)
        )
        tk.Button(frame, text="保存先...", command=self._select_output).grid(row=5, column=1)

        tk.Button(frame, text="スキンを生成", command=self._generate, width=20).grid(
            row=6, column=0, pady=(12, 4), sticky="w"
        )
        tk.Label(frame, textvariable=self.status, fg="#2c5282").grid(
            row=6, column=1, sticky="w"
        )

        self.preview_label = tk.Label(frame, text="プレビューはここに表示されます")
        self.preview_label.grid(row=7, column=0, columnspan=2, pady=(12, 0))

    def _select_photo(self) -> None:
        filename = filedialog.askopenfilename(
            title="写真を選択", filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.webp *.bmp")]
        )
        if filename:
            self.photo_path.set(filename)

    def _select_output(self) -> None:
        filename = filedialog.asksaveasfilename(
            title="保存先を選択", defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if filename:
            self.output_path.set(filename)

    def _load_photo(self) -> Image.Image:
        return Image.open(self.photo_path.get()).convert("RGBA")

    def _generate(self) -> None:
        if not self.photo_path.get():
            messagebox.showerror("エラー", "まず写真を選択してください")
            return

        try:
            photo = self._load_photo()
        except Exception as exc:  # pragma: no cover - GUI message surface
            messagebox.showerror("読み込み失敗", f"画像を開けませんでした: {exc}")
            return

        output = pathlib.Path(self.output_path.get()).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)

        palette_key = self.palette_choice.get()
        if palette_key == "auto":
            generator = PhotoSkinGenerator(photo_path=pathlib.Path(self.photo_path.get()))
            skin = generator.generate()
            palette_used = "写真から自動抽出"
        else:
            palette = base_palettes()[palette_key]
            base_generator = SkinGenerator(palette=palette)
            skin = base_generator.generate()
            if self.include_face.get():
                face = face_tile_from_photo(photo)
                skin = apply_face_tile(skin, face, base_generator.layout)
            palette_used = palette_key

        skin.save(output, format="PNG")
        self.status.set(f"{output} に保存しました (パレット: {palette_used})")
        self._show_preview(skin)

    def _show_preview(self, skin) -> None:
        preview = skin.resize((192, 192), Image.NEAREST)
        self.preview_image = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=self.preview_image)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:  # pragma: no cover - GUI entrypoint
    SkinGuiApp().run()


if __name__ == "__main__":  # pragma: no cover - GUI entrypoint
    main()
