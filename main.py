from fastapi import FastAPI
from api.crawling import router

app = FastAPI()

app.include_router(router, tags=["crawling"])
