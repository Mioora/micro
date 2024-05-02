import asyncio
import time
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.endpoints.delivery_endpoints import delivery_router
from prometheus_fastapi_instrumentator import Instrumentator
from logging import Logger, getLogger
from app.logger.logger_settings import LoggerSetup
from fastapi import FastAPI, Depends, Body
from app.settings import settings
from app import rabbitmq
from app.request.request_module import get_token

oauth_sceme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI(title="Delivery Service")
logger_setup = LoggerSetup()

@app.on_event('startup')
def startup():
    logger = getLogger(__name__)
    logger.info(f"TESTED BUILD {str(settings.for_test)}")
    logger.info("delivery_service app startup")
    if (settings.for_test is not None):
        logger.info('rabbitmq startup')
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(rabbitmq.consume(loop))

@app.on_event('shutdown')
def shutdown():
    logger = getLogger(__name__)
    logger.info("delivery_service app shutdown")

@app.post('/auth')
def auth(username: Annotated[str, Body()], password: Annotated[str, Body()]):
    data = get_token(username, password)
    return({'token' : data.json()['access_token']})

app.include_router(delivery_router, prefix='/api')

Instrumentator().instrument(app).expose(app)