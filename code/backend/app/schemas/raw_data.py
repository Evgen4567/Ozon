from typing import Optional, List, Any, Dict, AnyStr, Union

from pydantic import BaseModel


# Shared properties
class RawDataBase(BaseModel):
    posting_number: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    json_data_2: Dict[AnyStr, Any] = None  # Union[List[Any], Dict[AnyStr, Any]] = None


# Properties to receive on item creation
class RawDataCreate(RawDataBase):
    pass


# Properties to receive on item update
class RawDataUpdate(RawDataBase):
    pass


# Properties shared by models stored in DB
class RawDataInDBase(RawDataBase):
    id: int
    posting_number: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    json_data_2: Dict[AnyStr, Any] = None  # Union[List[Any], Dict[AnyStr, Any]] = None

    class Config:
        orm_mode = True


# Properties to return to client
class RawData(RawDataInDBase):
    pass


# Properties properties stored in DB
class RawDataInDB(RawDataInDBase):
    pass
