# -*- coding: utf-8 -*-

import urllib.parse
import zipfile
import requests
import time
import glob
import re
import os
import argparse
import ipdb
from constants import *
from gcs.gcs_controller import GcsController

def download_file(url: str) -> str:
    filename = FUDEPOLYGONS_DIR + urllib.parse.unquote(url.split('/')[-1])
    if (os.path.exists(filename)):
        print("skip downloading. {} exists".format(filename))
        return filename
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

def unzip_file(filename: str) -> None:
    zfile = zipfile.ZipFile(filename)
    for info in zfile.infolist():
        _rename(info)
        zfile.extract(info, FUDEPOLYGONS_DIR)

def download_fudepolygon_files(is_unzip: int) -> None:
    if not os.path.isdir(FUDEPOLYGONS_DIR):
        os.makedirs(FUDEPOLYGONS_DIR)
    for idx, pref in enumerate(PREFECTURES):
        encoded_pref = urllib.parse.quote(pref)
        pref_url = '{}{:02}{}{}.zip'.format(BASE_URL, idx + 1, encoded_pref, YEAR)
        file_name = download_file(pref_url)
        if (file_name and is_unzip):
            unzip_file(file_name)
            print('unzipped {}'.format(file_name))

#　都道府県名を指定してファイルをダウンロードする関数
def dwld_files_from_pref_num(pref_num) -> None:
    if not os.path.isdir(FUDEPOLYGONS_DIR):
        os.makedirs(FUDEPOLYGONS_DIR)
    for idx in pref_num:
        encoded_pref = urllib.parse.quote(PREFECTURES[idx - 1])
        pref_url = '{}{:02}{}{}.zip'.format(BASE_URL, idx, encoded_pref, YEAR)
        file_name = download_file(pref_url)
        if (file_name and is_unzip):
            unzip_file(file_name)
            print('unzipped {}'.format(file_name))

def rm_zfiles() -> None:
    for path in glob.glob('{}*.zip'.format(FUDEPOLYGONS_DIR)):
        os.remove(path)

# 北海道の入れ子になっているzip fileをfudepolygons配下に解凍
# def unzip_hokkaido_files() -> None:
#     for geo_code in HOKKAIDO_GEO_CODES:
#         nested_zpath = '{}{}系.zip'.format(HOKKAIDO_DIR, geo_code)
#         if (os.path.exists(nested_zpath)):
#             unzip_file(nested_zpath)

# 北海道の中のzipファイル削除
# def rm_hokkaido_files_and_dir() -> None:
#     for path in glob.glob('{}*.zip'.format(HOKKAIDO_DIR)):
#         os.remove(path)
#     # 空になった北海道ディレクトリを削除
#     if (os.path.exists(HOKKAIDO_DIR)):
#         os.rmdir(HOKKAIDO_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='番号を指定して筆ポリゴンファイルをダウンロードするスクリプト')
    parser.add_argument('--mode', help='全都道府県か否か')
    parser.add_argument('--gcs', type=int)
    parser.add_argument('--pref_num', type=int, nargs='*')
    args = parser.parse_args()
    if (args.mode == "all"):
        download_fudepolygon_files(0)
        if (args.gcs == 1):
            gcs = GcsController(storage.Client())
            bucket = gcs.create_bucket("COLDLINE", "us-east-1")
            gcs.upload_data_to_bucket(bucket.name)
    if (args.pref_num):
        # 都道府県名を指定してファイルをダウンロードしたい時
        dwld_files_from_pref_num(args.pref_num)
    rm_zfiles()
