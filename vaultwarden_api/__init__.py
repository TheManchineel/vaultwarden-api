from fastapi import FastAPI

from . import api_routes

app = FastAPI()

app.include_router(api_routes.router, prefix="/api")
