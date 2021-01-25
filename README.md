# fudepolygon_script

筆ポリゴンzipファイルをwebからダウンロードし解凍し、最後に不要になったzipファイルを消すスクリプト。
定数FUDEPOLYGONS_DIR配下に全ての都道府県のzipファイルが解凍されたものが残る。
北海道の入れ子になっているzipもFUDEPOLYGONS_DIR配下に展開される。

gcsへのアップロードが必要な場合はコマンドライン引数で指定すればできる。

# 注意

URLは2020年のものを前提としている。農水省の更新によってurlが変わるかもしれないためその都度updateする必要がある。
基本的にはYEAR定数を変更すれば大丈夫なはず。

# 使用

## venv作成、有効化、ライブラリインストール
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

## 実行

全都道府県のデータをインストールするか、zipを解凍するか、gcsへuploadするか、rmで解凍後のzipファイルを消すかどうかなどコマンドライン引数で指定する。
指定しない場合はfalseになる。

```
python download_polygons.py --pref all --unzip 1 --gcs 0 --rm 1
```

```
python download_polygons.py --pref 北海道 大阪府 沖縄県　--unzip 1
```
