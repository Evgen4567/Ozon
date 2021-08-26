from typing import List, Any, Optional
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from code.backend.app.crud.base import CRUDBase
from code.backend.app.models.sales import Sales
from code.backend.app.schemas.sales import SalesCreate, SalesUpdate

sales = CRUDBase[Sales, SalesCreate, SalesUpdate]
