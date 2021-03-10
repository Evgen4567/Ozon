import shutil
from typing import List, Optional

from fastapi.responses import FileResponse
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

headers_d = {
    "accept": "application/json",
    "Client-Id": "123090",
    "Api-Key": "87e400a8-a791-4cc5-ad98-82c032c90d5b",
    "Content-Type": "application/json"
}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/")  # , response_model=List[schemas.Item]
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return {"items": items}


# @app.get("/images/{path}")
@app.get("/")
async def read_item(path_img: str = "day_img.jpg"):
    path = "foodServer/images/" + path_img
    return FileResponse(path)


@app.post("/image")
async def image(image: UploadFile = File(...)):
    with open("foodServer/images/day_img.gif", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": image.filename}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.get("/orders", response_model=schemas.Orders)
async def get_orders_from_ozon():
    orders = crud.get_orders(headers_d)
    return {"orders": orders}