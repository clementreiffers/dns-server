import json
import os

from constants import TMP_DIR, TMP_URL


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def write_unknown_url(url):
    create_file_if_not_exist(TMP_DIR)
    with open(TMP_URL, "a") as f:
        f.write(url + "\n")


def empty_file(filename):
    with open(filename, "w") as f:
        f.write("")
        f.close()


def create_file_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)
