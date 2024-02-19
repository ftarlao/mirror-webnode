#!/usr/bin/env python3

# Script per il download di siti web su webnode.com
# Funziona con siti semplici con pochi livelli, scarica anche le risorse esterne
# in modo che gli elaborati si possano archiviare in modo quasi completo.
#
# Script for downloading websites on webnode.com
# Works with simple sites with few levels, also downloads external resources
# so that the documents can be archived almost completely.
#
# Prof. Tarlao Fabiano

import os
import subprocess
import re
import pathlib
import argparse
from multiprocessing import Pool
import shutil
from datetime import datetime

# You can also tune these params:
NUM_THREADS = 4 # download N sites at same time
TIMEOUT = 4     # secs
LEVELS = 1      # Depth in Levels


def remove_cookies_box_from_html_files(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                print(file_path)
                with open(file_path, 'r') as f:
                    content = f.read()
                updated_content = re.sub(r'<section\s*class="[^"]*"\s*id="cookiebar".+</section>', '', content, flags=re.DOTALL)
                with open(file_path, 'w') as f:
                    f.write(updated_content)


def download_site(url):
    print("DOWNLOAD STARTED FOR: "+url)

    os.makedirs(DEST_FOLDER, exist_ok=True)
    down_process = subprocess.run(
        ['wget', '-U', 'Mozilla/5.0', '-e', 'robots=off', '--mirror',
         '--timeout=' + str(TIMEOUT), '--tries=2',
         '--convert-links', '-H', '-l', str(LEVELS), '--adjust-extension', '--page-requisites',
         '--no-parent', '-P', DEST_FOLDER, url]
        , cwd=BASE_FOLDER, stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT, universal_newlines=True)

    down_process
    # Let's remove the cookies preference panel
    remove_cookies_box_from_html_files(DEST_FOLDER)
    print("COMPLETED URL "+url)


# path = path to folder to compress, className name of the class to add to the ZIP name
# name format eg:  "1F 202402 webnode mirror.zip"
def zip_folder(path, className):
    final_zip_name = str(className)+" "+datetime.now().strftime('%Y%m')+" webnode mirror"
    shutil.make_archive(final_zip_name, 'zip', path)
    print("OUTPUT ZIP FILENAME: "+final_zip_name)


if __name__ == '__main__':
    folder_name = "mirror"  # url.split('//')[-1].replace('/', '_')
    BASE_FOLDER = pathlib.Path().resolve()
    default_folder = os.path.join(BASE_FOLDER, folder_name)

    parser = argparse.ArgumentParser("download.py")
    parser.add_argument("filename", help="Nome del file contenente la lista delle URLs siti", type=str)
    parser.add_argument("name_prefix", help="Prefisso da aggiungere a nome articolo, e.g. puo' essere una"
                                          " classe: es:1E .. 4T", type=str)
    parser.add_argument("dest_folder", help="Cartella di destinazione per le immagini dei siti, "
                                            "default: 'mirror' folder in the current execution path",
                        type=str, default=default_folder, nargs='?')
    args = parser.parse_args()

    input_file = args.filename
    name_prefix = args.name_prefix
    DEST_FOLDER = args.dest_folder

    print("Destination Folder: ", DEST_FOLDER)

    with open(input_file, 'r') as f:
        urls = f.readlines()
        stripped_urls = [s.strip() for s in urls]
    with Pool(NUM_THREADS) as p:
        p.map(download_site, stripped_urls)
        p.close()
        p.join()

        zip_folder(DEST_FOLDER, name_prefix)

    print("******JOB DONE******")
