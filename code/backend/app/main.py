import requests
from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware

from code.backend.app.api.api_v1.api import api_router

from code.backend.app import models
from code.backend.app.db.database import SessionLocal, engine
from code.backend.app.core.config import Settings
# from personal_data import PersonalData


models.sales.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api_router, prefix=Settings.API_V1_STR)

# @app.get("/{id}")
# async def refresh():
#     print('server is started')
#     url = [PersonalData.HOST + "/api/v1/raw_data/upsert/?days_from=1",
#            PersonalData.HOST + "/api/v1/raw_data/update/by_status/"]
#     await refresher_bot(url)

# need to open ports 192.168.0.100 sudo nano /etc/hosts
# uvicorn code.backend.app.main:app --host 192.168.0.100 --port 80 --reload


# Добавить остальные таблицы с заказом

