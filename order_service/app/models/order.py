import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.cook import Cook


class OrderStatuses(enum.Enum):
    CREATED = "created"
    ACTIVATED = "active"
    DONE = "done"
    CANCELED = "canceled"


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date: datetime
    finish_date: datetime | None = None
    address: str | None = None
    status: OrderStatuses
    cook: Cook | None = None
