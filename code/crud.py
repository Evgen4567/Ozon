from datetime import datetime, timedelta
from typing import List

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


def orders_from_ozon_to_db(db: Session, orderproducts: List[schemas.OrderProductsCreate],
        headers: dict, dir: str="desc", time_since: datetime = datetime.utcnow()-timedelta(5),
        time_to: datetime=datetime.utcnow(), limit: int = 50, offset: int = 0):
    list_orders = order.list_orders(headers, dir, time_since, time_to, limit, offset).json()['result']
    for elem in list_orders:
        elem_product = elem['products'][0]
        db_product = models.OrderProducts(
            posting_number=elem['posting_number'],
            sku=elem_product['sku'],
            name=elem_product['name'],
            quantity=elem_product['quantity'],
            offer_id=elem_product['offer_id'],
            price=elem_product['price'],
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

    return "db_product complete!"


# def create_user(db: Session, orders: schemas.OrderCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
