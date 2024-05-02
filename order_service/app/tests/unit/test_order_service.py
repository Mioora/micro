import pytest
from uuid import UUID, uuid4
from app.services.order_service import OrderService
from app.models.order import OrderStatuses
from app.repositories.local_order_repo import OrderRepo

@pytest.fixture(scope='session')
def order_service() -> OrderService:
    return OrderService()

@pytest.fixture(scope='session')
def first_order_data() -> UUID:
    return uuid4()

@pytest.fixture(scope='session')
def second_order_data() -> tuple[UUID, str]:
    return (uuid4(), 'address')


def test_empty_order(order_service: OrderService):
    assert order_service.get_orders() == []


def test_cancel_first_order(first_order_data: UUID, order_service: OrderService):
    order_id = first_order_data
    with pytest.raises(KeyError):
        order_service.cancel_order(order_id=order_id)


def test_create_first_order(first_order_data: UUID, order_service: OrderService):
    order_id = first_order_data
    order = order_service.create_order(order_id=order_id)
    assert order.id == order_id
    assert order.date != None
    assert order.status == OrderStatuses.CREATED
    assert order.address == None
    assert order.cook == None
    assert order.finish_date == None


def test_finish_first_order(first_order_data: UUID, order_service: OrderService):
    order_id = first_order_data
    with pytest.raises(ValueError):
        order_service.finish_order(order_id=order_id)


def test_activate_first_order(first_order_data: UUID, order_service: OrderService):
    order_id = first_order_data
    order = order_service.activate_order(order_id=order_id)
    assert order.id == order_id
    assert order.date != None
    assert order.status == OrderStatuses.ACTIVATED
    assert order.address == None
    assert order.cook != None
    assert order.finish_date == None

def test_activate_first_order_repeat(first_order_data: UUID, order_service: OrderService):
    order_id = first_order_data
    with pytest.raises(ValueError):
        order_service.activate_order(order_id=order_id)


def test_create_second_order(second_order_data: tuple[UUID, str], order_service: OrderService):
    order_id, order_address = second_order_data
    order = order_service.create_order(order_id=order_id, address=order_address)
    assert order.id == order_id
    assert order.date != None
    assert order.status == OrderStatuses.CREATED
    assert order.address == order_address
    assert order.cook == None
    assert order.finish_date == None


def test_activate_second_order(second_order_data: tuple[UUID, str], order_service: OrderService):
    order_id, order_address = second_order_data
    order = order_service.activate_order(order_id=order_id)
    assert order.id == order_id
    assert order.date != None
    assert order.status == OrderStatuses.ACTIVATED
    assert order.address == order_address
    assert order.cook != None
    assert order.finish_date == None

def test_finish_second_order(second_order_data: tuple[UUID, str], order_service: OrderService):
    order_id, order_address = second_order_data
    order = order_service.finish_order(order_id=order_id)
    assert order.id == order_id
    assert order.date != None
    assert order.status == OrderStatuses.DONE
    assert order.address == order_address
    assert order.cook != None
    assert order.finish_date != None

def test_finish_second_order_repeat(second_order_data: tuple[UUID, str], order_service: OrderService):
    order_id, order_address = second_order_data
    with pytest.raises(ValueError):
        order_service.finish_order(order_id=order_id)


def test_cancel_second_order(second_order_data: tuple[UUID, str], order_service: OrderService):
    order_id, order_address = second_order_data
    with pytest.raises(ValueError):
        order_service.finish_order(order_id=order_id)
