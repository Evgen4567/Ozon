import requests
from datetime import datetime, timedelta

from code.backend.app.core.config import Settings


def list_orders(dir="asc",
                time_since: datetime = datetime.utcnow() - timedelta(1),
                time_to: datetime = datetime.utcnow(),
                limit=50, offset=0):
    # time_since = datetime.utcnow() - timedelta(days_ago)
    headers = Settings.HEADERS
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


def get_order(posting_number: str, analytics_data: bool = True, financial_data: bool = True):
    url = 'https://api-seller.ozon.ru/v2/posting/fbo/get'
    headers = Settings.HEADERS
    body_d = {
        "posting_number": posting_number,
        "with": {
            "analytics_data": analytics_data,
            "financial_data": financial_data
        }
    }
    return requests.post(url, headers=headers, json=body_d)
