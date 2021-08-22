# from typing import TYPE_CHECKING -- unknown

from sqlalchemy import Column, Integer, String, JSON
# from sqlalchemy.orm import relationship -- connect tables

from code.backend.app.db.database import Base


# if TYPE_CHECKING:  -- unknown
#     from .user import User  # noqa: F401 -- unknown


class RawData(Base):
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True, index=True)
    posting_number = Column(String, index=True)
    order_id = Column(String, index=True)
    status = Column(String, index=True)
    json_data_2 = Column(JSON)
