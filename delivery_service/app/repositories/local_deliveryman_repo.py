from uuid import UUID, uuid4

from app.models.Deliveryman import Deliveryman

deliveryman: list[Deliveryman] = [
    Deliveryman(id=uuid4(), name="Имя 1", surname="Фамилия 1"),
    Deliveryman(id=uuid4(), name="Имя 2", surname="Фамилия 2"),
]


class DeliverymanRepo():
    def get_deliveryman(self) -> list[Deliveryman]:
        return deliveryman

    def get_deliveryman_by_id(self, deliveryman_id: UUID = None) -> Deliveryman:
        for employee in deliveryman:
            if employee.id == deliveryman_id:
                return employee
        return deliveryman[0]

