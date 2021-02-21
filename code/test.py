import requests

# curl -X POST "https://api-seller.ozon.ru/v1/product/list"
# -H "accept: application/json"
# -H "Client-Id: 123090"
# -H "Api-Key: 87e400a8-a791-4cc5-ad98-82c032c90d5b"
# -H "Content-Type: application/json"
# -d "{}"

headers_d = {
    "accept": "application/json",
    "Client-Id": "123090",
    "Api-Key": "87e400a8-a791-4cc5-ad98-82c032c90d5b",
    "Content-Type": "application/json"
}


def product_info(headers): #, offer_id, product_id, sku
    url = 'https://api-seller.ozon.ru/v2/product/info'
    # sku = get_product_info_by_product_id(headers, product_id)['sku']
    body_d = {
        "offer_id": "uraala019",
        "product_id": 53503011,
        "sku": 231872934
    }
    return requests.post(url, headers=headers, data=body_d)


res = product_info(headers_d)
print(res.json())
