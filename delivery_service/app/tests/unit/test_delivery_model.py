import pytest
from datetime import datetime
from app.models.Deliveryman import Deliveryman
from app.models.Delivery import Delivery, DeliveryStatuses
from pydantic import ValidationError
from uuid import uuid4

@pytest.fixture()
def any_deliveryman() -> Deliveryman:
    return Deliveryman(id=uuid4(), name='deliveryman', surname='1')


def test_delivery_create(any_deliveryman: Deliveryman):
    id = uuid4()
    order_id = uuid4()
    status = DeliveryStatuses.DONE
    deliveryman = any_deliveryman
    address = 'address'
    start_time = datetime.now()
    end_time = datetime.now()

    delivery = Delivery(
        id=id,
        order_id=order_id,
        status=status,
        deliveryman=deliveryman,
        address=address,
        start_time=start_time,
        end_time=end_time
    )
    assert dict(delivery) == {
        'id': id,
        'order_id': order_id,
        'address': address,
        'status': status,
        'deliveryman': deliveryman,
        'start_time': start_time,
        'end_time': end_time
    }

def test_status_required(any_deliveryman: Deliveryman):
    with pytest.raises(ValidationError):
        Delivery(
            id=uuid4(),
            order_id=uuid4(),
            address='address',
            deliveryman=any_deliveryman,
            start_time=datetime.now(),
            end_time=datetime.now()
        )

def test_order_id_required(any_deliveryman: Deliveryman):
    with pytest.raises(ValidationError):
        Delivery(
            id=uuid4(),
            address='address',
            status=DeliveryStatuses.CREATED,
            deliveryman=any_deliveryman,
            start_time=datetime.now(),
            end_time=datetime.now()
        )
    
def test_id_required(any_deliveryman: Deliveryman):
    with pytest.raises(ValidationError):
        Delivery(
            order_id=uuid4(),
            address='address',
            status=DeliveryStatuses.CREATED,
            deliveryman=any_deliveryman,
            start_time=datetime.now(),
            end_time=datetime.now()
        )


def test_starttime_required(any_deliveryman: Deliveryman):
    with pytest.raises(ValidationError):
        Delivery(
            id=uuid4(),
            order_id=uuid4(),
            address='address',
            deliveryman=any_deliveryman,
            status=DeliveryStatuses.CREATED,
            end_time=datetime.now()
        )