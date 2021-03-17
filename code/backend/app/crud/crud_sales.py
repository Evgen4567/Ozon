from typing import List, Any, Optional
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from code.backend.app.crud.base import CRUDBase
from code.backend.app.models.sales import Sales
from code.backend.app.schemas.sales import SalesCreate, SalesUpdate


class CRUDSales(CRUDBase[Sales, SalesCreate, SalesUpdate]):
    def get_all_by_posting_number(
            self, db: Session, *, posting_number: str,
    ) -> List[Sales]:
        return (
            db.query(self.model).filter(Sales.posting_number == posting_number).all()
        )

    def get_all_by_status(
            self, db: Session, status: List[str],
    ) -> List[Sales]:
        return db.query(self.model).filter(Sales.status.in_(status)).all()

    def get_id_by_posting_number(
            self, db: Session, posting_number: str,
    ) -> Optional[int]:
        return db.query(self.model.id).filter(Sales.posting_number == posting_number).all()


sales = CRUDSales(Sales)
