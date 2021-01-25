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
from google.cloud import storage

def download_file(url: str) -> str:
    filename = FUDEPOLYGONS_DIR + urllib.parse.unquote(url.split('/')[-1])
    if (os.path.exists(filename)):
        print("{} already exists".format(filename))
        return filename
    print('downloading {} ...'.format(filename))
    chunk_size = 1024
    start_time = time.time()
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                f.flush()
        print("--- Finished in %s seconds with chunk_size %d---" % (time.time() - start_time, chunk_size))
        return filename

    # ファイルが開けなかった場合は False を返す
    return False

def _rename(info: zipfile.ZipInfo) -> None:
    """ヘルパー: `ZipInfo` のファイル名を SJIS でデコードし直す"""
    LANG_ENC_FLAG = 0x800
    encoding = 'utf-8' if info.flag_bits & LANG_ENC_FLAG else 'cp437'
    info.filename = info.filename.encode(encoding).decode('cp932')

def unzip_file(filename: str) -> None:
    unzipped_filename = os.path.splitext(filename)[0]
    if os.path.exists(unzipped_filename):
        print("{} is already unzipped\n".format(unzipped_filename))
    zfile = zipfile.ZipFile(filename)
    for info in zfile.infolist():
        _rename(info)
        zfile.extract(info, FUDEPOLYGONS_DIR)
    print('unzipped {}'.format(filename))

def download_fudepolygon_files(is_unzip: int) -> None:
    if not os.path.isdir(FUDEPOLYGONS_DIR):
        os.makedirs(FUDEPOLYGONS_DIR)
    for idx, pref in enumerate(PREFECTURES):
        encoded_pref = urllib.parse.quote(pref)
        pref_url = '{}{:02}{}{}.zip'.format(BASE_URL, idx + 1, encoded_pref, YEAR)
        file_name = download_file(pref_url)
        if (file_name and is_unzip):
            unzip_file(file_name)

#　都道府県名を指定してファイルをダウンロードする関数
def dwld_files_from_pref_num(pref_num, is_unzip: int) -> None:
    if not os.path.isdir(FUDEPOLYGONS_DIR):
        os.makedirs(FUDEPOLYGONS_DIR)
    for idx in pref_num:
        encoded_pref = urllib.parse.quote(PREFECTURES[idx - 1])
        pref_url = '{}{:02}{}{}.zip'.format(BASE_URL, idx, encoded_pref, YEAR)
        file_name = download_file(pref_url)
        if (file_name and is_unzip):
            unzip_file(file_name)

def rm_zfiles() -> None:
    for path in glob.iglob('{}*.zip'.format(FUDEPOLYGONS_DIR)):
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
    parser.add_argument('--pref_num', type=int, nargs='*')
    parser.add_argument('--gcs', type=int, default=0)
    parser.add_argument('--unzip', type=int, default=0)
    parser.add_argument('--rm', type=int, default=0)
    args = parser.parse_args()


    if (args.mode == "all"):
        # 全都道府県
        download_fudepolygon_files(args.unzip)
    if (args.pref_num):
        # 都道府県名を指定してファイルをダウンロードしたい時
        dwld_files_from_pref_num(args.pref_num)
    if (args.gcs):
        # gcsにアップロード
        strage_cl = storage.Client()
        gcs = GcsController(strage_cl)
        storage_class = "COLDLINE"
        location = "us-east-1"
        bucket = gcs.create_bucket(storage_class, location)
        gcs.upload_data_to_bucket(bucket.name)
    if (args.rm):
        # zipfileを消す
        rm_zfiles()
