import os

from constants import TMP_DIR, TMP_URL


def write_unknown_url(url):
    create_file_if_not_exist(TMP_DIR)
    with open(TMP_URL, "a") as f:
        f.write(url + "\n")


def create_file_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)
