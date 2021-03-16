from typing import Optional

from pydantic import BaseModel


# Shared properties
class FinDataBase(BaseModel):
    posting_number: Optional[str] = None
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
class FinDataCreate(FinDataBase):
    pass


# Properties to receive on item update
class FinDataUpdate(FinDataBase):
    pass


# Properties shared by models stored in DB
class FinDataInDBBase(FinDataBase):
    id: int
    posting_number: Optional[str] = None
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
class FinData(FinDataInDBBase):
    pass


# Properties properties stored in DB
class FinDataInDB(FinDataInDBBase):
    pass
