import pytest
from uuid import UUID, uuid4
from app.services.delivery_service import DeliveryService
from app.repositories.local_delivery_repo import DeliveryRepo
from app.models.Delivery import Delivery
from app.repositories.local_deliveryman_repo import DeliverymanRepo
from app.models.Delivery import DeliveryStatuses

@pytest.fixture(scope='session')
def delivery_service() -> DeliveryService:
    return DeliveryService()

@pytest.fixture
def deliveryman_repo() -> DeliverymanRepo:
    return DeliverymanRepo()

@pytest.fixture(scope='session')
def first_delivery_data() -> tuple[UUID, UUID]:
    return (uuid4(), uuid4())


@pytest.fixture(scope='session')
def second_delivery_data() -> UUID:
    return (uuid4(), uuid4())


@pytest.fixture
def third_delivery_data() -> UUID:
    return (uuid4(), uuid4())

def test_empty_deliveries(delivery_service: DeliveryService):
    assert delivery_service.get_delivery() == []

def test_create_first_delivery(first_delivery_data: tuple[UUID, UUID], delivery_service: DeliveryService):
    delivery_id, order_id = first_delivery_data
    delivery = delivery_service.create_delivery(order_id=order_id, delivery_id=delivery_id)
    assert delivery.id == delivery_id
    assert delivery.order_id == order_id
    assert delivery.deliveryman == None
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.end_time == None

def test_create_second_delivery(second_delivery_data: tuple[UUID, UUID], delivery_service: DeliveryService):
    delivery_id, order_id = second_delivery_data
    delivery = delivery_service.create_delivery(order_id = order_id, delivery_id=delivery_id)
    assert delivery.id == delivery_id
    assert delivery.order_id == order_id
    assert delivery.deliveryman == None
    assert delivery.status == DeliveryStatuses.CREATED
    assert delivery.end_time == None


def test_create_first_delivery_repeat(first_delivery_data: tuple[UUID, UUID], delivery_service: DeliveryService):
    delivery_id, order_id = first_delivery_data
    with pytest.raises(ValueError):
        delivery_service.create_delivery(order_id=order_id, delivery_id=delivery_id)


def test_get_third_delivery(third_delivery_data: tuple[UUID,UUID], delivery_service: DeliveryService):
    delivery_id, order_id = third_delivery_data
    with pytest.raises(KeyError):
        delivery_service.get_delivery_by_id(delivery_id = delivery_id)

def test_accept_third_delivery(third_delivery_data: tuple[UUID,UUID], delivery_service: DeliveryService):
    delivery_id, order_id = third_delivery_data
    with pytest.raises(KeyError):
        delivery_service.activate_delivery(delivery_id=delivery_id)

def test_finish_third_delivery(third_delivery_data: tuple[UUID,UUID], delivery_service: DeliveryService):
    delivery_id, order_id = third_delivery_data
    with pytest.raises(KeyError):
        delivery_service.finish_delivery(delivery_id=delivery_id)