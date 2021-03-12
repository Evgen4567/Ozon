from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas
from .ozon_methods import order


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# TODO(upsert)
def orders_from_ozon_to_db(db: Session, headers: dict, dir: str = "desc",
                           time_since: datetime = datetime.utcnow() - timedelta(1),
                           time_to: datetime = datetime.utcnow(), limit: int = 50, offset: int = 0):
    list_orders = order.list_orders(headers, dir, time_since, time_to, limit, offset).json()['result']
    for elem in list_orders:
        if check_unique_order(db, elem['posting_number']) == 0:
            db_orders = models.Orders(
                posting_number=elem['posting_number'], order_id=elem['order_id'], order_number=elem['order_number'],
                status=elem['status'], cancel_reason_id=elem['cancel_reason_id'], created_at=elem['created_at'],
                in_process_at=elem['in_process_at']
            )
            db.add(db_orders)
            db.commit()
            db.refresh(db_orders)

        if check_unique_order_product(db, elem['posting_number']) == 0:
            elem_product = elem['products'][0]
            db_product = models.OrderProducts(
                posting_number=elem['posting_number'], sku=elem_product['sku'], name=elem_product['name'],
                quantity=elem_product['quantity'], offer_id=elem_product['offer_id'], price=elem_product['price']
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)

        if check_unique_order_analytics(db, elem['posting_number']) == 0:
            elem_analytics = elem['analytics_data']
            db_analytics = models.OrderAnalytics(
                posting_number=elem['posting_number'], region=elem_analytics['region'],
                city=elem_analytics['city'], delivery_type=elem_analytics['delivery_type'],
                is_premium=elem_analytics['is_premium'],
                payment_type_group_name=elem_analytics['payment_type_group_name'],
                warehouse_id=elem_analytics['warehouse_id'], warehouse_name=elem_analytics['warehouse_name'],
            )
            db.add(db_analytics)
            db.commit()
            db.refresh(db_analytics)

        if check_unique_order_findata(db, elem['posting_number']) == 0:
            elem_findata = elem['financial_data']['products'][0]
            db_findata = models.OrderFinData(
                posting_number=elem['posting_number'], commission_amount=elem_findata['commission_amount'],
                commission_percent=elem_findata['commission_percent'], payout=elem_findata['payout'],
                product_id=elem_findata['product_id'], old_price=elem_findata['old_price'],
                price=elem_findata['price'], total_discount_value=elem_findata['total_discount_value'],
                total_discount_percent=elem_findata['total_discount_percent'],  # actions=elem_findata['actions'],
                picking=elem_findata['picking'], quantity=elem_findata['quantity'],
                client_price=elem_findata['client_price']
            )
            db.add(db_findata)
            db.commit()
            db.refresh(db_findata)

    return "New orders insert in to db"


def check_unique_order(db: Session, posting_number: Optional[str]):
    return db.query(models.Orders).filter(models.Orders.posting_number == posting_number).count()


def check_unique_order_product(db: Session, posting_number: Optional[str]):
    return db.query(models.OrderProducts).filter(models.OrderProducts.posting_number == posting_number).count()


def check_unique_order_analytics(db: Session, posting_number: Optional[str]):
    return db.query(models.OrderAnalytics).filter(models.OrderAnalytics.posting_number == posting_number).count()


def check_unique_order_findata(db: Session, posting_number: Optional[str]):
    return db.query(models.OrderFinData).filter(models.OrderFinData.posting_number == posting_number).count()

# def create_user(db: Session, orders: schemas.OrderCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
