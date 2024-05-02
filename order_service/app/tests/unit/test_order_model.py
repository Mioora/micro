import pytest
from datetime import datetime
from app.models.order import Order, OrderStatuses
from app.models.cook import Cook, CookPositions
from pydantic import ValidationError
from uuid import uuid4


def test_create_order():
    order_id = uuid4()
    order_date = datetime.now()
    order_status = OrderStatuses.CREATED

    order = Order(id=order_id, date=order_date, status=order_status)

    assert order.id == order_id
    assert order.date == order_date
    assert order.finish_date == None
    assert order.address == None
    assert order.status == OrderStatuses.CREATED
    assert order.cook == None


def test_create_address_order():
    order_id = uuid4()
    order_date = datetime.now()
    order_status = OrderStatuses.CREATED
    order_address = 'address'

    order = Order(
        id=order_id, 
        date=order_date, 
        status=order_status,
        address=order_address)

    assert order.id == order_id
    assert order.date == order_date
    assert order.finish_date == None
    assert order.address == 'address'
    assert order.status == OrderStatuses.CREATED
    assert order.cook == None

def test_date_required():
    with pytest.raises(ValidationError):
        Order(
            id=uuid4(),
            status=OrderStatuses.CREATED
        )

def test_status_created():
    with pytest.raises(ValidationError):
        Order(
            id=uuid4(),
            date=datetime.now()
        )


def test_id_required():
    with pytest.raises(ValidationError):
        Order(
            date=datetime.now(),
            status=OrderStatuses.CREATED
        )