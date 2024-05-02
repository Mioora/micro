from uuid import UUID, uuid4
from typing import Annotated
from app.logger.logger_settings import LoggerSetup
from logging import getLogger
from app.request.request_module import get_userinfo
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from fastapi.security import OAuth2PasswordBearer
from app.services.delivery_service import DeliveryService
from app.settings import settings

delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])
logger_setup = LoggerSetup()
logger = getLogger(__name__)

@delivery_router.get('/')
def get_deliveries(delivery_service: DeliveryService = Depends(DeliveryService)) -> list[dict]:
    logger.info("GET on /")
    return delivery_service.get_delivery()

@delivery_router.post('/create')
def create_delivery(order_id: UUID = Body(), delivery_id: UUID | None = Body(default=None), token: str = Header(), delivery_service: DeliveryService = Depends(DeliveryService)) -> dict:
    logger.info("POST on /create")
    validate_user(token)
    try:
        delivery = delivery_service.create_delivery(order_id=order_id, delivery_id=delivery_id)
        return delivery.dict()
    except ValueError:
        raise HTTPException(404, f'Delivery with order_id={order_id} exists')
    except KeyError:
        raise HTTPException(404, f'Delivery with this delivery_id exists')


@delivery_router.post('/activate')
def activate_delivery(delivery_id: UUID, token: str = Header(), delivery_service: DeliveryService = Depends(DeliveryService)) -> dict:
    logger.info("POST on /activate")
    validate_moder(token)
    try:
        delivery = delivery_service.activate_delivery(delivery_id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={delivery_id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={delivery_id} cannot be activated')


@delivery_router.get('/deliveryman')
def get_deliveryman(delivery_service: DeliveryService = Depends(DeliveryService)) -> list:
    logger.info("GET on /deliveryman")
    return delivery_service.get_deliveryman()


@delivery_router.post('/finish')
def finish_delivery(delivery_id: UUID, token: str = Header(), delivery_service: DeliveryService = Depends(DeliveryService)) -> dict:
    logger.info("POST on /finish")
    validate_moder(token=token)
    try:
        delivery = delivery_service.finish_delivery(delivery_id)
        return delivery.dict()
    except KeyError:
        raise HTTPException(404, f'Delivery with id={delivery_id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={delivery_id} cannot be finished')
    

def validate_moder(token: str):
    if (settings.for_test is None):
        return
    response = get_userinfo(token=token)
    if (response == None or response.status_code != 200):
        raise HTTPException(401, 'Account not found')
    elif ('moder' not in response.json()['roles']):
        raise HTTPException(401, 'Account dont have permissions')
    
def validate_user(token: str):
    logger.info('validation')
    if (settings.for_test is None):
        return
    response = get_userinfo(token=token)
    logger.info('try to validate user')
    if (response == None or response.status_code != 200):
        raise HTTPException(401, 'Account not found')