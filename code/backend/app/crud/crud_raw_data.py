from typing import List, Any, Optional, Union, Dict
# from fastapi.encoders import jsonable_encoder
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from code.backend.app.crud.base import CRUDBase
from code.backend.app.models.raw_data import RawData
from code.backend.app.schemas.raw_data import RawDataCreate, RawDataUpdate


class CRUDRawData(CRUDBase[RawData, RawDataCreate, RawDataUpdate]):
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

    def update(
        self,
        db: Session,
        *,
        db_obj: RawData,
        obj_in: RawDataUpdate
    ) -> RawData:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in
        # Переопределил , т.к. json_data - dict, поэтому obj_in.dict(exclude_unset=True) не то парсит.
        # if isinstance(obj_in, dict):
        #     update_data = obj_in
        # else:
        #     update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


raw_data = CRUDRawData(RawData)
