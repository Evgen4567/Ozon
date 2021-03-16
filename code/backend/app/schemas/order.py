from typing import Optional

from pydantic import BaseModel


# Shared properties
class OrderBase(BaseModel):
    posting_number: Optional[str] = None
    order_id: Optional[str] = None
    order_number: Optional[str] = None
    status: Optional[str] = None
    cancel_reason_id: Optional[int] = None
    created_at: Optional[str] = None
    in_process_at: Optional[str] = None
    sku: Optional[int] = None
    name: Optional[str] = None
    quantity_products: Optional[int] = None
    offer_id: Optional[str] = None
    price_products: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    delivery_type: Optional[str] = None
    is_premium: Optional[bool] = None
    payment_type_group_name: Optional[str] = None
    warehouse_id: Optional[int] = None
    warehouse_name: Optional[str] = None
    commission_amount: Optional[float] = None
    commission_percent: Optional[float] = None
    payout: Optional[float] = None
    product_id: Optional[int] = None
    old_price: Optional[float] = None
    price: Optional[float] = None
    total_discount_value: Optional[float] = None
    total_discount_percent: Optional[float] = None
    picking: Optional[str] = None
    quantity: Optional[float] = None
    client_price: Optional[str] = None


# Properties to receive on item creation
class OrderCreate(OrderBase):
    pass


# Properties to receive on item update
class OrderUpdate(OrderBase):
    pass


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    posting_number: Optional[str] = None
    order_id: Optional[str] = None
    order_number: Optional[str] = None
    status: Optional[str] = None
    cancel_reason_id: Optional[int] = None
    created_at: Optional[str] = None
    in_process_at: Optional[str] = None
    sku: Optional[int] = None
    name: Optional[str] = None
    quantity_products: Optional[int] = None
    offer_id: Optional[str] = None
    price_products: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    delivery_type: Optional[str] = None
    is_premium: Optional[bool] = None
    payment_type_group_name: Optional[str] = None
    warehouse_id: Optional[int] = None
    warehouse_name: Optional[str] = None
    commission_amount: Optional[float] = None
    commission_percent: Optional[float] = None
    payout: Optional[float] = None
    product_id: Optional[int] = None
    old_price: Optional[float] = None
    price: Optional[float] = None
    total_discount_value: Optional[float] = None
    total_discount_percent: Optional[float] = None
    picking: Optional[str] = None
    quantity: Optional[float] = None
    client_price: Optional[str] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    pass


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    pass
