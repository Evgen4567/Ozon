# from typing import TYPE_CHECKING -- unknown

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
# from sqlalchemy.orm import relationship -- connect tables

from code.backend.app.db.database import Base

# if TYPE_CHECKING:  -- unknown
#     from .user import User  # noqa: F401 -- unknown


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, index=True)
    order_id = Column(String, index=True)
    order_number = Column(String, index=True)
    status = Column(String, index=True)
    cancel_reason_id = Column(Integer, index=True)
    created_at = Column(String, index=True)
    in_process_at = Column(String, index=True)
    sku = Column(Integer, index=True)
    name = Column(String, index=True)
    quantity_products = Column(Integer, index=True)
    offer_id = Column(String, index=True)
    price_products = Column(String, index=True)
    region = Column(String, index=True)
    city = Column(String, index=True)
    delivery_type = Column(String, index=True)
    is_premium = Column(Boolean, index=True)
    payment_type_group_name = Column(String, index=True)
    warehouse_id = Column(Integer, index=True)
    warehouse_name = Column(String, index=True)
    commission_amount = Column(Float, index=True)
    commission_percent = Column(Float, index=True)
    payout = Column(Float, index=True)
    product_id = Column(Integer, index=True)
    old_price = Column(Float, index=True)
    price = Column(Float, index=True)
    total_discount_value = Column(Float, index=True)
    total_discount_percent = Column(Float, index=True)
    picking = Column(String, index=True)
    quantity = Column(Float, index=True)
    client_price = Column(String, index=True)