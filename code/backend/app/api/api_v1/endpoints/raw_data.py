from datetime import datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from code.backend.app import crud, schemas
from code.backend.app.api import deps
from code.backend.app.api.api_v1.endpoints import utils
from code.backend.app.ozon_methods import fbo_orders

router = APIRouter()


@router.get("/", response_model=List[schemas.RawData])
def read_sales(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Retrieve raw_data.
    """
    raw_data = crud.raw_data.get_multi(db, skip=skip, limit=limit)
    # if crud.user.is_superuser(current_user):
    #     items = crud.order.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.order.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return raw_data


@router.post("/", response_model=schemas.RawData)
def create_sales(
        *,
        db: Session = Depends(deps.get_db),
        raw_data_in: schemas.RawDataCreate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Create new raw_data.
    """
    raw_data = crud.raw_data.create(db=db, obj_in=raw_data_in)
    return raw_data


@router.put("/{id}", response_model=schemas.RawData)
def update_sales(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        raw_data_in: schemas.RawDataUpdate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update an raw_data.
    """
    raw_data = crud.raw_data.get(db=db, id=id)
    if not raw_data:
        raise HTTPException(status_code=404, detail="raw_data not found")
    # if not crud.user.is_superuser(current_user) and (sales.owner_id != current_user.id):  -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    raw_data = crud.raw_data.update(db=db, db_obj=raw_data, obj_in=raw_data_in)
    return raw_data


@router.get("/{id}", response_model=schemas.RawData)
def read_sales_by_id(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Get raw_data by ID.
    """
    raw_data = crud.raw_data.get(db=db, id=id)
    if not raw_data:
        raise HTTPException(status_code=404, detail="raw_data not found")
    # if not crud.user.is_superuser(current_user) and (sales.owner_id != current_user.id): -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    return raw_data


@router.delete("/{id}", response_model=schemas.RawData)
def delete_sales(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Delete an raw_data.
    """
    raw_data = crud.raw_data.get(db=db, id=id)
    if not raw_data:
        raise HTTPException(status_code=404, detail="raw_data not found")
    # if not crud.user.is_superuser(current_user) and (sales.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    raw_data = crud.raw_data.remove(db=db, id=id)
    return raw_data


@router.get("/upsert/")  # , response_model=List[str]
async def upsert_sales(
        *,
        db: Session = Depends(deps.get_db),
        days_from: int = 1,
        days_to: int = 0
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Upsert orders from Ozon.
    """
    list_sales = fbo_orders.list_orders(time_since=datetime.utcnow() - timedelta(days_from),
                                        time_to=datetime.utcnow() - timedelta(days_to))
    result = {'created': [], 'updated': []}
    for elem in list_sales:
        raw_data_ins = utils.parse_raw_data_to_insert(elem)
        raw_data_upd = utils.parse_raw_data_to_update(elem)
        raw_data_in_db = crud.raw_data.get_all_by_posting_number(db=db, posting_number=elem['posting_number'])
        if not raw_data_in_db:
            create_sales(db=db, raw_data_in=raw_data_ins)
            result['created'].append(elem['posting_number'])
        else:
            id_for_upd = raw_data_in_db[0].id
            update_sales(db=db, id=id_for_upd, raw_data_in=raw_data_upd)
            result['updated'].append(elem['posting_number'])
    return result


@router.post("/update/by_status/")  # , response_model=schemas.Sales)
async def upd_sales_by_status(
        *,
        db: Session = Depends(deps.get_db),
        status=None
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update sales in DB by status.
    """
    if status is None:
        status = ["awaiting_approve", "awaiting_packaging", "awaiting_deliver", "delivering", "driver_pickup"]
    sales_in, count_upd = 0, 0
    sales = crud.raw_data.get_all_by_status(db=db, status=status)
    for sale in sales:
        post_num = sale.posting_number
        sales_from_ozon = fbo_orders.get_order(post_num)
        sales_in = utils.parse_raw_data_to_update(sales_from_ozon)
        update_sales(db=db, id=sale.id, raw_data_in=sales_in)
        count_upd += 1
    return count_upd

