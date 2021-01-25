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

--modeで全都道府県のデータをインストールするか、gcsへuploadするか、rmで解凍後のzipファイルを消すかどうかなどを指定する。

```
python download_polygons.py --mode all --gcs 1 --rm 1
```
