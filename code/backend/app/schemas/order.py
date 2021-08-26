from typing import Optional

from pydantic import BaseModel


# Shared properties
class OrderBase(BaseModel):
    order_id: Optional[int] = None
    order_number: Optional[str] = None
    posting_number: Optional[str] = None
    status: Optional[str] = None
    cancel_reason_id: Optional[int] = None
    created_at: Optional[str] = None
    in_process_at: Optional[str] = None
    order_sum: Optional[int] = None


# Properties to receive on item creation
class OrderCreate(OrderBase):
    pass


# Properties to receive on item update
class OrderUpdate(OrderBase):
    pass


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    order_id: Optional[int] = None
    order_number: Optional[str] = None
    posting_number: Optional[str] = None
    status: Optional[str] = None
    cancel_reason_id: Optional[int] = None
    created_at: Optional[str] = None
    in_process_at: Optional[str] = None
    order_sum: Optional[int] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    pass


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    pass
