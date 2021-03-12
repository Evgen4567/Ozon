from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from code.backend.app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, index=True)
    order_id = Column(String, index=True)
    status = Column(String, index=True)
    cancel_reason_id = Column(Integer, index=True)
    created_at = Column(String, index=True)
    in_process_at = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="orders")

