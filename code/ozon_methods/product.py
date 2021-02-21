import requests


def to_archive(headers, product_id):
    url = 'https://api-seller.ozon.ru/v1/product/archive'
    body_d = {
        "product_id": [product_id]
    }
    return requests.post(url, headers=headers, data=body_d)


def product_info(headers, offer_id, product_id, sku):
    url = 'https://api-seller.ozon.ru/v2/product/info'
    # sku = get_product_info_by_product_id(headers, product_id)['sku']
    body_d = {
        "offer_id": offer_id,
        "product_id": product_id,
        "sku": sku
    }
    return requests.post(url, headers=headers, data=body_d)


def product_info_list(headers, offer_id_list, product_id_list, list_sku):
    url = 'https://api-seller.ozon.ru/v2/product/info'
    body_d = {
        "offer_id": offer_id_list,
        "product_id": product_id_list,
        "sku": list_sku
    }
    return requests.post(url, headers=headers, data=body_d)


def get_product_info_by_product_id(headers, product_id):
    url = 'https://api-seller.ozon.ru/v1/products/info/' + str(product_id)
    return requests.get(url, headers=headers).json()['result']
