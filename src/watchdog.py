import time

from change_dns_address import change_dns
from constants import GOOGLE_DNS, LOCALHOST, TMP_URL, CLOCK
from fs import read_file, empty_file, read_state_dns
from mongo import insert_many_url_to_analyze


def launch_watchdog():
    print("Starting watchdog..")
    start = time.time()
    while True:
        try:
            if read_state_dns()["dns_choosen"] == LOCALHOST and time.time() - start > CLOCK:
                start = time.time()
                change_dns(GOOGLE_DNS)
                data = list(filter(lambda d: d != "", read_file(TMP_URL).split("\n")))
                if len(data):
                    insert_many_url_to_analyze(data)
                    print("data saved successfully!")
                    empty_file(TMP_URL)
                    change_dns(LOCALHOST)
        except:
            pass
