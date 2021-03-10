import requests
from datetime import datetime, timedelta

headers_d = {
    "accept": "application/json",
    "Client-Id": "123090",
    "Api-Key": "87e400a8-a791-4cc5-ad98-82c032c90d5b",
    "Content-Type": "application/json"
}


def list_orders(headers, dir="desc", time_since=datetime.utcnow()-timedelta(1), time_to=datetime.utcnow(), limit=50, offset=0):
    url = 'https://api-seller.ozon.ru/v2/posting/fbo/list'
    since = time_since.isoformat()[:-3] + 'Z'
    to = time_to.isoformat()[:-3]+'Z'
    body_d = {
        "dir": dir,
        "filter": {
            "since": since,
            "to": to
        },
        "limit": limit,
        "offset": offset,
        "translit": True,
        "with": {
            "analytics_data": True,
            "financial_data": True
        }
    }
    return requests.post(url, headers=headers, json=body_d)

