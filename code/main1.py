from ozon_methods import product, fbo_orders
import pandas as pd
from datetime import datetime, timedelta

headers_d = {
        "accept": "application/json",
        "Client-Id": "123090",
        "Api-Key": "87e400a8-a791-4cc5-ad98-82c032c90d5b",
        "Content-Type": "application/json"
    }

if __name__ == "__main__":
    # res = product.product_info(headers_d, "uraala019", 53503011, 231872934)
    # res = str(product.get_product_info_by_product_id(headers_d, 53503011)['sku'])
    time_since = datetime(2021, 3, 6, microsecond=1)
    time_to = datetime(2021, 3, 10, microsecond=1)
    res = fbo_orders.list_orders(headers_d, time_since=time_since, time_to=time_to).json()['result']
    print(res[0])


