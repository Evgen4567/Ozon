from datetime import datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse, FileResponse

from code.backend.app import crud, models, schemas
from code.backend.app.api import deps
from code.backend.app.api.api_v1.endpoints import utils
from code.backend.app.ozon_methods import fbo_orders


router = APIRouter()


@router.get("/", response_model=List[schemas.FinData])
def read_findata(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Retrieve findata of orders.
    """
    findata = crud.findata.get_multi(db, skip=skip, limit=limit)
    # if crud.user.is_superuser(current_user):
    #     items = crud.order.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.order.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return findata


@router.post("/", response_model=schemas.FinData)
def create_findata(
        *,
        db: Session = Depends(deps.get_db),
        findata_in: schemas.FinDataUpdate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Create new findata of order.
    """
    findata = crud.findata.create(db=db, obj_in=findata_in)
    return findata


@router.put("/{id}", response_model=schemas.FinData)
def update_findata(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        findata_in: schemas.FinDataUpdate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update an findata of order.
    """
    findata = crud.findata.get(db=db, id=id)
    if not findata:
        raise HTTPException(status_code=404, detail="Findata of order not found")
    # if not crud.user.is_superuser(current_user) and (order.owner_id != current_user.id):  -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    findata = crud.findata.update(db=db, db_obj=findata, obj_in=findata_in)
    return findata


@router.get("/{id}", response_model=schemas.FinData)
def read_findata(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Get order by ID.
    """
    findata = crud.order.get(db=db, id=id)
    if not findata:
        raise HTTPException(status_code=404, detail="Findata not found")
    # if not crud.user.is_superuser(current_user) and (order.owner_id != current_user.id): -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    return findata


@router.delete("/{id}", response_model=schemas.FinData)
def delete_findata(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Delete an findata of order.
    """
    findata = crud.findata.get(db=db, id=id)
    if not findata:
        raise HTTPException(status_code=404, detail="Findata not found")
    # if not crud.user.is_superuser(current_user) and (order.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    findata = crud.findata.remove(db=db, id=id)
    return findata


@router.get("/upsert/")  # , response_model=List[str]
async def upsert_findata(
        *,
        db: Session = Depends(deps.get_db),
        days: int = 1,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Upsert orders from Ozon.
    """
    list_findata = fbo_orders.list_orders(time_since=datetime.utcnow() - timedelta(days))
    result = {'created': [], 'updated': []}
    for elem in list_findata:
        findata_ins = utils.parse_findata_to_insert(elem)
        findata_upd = utils.parse_findata_to_update(elem)
        findata_in_db = crud.findata.get_all_by_posting_number(db=db, posting_number=elem['posting_number'])
        if not findata_in_db:
            create_findata(db=db, findata_in=findata_ins)
            result['created'].append(elem['posting_number'])
        else:
            id_for_upd = findata_in_db[0].id
            update_findata(db=db, id=id_for_upd, findata_in=findata_upd)
            result['updated'].append(elem['posting_number'])
    return result


@router.post("/update/by_status/")  # , response_model=schemas.Order)
async def upd_findata_by_status_order(
        *,
        db: Session = Depends(deps.get_db),
        status=None
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update orders in DB by status.
    """
    if status is None:
        status = ["awaiting_approve", "awaiting_packaging", "awaiting_deliver", "delivering", "driver_pickup"]
    order_in, count_upd = 0, 0
    orders = crud.order.get_all_by_status(db=db, status=status)
    for order in orders:
        post_num = order.posting_number
        findata_id = crud.findata.get_id_by_posting_number(db=db, posting_number=post_num)
        findata_from_ozon = fbo_orders.get_order(post_num)
        findata_in = utils.parse_findata_to_update(findata_from_ozon)
        update_findata(db=db, id=findata_id, findata_in=findata_in)
        count_upd += 1
    return count_upd

