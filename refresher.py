from typing import List

import requests
import time
from personal_data import PersonalData


def refresher_bot(url_links: List[str]):
    count = 0
    while True:
        count += 1
        res_upsert = requests.get(url_links[0]).json()
        print(res_upsert)
        if res_upsert['created']:
            print("New order!")
        if count == PersonalData.COUNT_REQ:
            count = 0
            requests.post(url_links[1])
            print("Refresh status of orders done. Go to sleep")
        print("Refresh orders done. Go to sleep")
        time.sleep(PersonalData.SLEEP)


def fill_db(d_from, d_to, host):
    for d in range(d_from, d_to, -1):
        url = f'{host}/api/v1/raw_data/upsert/?days_from={d}&days_to={d-1}'
        # while requests.get(url) !=
        # time.sleep(1)
    print('finish')


if __name__ == '__main__':
    url = [PersonalData.HOST + "/api/v1/raw_data/upsert/?days_from=1",
           PersonalData.HOST + "/api/v1/raw_data/update/by_status/"]
    refresher_bot(url)
    # fill_db(200, 0, PersonalData.HOST)
    # status_code = requests.get(f'{PersonalData.HOST}/api/v1/raw_data/upsert/?days_from=69&days_to=68').status_code
    # print(status_code)