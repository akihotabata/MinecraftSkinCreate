# MinecraftSkinCreate

Python ベースのスクリプトで、Minecraft の 64×64 スキン PNG を自動生成します。生成したファイルは、[minecraftskins.com のスキンエディター](https://www.minecraftskins.com/skin-editor/) や [Novaskin](https://minecraft.novaskin.me/) にそのままアップロードして利用できます。写真を読み込んで自動的に色味を抽出し、8×8 の顔タイルも埋め込める簡単 GUI 付きです。

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

以下のコマンドでスキン PNG を出力します。

```bash
python -m src.skin_creator.cli --out build/forest.png --palette forest
```

オプション:

- `--out` (必須): 出力先 PNG ファイルパス。親ディレクトリが無ければ自動作成されます。
- `--palette`: `classic` / `forest` / `tech` または `auto`。写真を渡したときに `auto` を選ぶと色を自動抽出します。
- `--seed`: アクセントドットのランダム性を固定したい場合の任意のシード値。
- `--photo`: 自分の写真ファイルを指定するとパレットを抽出し、8×8 の顔も頭部に載せます。
- `--skip-face`: 写真パレットだけを使いたい場合に、顔の貼り付けを無効化します。

生成されるスキンは、頭部のヘアレイヤーや胴体オーバーレイも含むフル 64×64 レイアウトです。PNG を上記エディターにそのまま読み込むと、クラシックサイズのスキンとして利用できます。

## GUI で写真からスキンを作る

Tkinter ベースの簡単な GUI から、写真を選んでスキンを生成できます。

```bash
python -m src.skin_creator.gui
```

1. 「写真ファイル」で自撮り画像などを指定
2. 「色味/パレット」で `auto` を選ぶと写真から色を抽出（`classic` など既存パレットも選択可）
3. 「スキンを生成」を押すとプレビューと保存先が表示されます
