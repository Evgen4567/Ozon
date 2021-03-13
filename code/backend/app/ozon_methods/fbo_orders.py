import requests
from datetime import datetime, timedelta


def list_orders(headers, dir="desc",
                time_since: datetime = datetime.utcnow() - timedelta(1),
                time_to: datetime = datetime.utcnow(),
                limit=50, offset=0):
    # time_since = datetime.utcnow() - timedelta(days_ago)
    url = 'https://api-seller.ozon.ru/v2/posting/fbo/list'
    since = time_since.isoformat()[:-3] + 'Z'
    to = time_to.isoformat()[:-3] + 'Z'
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