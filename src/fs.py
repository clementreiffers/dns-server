import json
import os

from constants import TMP_DIR, TMP_URL, TMP_STATE


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def read_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            f.close()
            return data
    return {}


def write_unknown_url(url):
    create_file_if_not_exist(TMP_DIR)
    with open(TMP_URL, "a") as f:
        f.write(url + "\n")


def write_json_file(filename, data):
    with open(filename, "w") as f:
        f.write(json.dumps(data))
        f.close()


def empty_file(filename):
    with open(filename, "w") as f:
        f.write("")
        f.close()


def create_file_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def set_state_dns_listening(boolean):
    state = read_json(TMP_STATE)
    state["listening"] = boolean
    write_json_file(TMP_STATE, state)


def set_state_dns_choosen(dns_choosen):
    state = read_json(TMP_STATE)
    state["dns_choosen"] = dns_choosen
    write_json_file(TMP_STATE, state)


def read_state_dns():
    return read_json(TMP_STATE)
