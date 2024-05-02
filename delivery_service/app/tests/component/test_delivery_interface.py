import pytest
import requests
from app.models.Delivery import Delivery, DeliveryStatuses
from fastapi import HTTPException
from uuid import UUID, uuid4
import time


time.sleep(1)
base_url = 'http://localhost:80/api/delivery/'

@pytest.fixture(scope='session')
def first_delivery_data() -> tuple[UUID, UUID, dict]:
    return (uuid4(), uuid4(), {'token': ''})

@pytest.fixture(scope='session')
def second_delivery_data() -> tuple[UUID, UUID, dict]:
    return (uuid4(), uuid4(), {'token':''})


def test_get_delivery_empty() -> None:
    request = requests.get(base_url)
    assert request.status_code == 200
    assert request.json() == []

def test_add_first_delivery(first_delivery_data: tuple[UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = first_delivery_data
    json = {'order_id': str(order_id), 'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}create', json=json, headers=header)
    delivery = Delivery.model_validate(request.json())
    assert request.status_code == 200
    assert delivery.id == delivery_id
    assert delivery.order_id == order_id
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.address == 'address'
    assert delivery.deliveryman == None
    assert delivery.end_time == None

def test_finish_first_delivery(first_delivery_data: tuple[UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = first_delivery_data
    json = {'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}finish', params=json, headers = header)
    assert request.status_code == 400

def test_activate_first_delivery(first_delivery_data: tuple[UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = first_delivery_data
    json = {'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}activate', params=json, headers=header)
    delivery = Delivery.model_validate(request.json())
    assert request.status_code == 200
    assert delivery.id == delivery_id
    assert delivery.order_id == order_id
    assert delivery.status == DeliveryStatuses.ACTIVE
    assert delivery.address == 'address'
    assert delivery.deliveryman != None
    assert delivery.start_time != None
    assert delivery.end_time == None


def test_activate_first_delivery_repeat(first_delivery_data: tuple[UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = first_delivery_data
    json = {'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}activate', params=json, headers=header)
    assert request.status_code == 400


def test_activate_second_delivery(second_delivery_data: tuple[UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = second_delivery_data
    json = {'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}activate', params=json, headers=header)
    assert request.status_code == 404


def test_finish_second_delivery(second_delivery_data: tuple[UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = second_delivery_data
    json = {'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}finish', params=json, headers=header)
    assert request.status_code == 404


def test_finish_first_delivery_repeat(first_delivery_data: tuple[UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = first_delivery_data
    json = {'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}finish', params=json, headers=header)
    delivery = Delivery.model_validate(request.json())
    assert request.status_code == 200
    assert delivery.id == delivery_id
    assert delivery.order_id == order_id
    assert delivery.status == DeliveryStatuses.DONE
    assert delivery.address == 'address'
    assert delivery.deliveryman != None
    assert delivery.start_time != None
    assert delivery.end_time != None


def test_activate_first_delivery_rep(first_delivery_data: tuple [UUID, UUID, dict]) -> None:
    order_id, delivery_id, header = first_delivery_data
    json = {'delivery_id': str(delivery_id)}
    request = requests.post(f'{base_url}finish', params=json, headers=header)
    assert request.status_code == 400




