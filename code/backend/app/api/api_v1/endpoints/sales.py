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


@router.get("/", response_model=List[schemas.Sales])
def read_sales(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Retrieve sales.
    """
    sales = crud.sales.get_multi(db, skip=skip, limit=limit)
    # if crud.user.is_superuser(current_user):
    #     items = crud.order.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.order.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return sales


@router.post("/", response_model=schemas.Sales)
def create_sales(
        *,
        db: Session = Depends(deps.get_db),
        sales_in: schemas.SalesCreate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Create new sales.
    """
    sales = crud.sales.create(db=db, obj_in=sales_in)
    return sales


@router.put("/{id}", response_model=schemas.Sales)
def update_sales(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        sales_in: schemas.SalesUpdate,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Update an sales.
    """
    sales = crud.sales.get(db=db, id=id)
    if not sales:
        raise HTTPException(status_code=404, detail="Order not found")
    # if not crud.user.is_superuser(current_user) and (sales.owner_id != current_user.id):  -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    sales = crud.sales.update(db=db, db_obj=sales, obj_in=sales_in)
    return sales


@router.get("/{id}", response_model=schemas.Sales)
def read_sales_by_id(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Get sales by ID.
    """
    sales = crud.sales.get(db=db, id=id)
    if not sales:
        raise HTTPException(status_code=404, detail="Order not found")
    # if not crud.user.is_superuser(current_user) and (sales.owner_id != current_user.id): -- для авторизации
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    return sales


@router.delete("/{id}", response_model=schemas.Sales)
def delete_sales(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Delete an sales.
    """
    sales = crud.sales.get(db=db, id=id)
    if not sales:
        raise HTTPException(status_code=404, detail="Order not found")
    # if not crud.user.is_superuser(current_user) and (sales.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    sales = crud.sales.remove(db=db, id=id)
    return sales


@router.get("/upsert/")  # , response_model=List[str]
async def upsert_sales(
        *,
        db: Session = Depends(deps.get_db),
        days: int = 1,
        # current_user: models.User = Depends(deps.get_current_active_user), -- для авторизации
) -> Any:
    """
    Upsert orders from Ozon.
    """
    list_sales = fbo_orders.list_orders(time_since=datetime.utcnow() - timedelta(days))
    result = {'created': [], 'updated': []}
    for elem in list_sales:
        sales_ins = utils.parse_sales_to_insert(elem)
        sales_upd = utils.parse_sales_to_update(elem)
        sales_in_db = crud.sales.get_all_by_posting_number(db=db, posting_number=elem['posting_number'])
        if not sales_in_db:
            create_sales(db=db, sales_in=sales_ins)
            result['created'].append(elem['posting_number'])
        else:
            id_for_upd = sales_in_db[0].id
            update_sales(db=db, id=id_for_upd, sales_in=sales_upd)
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
    sales = crud.sales.get_all_by_status(db=db, status=status)
    for sale in sales:
        post_num = sale.posting_number
        sales_from_ozon = fbo_orders.get_order(post_num)
        sales_in = utils.parse_sales_to_update(sales_from_ozon)
        update_sales(db=db, id=sale.id, sales_in=sales_in)
        count_upd += 1
    return count_upd


@router.get("/test/")  # , response_model=schemas.Order)
def sound_of_success():
    return FileResponse("money.mp3")
