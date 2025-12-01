# MinecraftSkinCreate

Python ベースのスクリプトで、Minecraft の 64×64 スキン PNG を自動生成します。生成したファイルは、[minecraftskins.com のスキンエディター](https://www.minecraftskins.com/skin-editor/) や [Novaskin](https://minecraft.novaskin.me/) にそのままアップロードして利用できます。

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
- `--palette`: `classic` / `forest` / `tech` から選択。デフォルトは `classic`。
- `--seed`: アクセントドットのランダム性を固定したい場合の任意のシード値。

生成されるスキンは、頭部のヘアレイヤーや胴体オーバーレイも含むフル 64×64 レイアウトです。PNG を上記エディターにそのまま読み込むと、クラシックサイズのスキンとして利用できます。
