from typing import List, Any, Optional
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from code.backend.app.crud.base import CRUDBase
from code.backend.app.models.raw_data import RawData
from code.backend.app.schemas.raw_data import RawDataCreate, RawDataUpdate


class CRUDSales(CRUDBase[RawData, RawDataCreate, RawDataUpdate]):
    def get_all_by_posting_number(
            self, db: Session, *, posting_number: str,
    ) -> List[RawData]:
        return (
            db.query(self.model).filter(RawData.posting_number == posting_number).all()
        )

    def get_all_by_status(
            self, db: Session, status: List[str],
    ) -> List[RawData]:
        return db.query(self.model).filter(RawData.status.in_(status)).all()

    def get_id_by_posting_number(
            self, db: Session, posting_number: str,
    ) -> Optional[int]:
        return db.query(self.model.id).filter(RawData.posting_number == posting_number).all()


raw_data = CRUDSales(RawData)
