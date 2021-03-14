from datetime import datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from code.backend.app import crud, models, schemas
from code.backend.app.api import deps
from code.backend.app.core.config import Settings
from code.backend.app.ozon_methods import fbo_orders
from code.backend.app.schemas import OrderCreate

router = APIRouter()


@router.get("/", response_model=List[schemas.Order])
def read_orders(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Retrieve orders.
    """
    orders = crud.order.get_multi(db, skip=skip, limit=limit)
    # if crud.user.is_superuser(current_user):
    #     items = crud.order.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.order.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return orders


@router.post("/", response_model=schemas.Order)
def create_order(
        *,
        db: Session = Depends(deps.get_db),
        order_in: schemas.OrderCreate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Create new order.
    """
    order = crud.order.create(db=db, obj_in=order_in)
    return order


@router.put("/{id}", response_model=schemas.Order)
def update_order(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        order_in: schemas.OrderUpdate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update an order.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # if not crud.user.is_superuser(current_user) and (order.owner_id != current_user.id):  -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    order = crud.order.update(db=db, db_obj=order, obj_in=order_in)
    return order


@router.get("/{id}", response_model=schemas.Order)
def read_order(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Get order by ID.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # if not crud.user.is_superuser(current_user) and (order.owner_id != current_user.id): -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    return order


@router.delete("/{id}", response_model=schemas.Order)
def delete_order(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Delete an order.
    """
    order = crud.order.get(db=db, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # if not crud.user.is_superuser(current_user) and (order.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.order.remove(db=db, id=id)
    return item


@router.get("/upsert/")  # , response_model=List[str]
def upsert_order(
        *,
        db: Session = Depends(deps.get_db),
        days: int = 1,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Upsert orders from Ozon.
    """
    list_orders = fbo_orders.list_orders(time_since=datetime.utcnow() - timedelta(days)) \
        .json()['result']
    result = {'created': [], 'updated': []}
    for elem in list_orders:
        order_in = schemas.OrderCreate(
            posting_number=elem['posting_number'], order_id=elem['order_id'], order_number=elem['order_number'],
            status=elem['status'], cancel_reason_id=elem['cancel_reason_id'], created_at=elem['created_at'],
            in_process_at=elem['in_process_at']
        )
        order_upd = schemas.OrderUpdate(
            posting_number=elem['posting_number'], order_id=elem['order_id'], order_number=elem['order_number'],
            status=elem['status'], cancel_reason_id=elem['cancel_reason_id'], created_at=elem['created_at'],
            in_process_at=elem['in_process_at']
        )
        order_in_db = crud.order.get_id_by_posting_number(db=db, posting_number=elem['posting_number'])
        if not order_in_db:
            create_order(db=db, order_in=order_in)
            result['created'].append(elem['posting_number'])
        else:
            id_for_upd = order_in_db[0][0]
            update_order(db=db, id=id_for_upd, order_in=order_upd)
            result['updated'].append(elem['posting_number'])
    return result


@router.post("/update/internal_orders/")  # , response_model=schemas.Order)
def upd_internal_orders(
        *,
        db: Session = Depends(deps.get_db),
        status: str = 'cancelled'
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update orders in DB by status.
    """
    orders = crud.order.get_all_by_status(db=db, status=status)
    for order in orders:
        id_upd = order.id
        post_num = order.posting_number
        order_in = fbo_orders.get_order(post_num).json()['result']
        # order
        # update_order(db=db, id=order.id, order_in=order_in)
    return order_in


@router.get("/test/")  # , response_model=schemas.Order)
def test_req_func(
        *,
        db: Session = Depends(deps.get_db),
        posting_number: str = '34857201-0007-1'
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update orders in DB by status.
    """
    res = crud.order.get_by_posting_number(db=db, posting_number=posting_number)
    return res
