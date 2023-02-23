import time

from src.change_dns_address import change_dns
from src.fs import TMP_DIR


def launch_watchdog():
    print("Starting watchdog..")
    start = time.time()
    while True:
        if time.time() - start > 5:
            start = time.time()
            change_dns("8.8.8.8")
            with open(f"{TMP_DIR}unknown_urls.txt", "r") as f:
                data = f.read()
            # todo: make post request to send data
            # todo: empty the tmp file
            change_dns("127.0.0.1")
