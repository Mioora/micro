import enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CookPositions(enum.Enum):
    TRAINEE = "trainee"
    COOK = "cook"
    SOUS_CHIEF = "sous chief"
    CHIEF = "chief"


class Cook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    surname: str
    position: CookPositions
