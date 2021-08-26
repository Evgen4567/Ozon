from starlette.responses import FileResponse

from code.backend.app import schemas


def parse_sales_to_insert(elem):
    return schemas.SalesCreate(
        posting_number=elem['posting_number'],
        order_id=elem['order_id'],
        order_number=elem['order_number'],
        status=elem['status'],
        cancel_reason_id=elem['cancel_reason_id'],
        created_at=elem['created_at'],
        in_process_at=elem['in_process_at'],
        sku=elem['products'][0]['sku'],
        name=elem['products'][0]['name'],
        quantity_products=elem['products'][0]['quantity'],
        offer_id=elem['products'][0]['offer_id'],
        price_products=elem['products'][0]['price'],
        region=elem['analytics_data']['region'],
        city=elem['analytics_data']['city'],
        delivery_type=elem['analytics_data']['delivery_type'],
        is_premium=elem['analytics_data']['is_premium'],
        payment_type_group_name=elem['analytics_data']['payment_type_group_name'],
        warehouse_id=elem['analytics_data']['warehouse_id'],
        warehouse_name=elem['analytics_data']['warehouse_name'],
        commission_amount=elem['financial_data']['products'][0]['commission_amount'],
        commission_percent=elem['financial_data']['products'][0]['commission_percent'],
        payout=elem['financial_data']['products'][0]['payout'],
        product_id=elem['financial_data']['products'][0]['product_id'],
        old_price=elem['financial_data']['products'][0]['old_price'],
        price=elem['financial_data']['products'][0]['price'],
        total_discount_value=elem['financial_data']['products'][0]['total_discount_value'],
        total_discount_percent=elem['financial_data']['products'][0]['total_discount_percent'],
        picking=elem['financial_data']['products'][0]['picking'],
        quantity=elem['financial_data']['products'][0]['quantity'],
        client_price=elem['financial_data']['products'][0]['client_price']
    )


def parse_sales_to_update(elem):
    return schemas.SalesUpdate(
        posting_number=elem['posting_number'],
        order_id=elem['order_id'],
        order_number=elem['order_number'],
        status=elem['status'],
        cancel_reason_id=elem['cancel_reason_id'],
        created_at=elem['created_at'],
        in_process_at=elem['in_process_at'],
        sku=elem['products'][0]['sku'],
        name=elem['products'][0]['name'],
        quantity_products=elem['products'][0]['quantity'],
        offer_id=elem['products'][0]['offer_id'],
        price_products=elem['products'][0]['price'],
        region=elem['analytics_data']['region'],
        city=elem['analytics_data']['city'],
        delivery_type=elem['analytics_data']['delivery_type'],
        is_premium=elem['analytics_data']['is_premium'],
        payment_type_group_name=elem['analytics_data']['payment_type_group_name'],
        warehouse_id=elem['analytics_data']['warehouse_id'],
        warehouse_name=elem['analytics_data']['warehouse_name'],
        commission_amount=elem['financial_data']['products'][0]['commission_amount'],
        commission_percent=elem['financial_data']['products'][0]['commission_percent'],
        payout=elem['financial_data']['products'][0]['payout'],
        product_id=elem['financial_data']['products'][0]['product_id'],
        old_price=elem['financial_data']['products'][0]['old_price'],
        price=elem['financial_data']['products'][0]['price'],
        total_discount_value=elem['financial_data']['products'][0]['total_discount_value'],
        total_discount_percent=elem['financial_data']['products'][0]['total_discount_percent'],
        picking=elem['financial_data']['products'][0]['picking'],
        quantity=elem['financial_data']['products'][0]['quantity'],
        client_price=elem['financial_data']['products'][0]['client_price']
    )


def parse_raw_data_to_insert(elem):
    return schemas.RawDataCreate(
        posting_number=elem['posting_number'],
        order_id=elem['order_id'],
        status=elem['status'],
        json_data=elem,
    )


def parse_raw_data_to_update(elem):
    return schemas.RawDataUpdate(
        posting_number=elem['posting_number'],
        order_id=elem['order_id'],
        status=elem['status'],
        json_data=elem,
    )


def sound_of_success():
    return FileResponse("money.mp3")


def parse_order_to_insert(elem):
    return schemas.OrderCreate(
        order_id=elem['order_id'],
        order_number=elem['order_number'],
        posting_number=elem['posting_number'],
        status=elem['status'],
        cancel_reason_id=elem['cancel_reason_id'],
        created_at=elem['created_at'],
        in_process_at=elem['in_process_at'],
        order_sum=sum([float(p['price']) for p in elem['products']]),
    )


def parse_order_to_update(elem):
    return schemas.OrderUpdate(
        order_id=elem['order_id'],
        order_number=elem['order_number'],
        posting_number=elem['posting_number'],
        status=elem['status'],
        cancel_reason_id=elem['cancel_reason_id'],
        created_at=elem['created_at'],
        in_process_at=elem['in_process_at'],
        order_sum=sum([float(p['price']) for p in elem['products']]),
    )
