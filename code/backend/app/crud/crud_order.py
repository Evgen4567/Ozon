from typing import List, Any
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from code.backend.app.crud.base import CRUDBase
from code.backend.app.models.order import Order
from code.backend.app.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_all_by_posting_number(
            self, db: Session, *, posting_number: str,
    ) -> List[Order]:
        return (
            db.query(self.model).filter(Order.posting_number == posting_number).all()
        )

    def get_id_by_posting_number(
            self, db: Session, *, posting_number: str,
    ) -> Any:
        print("get_id_by_posting_number started")
        return (
            db.query(self.model.id).filter(Order.posting_number == posting_number).all()
        )


order = CRUDOrder(Order)
