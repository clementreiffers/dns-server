import time

from change_dns_address import change_dns
from constants import GOOGLE_DNS, LOCALHOST, TMP_URL
from fs import read_file, empty_file
from src.mongo import insert_many_url_to_analyze


def launch_watchdog():
    print("Starting watchdog..")
    start = time.time()
    while True:
        if time.time() - start > 10:
            start = time.time()
            change_dns(GOOGLE_DNS)
            data = list(filter(lambda d: d != "", read_file(TMP_URL).split("\n")))
            insert_many_url_to_analyze(data)
            print("data saved successfully!")
            empty_file(TMP_URL)
            change_dns(LOCALHOST)
            exit(0)
