from uuid import UUID

from app.models.cook import Cook, CookPositions

cooks: list[Cook] = [
    Cook(id='a8242b14-4433-495a-a43e-12d980d3ea7f', name="Имя 1", surname="Фамилия 1", position=CookPositions.TRAINEE),
    Cook(id='1bd7f1a0-237c-49d6-aa5d-febf3fc40703', name="Имя 2", surname="Фамилия 2", position=CookPositions.COOK),
    Cook(id='dd533304-d994-4b96-b168-2538d134a85e', name="Имя 3", surname="Фамилия 3", position=CookPositions.CHIEF),
]


class CookRepo():
    def get_cook(self) -> list[Cook]:
        return cooks

    def get_cook_by_id(self, id: UUID) -> Cook:
        for cook in cooks:
            if cook.id == id:
                return cook
        return None
