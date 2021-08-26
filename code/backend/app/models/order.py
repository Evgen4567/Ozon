# from typing import TYPE_CHECKING -- unknown

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, BigInteger
# from sqlalchemy.orm import relationship -- connect tables

from code.backend.app.db.database import Base

# if TYPE_CHECKING:  -- unknown
#     from .user import User  # noqa: F401 -- unknown


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(BigInteger, index=True)
    order_number = Column(String, index=True)
    posting_number = Column(String, index=True)
    status = Column(String, index=True)
    cancel_reason_id = Column(Integer, index=True)
    created_at = Column(String, index=True)
    in_process_at = Column(String, index=True)
    order_sum = Column(Integer, index=True)