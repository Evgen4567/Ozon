import test
from ozon_methods import product

# https://api-seller.ozon.ru/docs/

client_id = "123090"
api_key = "87e400a8-a791-4cc5-ad98-82c032c90d5b"
headers_d = {
        "accept": "application/json",
        "Client-Id": "123090",
        "Api-Key": "87e400a8-a791-4cc5-ad98-82c032c90d5b",
        "Content-Type": "application/json"
    }

if __name__ == "__main__":
    res = product.product_info(headers_d, "uraala019", 53503011, 231872934)
    # res = str(product.get_product_info_by_product_id(headers_d, 53503011)['sku'])
    print(res)
