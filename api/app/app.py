from fastapi import FastAPI
from fastapi_pagination import add_pagination


import database
from routes import datasetRoute
from dependencies import get_db


database.db.connect()
database.db.close()

app = FastAPI()
sleep_time = 10

version_one = FastAPI()
version_one.include_router(datasetRoute.router)
add_pagination(version_one)

app.mount("/api/v1", version_one)