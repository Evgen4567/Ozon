from typing import List

import requests
import time
from playsound import playsound


def refresher_bot(url_links: List[str]):
    while True:
        res_upsert = requests.get(url_links[0]).json()
        requests.post(url_links[1])
        if not res_upsert['created']:
            playsound("money.mp3")
        print("Refresh_done. go to sleep")
        time.sleep(180)


if __name__ == '__main__':
    url = ["http://192.168.0.101/api/v1/orders/upsert/?days=3", "http://192.168.0.101/api/v1/orders/update/by_status/"]
    refresher_bot(url)

