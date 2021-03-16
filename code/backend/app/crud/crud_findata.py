from typing import List, Any, Optional
# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from code.backend.app.crud.base import CRUDBase
from code.backend.app.models.findata import FinData
from code.backend.app.schemas.findata import FinDataCreate, FinDataUpdate


class CRUDFinData(CRUDBase[FinData, FinDataCreate, FinDataUpdate]):
    def get_all_by_posting_number(
            self, db: Session, *, posting_number: str,
    ) -> List[FinData]:
        return (
            db.query(self.model).filter(FinData.posting_number == posting_number).all()
        )

    def get_id_by_posting_number(
            self, db: Session, posting_number: str,
    ) -> Optional[int]:
        return db.query(self.model.id).filter(FinData.posting_number == posting_number).all()


findata = CRUDFinData(FinData)
