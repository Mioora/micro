import pytest
import requests
from app.models.order import Order, OrderStatuses
from fastapi import HTTPException
from logging import getLogger
from uuid import UUID, uuid4
import time

time.sleep(1)
base_url = 'http://localhost:81/api/order/'
header = {'token': ''}

def test_get_order_empty() -> None:
    request = requests.get(base_url)
    assert request.status_code == 200
    assert request.json() == []

@pytest.fixture(scope='session')
def first_order_data() -> UUID:
    return UUID(requests.post(base_url+'create', headers=header).json()['id'])

@pytest.fixture(scope='session')
def second_order_data() -> UUID:
    address = "test_address"
    return UUID(requests.post(f'{base_url}create/{address}', headers=header).json()['id'])

@pytest.fixture(scope='session')
def third_order_data() -> UUID:
    return uuid4()


def test_activate_first_order(first_order_data: UUID) -> None:
    order_id = first_order_data
    request = requests.post(f'{base_url}{order_id}/activate', headers=header)
    order = Order.model_validate(request.json())
    assert request.status_code == 200
    assert order.id == order_id
    assert order.status == OrderStatuses.ACTIVATED
    assert order.date != None
    assert order.finish_date == None
    assert order.address == None
    assert order.cook != None


def test_finish_first_order(first_order_data: UUID) -> None:
    order_id = first_order_data
    request = requests.post(f'{base_url}{order_id}/finish', headers=header)
    order = Order.model_validate(request.json())
    assert request.status_code == 200
    assert order.id == order_id
    assert order.status == OrderStatuses.DONE
    assert order.date != None
    assert order.finish_date != None
    assert order.address == None
    assert order.cook != None


def test_activate_first_order_repeat(first_order_data: UUID) -> None:
    order_id = first_order_data
    request = requests.post(f'{base_url}{order_id}/activate', headers=header)
    assert request.status_code == 400


def test_activate_second_order(second_order_data: UUID) -> None:
    order_id = second_order_data
    request = requests.post(f'{base_url}{order_id}/activate', headers=header)
    order = Order.model_validate(request.json())
    assert request.status_code == 200
    assert order.id == order_id
    assert order.status == OrderStatuses.ACTIVATED
    assert order.date != None
    assert order.finish_date == None
    assert order.address == 'test_address'
    assert order.cook != None


def test_activate_second_order_repeat(second_order_data: UUID) -> None:
    order_id = second_order_data
    request = requests.post(f'{base_url}{order_id}/activate', headers=header)
    assert request.status_code == 400


def test_cancel_first_order(first_order_data: UUID) -> None:
    order_id = first_order_data
    request = requests.post(f'{base_url}{order_id}/cancel', headers=header)
    assert request.status_code == 400

def test_activate_not_exists_order(third_order_data: UUID) -> None:
    order_id = third_order_data
    request = requests.post(f'{base_url}{order_id}/activate', headers=header)
    assert request.status_code == 404