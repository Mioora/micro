from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from app.logger.logger_settings import LoggerSetup
from app.settings import settings
from logging import getLogger
from typing import Annotated
from app.request.request_module import get_userinfo
from app.services.order_service import OrderService

order_router = APIRouter(prefix='/order', tags=['Order'])
logger_setup = LoggerSetup()
logger = getLogger(__name__)

@order_router.get('/')
def get_orders(order_service: OrderService = Depends(OrderService)) -> list[dict]:
    logger.info('GET ON /')
    return order_service.get_orders()

@order_router.get('/{order_id}')
def get_orders(order_id: UUID, order_service: OrderService = Depends(OrderService)) -> dict:
    logger.info('GET ON / WITH ORDER')
    return order_service.get_order(order_id)


@order_router.post('/create')
def create_order(token: str = Header(), order_service: OrderService = Depends(OrderService)) -> dict:
    logger.info('POST ON /create')
    validate_user(token=token)
    return {'id': str(order_service.create_order().id)}


@order_router.post('/create/{address}')
def create_address_order(address: str, token: str = Header(), order_service: OrderService = Depends(OrderService)) -> dict:
    validate_user(token=token)
    logger.info("POST ON /create WITH ADDRESS")
    return {'id': str(order_service.create_order(address).id)}


@order_router.post('/{order_id}/activate/')
def activate_order(order_id: UUID, token: str = Header(), order_service: OrderService = Depends(OrderService)) -> dict:
    validate_moder(token=token)
    logger.info("POST ON /activate WITH ORDER")
    try:
        order = order_service.activate_order(order_id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={order_id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={order_id} cant be activated')


@order_router.get('/cook')
def get_cook(order_service: OrderService = Depends(OrderService)) -> list:
    logger.info("GET ON /cook")
    return order_service.get_cook()


@order_router.post('/{order_id}/cancel')
def cancel_order(order_id: UUID, token: str = Header(), order_service: OrderService = Depends(OrderService)) -> dict:
    validate_moder(token=token)
    logger.info("POST ON /cancel WITH ORDER")
    try:
        order = order_service.cancel_order(order_id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={order_id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={order_id} cant be canceled')


@order_router.post('/{order_id}/finish')
def finish_order(order_id: UUID, token: str = Header(), order_service: OrderService = Depends(OrderService)) -> dict:
    validate_moder(token=token)
    logger.info("POST ON /finish WITH ORDER")
    try:
        order = order_service.finish_order(order_id)
        return order.dict()
    except KeyError:
        raise HTTPException(404, f'Order with id={order_id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={order_id} cant be finished')


def validate_user(token: str):
    if settings.for_test is None:
        return
    response = get_userinfo(token=token)
    if response.status_code != 200:
        raise HTTPException(401, 'Bad User Info')

def validate_moder(token: str):
    if settings.for_test is None:
        return
    response = get_userinfo(token=token)
    if response.status_code != 200:
        raise HTTPException(401, 'Bad User Info')
    elif ('moder' not in response.json()['roles']):
        raise HTTPException(401, 'Account Dont have permission for this')