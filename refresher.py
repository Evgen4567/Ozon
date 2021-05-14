import os
from typing import List

import requests
import time
from personal_data import PersonalData


def refresher_bot(url_links: List[str]):
    count = 0
    while True:
        count += 1
        res_upsert = requests.get(url_links[0]).json()
        requests.get(url_links[2]).json()
        if res_upsert['created']:
            # os.system('deadbeef money.py')
            print("New order!")
        if count == PersonalData.COUNT_REQ:
            count = 0
            requests.post(url_links[3])
            requests.post(url_links[1])
            print("Refresh status of orders done. Go to sleep")
        print("Refresh orders done. Go to sleep")
        time.sleep(PersonalData.SLEEP)


if __name__ == '__main__':
    url = [PersonalData.HOST + "/api/v1/orders/upsert/?days=1",
           PersonalData.HOST + "/api/v1/orders/update/by_status/"]
    refresher_bot(url)
    # os.system('deadbeef money.py')