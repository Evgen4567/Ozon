# from typing import TYPE_CHECKING -- unknown

from sqlalchemy import Column, ForeignKey, Integer, String, Float
# from sqlalchemy.orm import relationship -- connect tables

from code.backend.app.db.database import Base

# if TYPE_CHECKING:  -- unknown
#     from .user import User  # noqa: F401 -- unknown


class FinData(Base):
    __tablename__ = "findata"
    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, index=True)
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
