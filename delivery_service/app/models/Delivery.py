import enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.Deliveryman import Deliveryman


class DeliveryStatuses(enum.Enum):
    CREATED = "created"
    ACTIVE = "active"
    DONE = "done"


class Delivery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    status: DeliveryStatuses
    deliveryman: Deliveryman | None = None
    address: str
    start_time: datetime
    end_time: datetime | None = None
