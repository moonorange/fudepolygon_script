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

def download_file(url: str, fudepoly_dir: str) -> str:
    filename = fudepoly_dir + urllib.parse.unquote(url.split('/')[-1])
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

def unzip_file(filename: str, fudepoly_dir: str) -> None:
    unzipped_filename = os.path.splitext(filename)[0]
    if os.path.exists(unzipped_filename):
        print("{} is already unzipped\n".format(unzipped_filename))
    zfile = zipfile.ZipFile(filename)
    for info in zfile.infolist():
        _rename(info)
        zfile.extract(info, fudepoly_dir)
    print('unzipped {}'.format(filename))

def download_fudepolygon_files(is_unzip: int, pref_list=PREFECTURES, fudepoly_dir: str = FUDEPOLYGONS_DIR) -> None:
    if not os.path.isdir(fudepoly_dir):
        os.makedirs(fudepoly_dir)
    for pref in (pref_list):
        encoded_pref = urllib.parse.quote(pref)
        idx = PREFECTURES.index(pref)
        pref_url = '{}{:02}{}{}.zip'.format(BASE_URL, idx + 1, encoded_pref, YEAR)
        file_name = download_file(pref_url, fudepoly_dir)
        if (file_name and is_unzip):
            unzip_file(file_name, fudepoly_dir)

def rm_zfiles() -> None:
    for path in glob.iglob('{}*.zip'.format(FUDEPOLYGONS_DIR)):
        os.remove(path)

# 筆ポリupadateで不必要になった関数、念のため残しておく

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
    parser = argparse.ArgumentParser(description='筆ポリゴンファイルをダウンロードしたりgcsにuploadするスクリプト')
    parser.add_argument('-pref', required=True, type=str, nargs='*', help='ダウンロードしたい都道府県名を任意数正確に入力、全部の場合はallを指定')
    parser.add_argument('-dir', required=True, type=str, help='筆ポリデータを保存する階層')
    parser.add_argument('-unzip', action='store_true', help='zipファイルを解凍する場合は指定')
    parser.add_argument('-rm', action='store_true', help='zipファイルを消す場合は指定')
    args = parser.parse_args()

    if (args.pref[0] == "all"):
        # 全都道府県
        download_fudepolygon_files(args.unzip, args.dir)
    else:
        # 都道府県名を指定してファイルをダウンロードする
        download_fudepolygon_files(args.unzip, args.pref, args.dir)
    if (args.rm):
        # zipfileを消す
        rm_zfiles()
