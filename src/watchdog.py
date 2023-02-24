import time

from change_dns_address import change_dns
from constants import GOOGLE_DNS, LOCALHOST, TMP_URL


def launch_watchdog():
    print("Starting watchdog..")
    start = time.time()
    while True:
        if time.time() - start > 5:
            start = time.time()
            change_dns(GOOGLE_DNS)
            with open(TMP_URL, "r") as f:
                data = f.read()
            # todo: make post request to send data
            # todo: empty the tmp file
            change_dns(LOCALHOST)
