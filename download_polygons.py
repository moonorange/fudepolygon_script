# -*- coding: utf-8 -*-

import urllib.parse
import zipfile
import requests
import time
import glob
import re
import os

PREFECTURES = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

YEAR = '2019'

BASE_URL = 'http://www.machimura.maff.go.jp/polygon/'

FUDEPOLYGONS_DIR = 'fudepolygons/'

HOKKAIDO_DIR = 'fudepolygons/01北海道{}/'.format(YEAR)
HOKKAIDO_GEO_CODES = ['11', '12', '13']

def download_file(url: str) -> str:
    filename = urllib.parse.unquote(url.split('/')[-1])
    print('downloading {} ...'.format(filename))
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return filename

    # ファイルが開けなかった場合は False を返す
    return False

def _rename(info: zipfile.ZipInfo) -> None:
    """ヘルパー: `ZipInfo` のファイル名を SJIS でデコードし直す"""
    LANG_ENC_FLAG = 0x800
    encoding = 'utf-8' if info.flag_bits & LANG_ENC_FLAG else 'cp437'
    info.filename = info.filename.encode(encoding).decode('cp932')

def zip_extract(filename: str) -> None:
    zfile = zipfile.ZipFile(filename)
    for info in zfile.infolist():
        _rename(info)
        zfile.extract(info, FUDEPOLYGONS_DIR)

def get_fudepolygon_files():
    for idx, pref in enumerate(PREFECTURES):
        encoded_pref = urllib.parse.quote(pref)
        pref_url = '{}{:02}{}{}.zip'.format(BASE_URL, idx + 1, encoded_pref, YEAR)
        file_name = download_file(pref_url)
        if (file_name):
            zip_extract(file_name)
            print('unzipped {}'.format(file_name))

def rm_zfiles_and_empty_hokkaido():
    for path in glob.glob('./*.zip'):
        os.remove(path)
    # 北海道の中のzipファイル削除
    for path in glob.glob('{}*.zip'.format(HOKKAIDO_DIR)):
        os.remove(path)
    # 空になった北海道ディレクトリを削除
    os.rmdir(HOKKAIDO_DIR)

if __name__ == "__main__":
    get_fudepolygon_files()

    # 北海道の入れ子になっているzip fileをfudepolygons配下に解凍
    for geo_code in HOKKAIDO_GEO_CODES:
        nested_zpath = '{}{}系.zip'.format(HOKKAIDO_DIR, geo_code)
        if (os.path.exists(nested_zpath)):
            zip_extract(nested_zpath)
    rm_zfiles_and_empty_hokkaido()
