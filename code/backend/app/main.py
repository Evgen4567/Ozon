import requests
from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware

from code.backend.app.api.api_v1.api import api_router

from code.backend.app import models
from code.backend.app.db.database import SessionLocal, engine
from code.backend.app.core.config import Settings

models.order.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api_router, prefix=Settings.API_V1_STR)

# uvicorn code.backend.app.main:app --host 192.168.0.100 --port 80 --reload


# Добавить обновление по таймеру каждые 5 минут - upsert за последние сутки
# Обновление всех товаров 1 раз в неделю.
# Добавить остальные таблицы с заказом

