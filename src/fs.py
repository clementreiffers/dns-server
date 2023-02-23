import os

TMP_DIR = "../tmp/"


def write_unknown_url(url):
    create_file_if_not_exist(TMP_DIR)
    with open(f"{TMP_DIR}unknown_urls.txt", "a") as f:
        f.write(url + "\n")


def create_file_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)
