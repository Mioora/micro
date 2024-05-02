from app.endpoints.order_endpoints import order_router
from prometheus_fastapi_instrumentator import Instrumentator
from app.logger.logger_settings import LoggerSetup
from typing import Annotated
from app.settings import settings
from logging import getLogger
from fastapi import FastAPI, Body, HTTPException
from app.request.request_module import get_token

app = FastAPI(title="Order Service")
if (not settings.for_test):
    logger_setup = LoggerSetup()

@app.on_event("startup")
def startup():
    logger = getLogger(__name__)
    logger.info('ORDER SERVICE INITIALIZED')

@app.on_event("shutdown")
def shutdown():
    logger = getLogger(__name__)
    logger.info('ORDER SERVICE SHUTDOWN')

@app.post("/auth")
def auth(username: Annotated[str, Body()], password: Annotated[str, Body()]):
    response = get_token(username=username, password=password)
    if (response.status_code != 200):
        raise HTTPException(401, "bad user data")
    return {'token': response.json()['access_token']}

    
app.include_router(order_router, prefix='/api')


Instrumentator().instrument(app).expose(app)