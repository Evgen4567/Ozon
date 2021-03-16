from starlette.responses import FileResponse

from code.backend.app import schemas


def parse_order_to_insert(elem):
    return schemas.OrderCreate(
        posting_number=elem['posting_number'], order_id=elem['order_id'], order_number=elem['order_number'],
        status=elem['status'], cancel_reason_id=elem['cancel_reason_id'], created_at=elem['created_at'],
        in_process_at=elem['in_process_at'])


def parse_order_to_update(elem):
    return schemas.OrderUpdate(
        posting_number=elem['posting_number'], order_id=elem['order_id'], order_number=elem['order_number'],
        status=elem['status'], cancel_reason_id=elem['cancel_reason_id'], created_at=elem['created_at'],
        in_process_at=elem['in_process_at']
    )

def parse_findata_to_insert(elem):
    findata = elem['financial_data']['products'][0]
    return schemas.FinDataCreate(
        posting_number=elem['posting_number'], commission_amount=findata['commission_amount'],
        commission_percent=findata['commission_percent'], payout=findata['payout'], product_id=findata['product_id'],
        old_price=findata['old_price'], price=findata['price'], total_discount_value=findata['total_discount_value'],
        total_discount_percent=findata['total_discount_percent'], picking=findata['picking'],
        quantity=findata['quantity'], client_price=findata['client_price'])


def parse_findata_to_update(elem):
    findata = elem['financial_data']['products'][0]
    return schemas.FinDataCreate(
        posting_number=elem['posting_number'], commission_amount=findata['commission_amount'],
        commission_percent=findata['commission_percent'], payout=findata['payout'], product_id=findata['product_id'],
        old_price=findata['old_price'], price=findata['price'], total_discount_value=findata['total_discount_value'],
        total_discount_percent=findata['total_discount_percent'], picking=findata['picking'],
        quantity=findata['quantity'], client_price=findata['client_price'])


def sound_of_success():
    return FileResponse("money.mp3")
