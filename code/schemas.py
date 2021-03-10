from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class Orders(BaseModel):
    posting_number: str
    order_id: str
    order_number: str
    status: str
    cancel_reason_id: int
    created_at: str
    in_process_at: str

    class Config:
        orm_mode = True


class OrderCreate(Orders):
    pass


class OrderProducts(BaseModel):
    posting_number: str
    sku: int
    name: str
    quantity: int
    offer_id: str
    price: float

    class Config:
        orm_mode = True


class OrderProductsCreate(OrderProducts):
    pass


class OrderAnalytics(BaseModel):
    posting_number: str
    region: str
    city: str
    delivery_type: str
    is_premium: bool
    payment_type_group_name: str
    warehouse_id: int
    warehouse_name: str

    class Config:
        orm_mode = True


class OrderAnalyticsCreate(OrderAnalytics):
    pass


class OrderFinData(BaseModel):
    posting_number: str
    commission_amount: int
    commission_percent: int
    payout: int
    product_id: int
    old_price: float
    price: float
    total_discount_value: float
    total_discount_percent: float
    # actions: List[Optional[str]] = None
    picking: Optional[str] = None
    quantity: int
    client_price: str

    class Config:
        orm_mode = True


class OrderFinDataCreate(OrderFinData):
    pass
