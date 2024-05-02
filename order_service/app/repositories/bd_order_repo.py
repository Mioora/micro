import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order, OrderStatuses
from app.schemas.order import Order as DBOrder
from app.repositories.local_cook_repo import CookRepo


class OrderRepo():
    db: Session
    cook_repo: CookRepo

    def __init__(self) -> None:
        self.cook_repo = CookRepo()
        self.db = next(get_db())


    def _map_to_model(self, order: DBOrder) -> Order:
        result = Order.from_orm(order)
        if order.cook_id != None:
            result.cook = self.cook_repo.get_cook_by_id(order.cook_id)
        return result

    def _map_to_schema(self, order: Order) -> DBOrder:
        data = dict(order)
        del data['cook']
        data['cook_id'] = order.cook.id if order.cook != None else None
        result = DBOrder(**data)
        return result

    def get_orders(self) -> list[Order]:
        orders = []
        for order in self.db.query(DBOrder).all():
            temp = Order.from_orm(order)
            if order.cook_id is not None:
                temp.cook = self.cook_repo.get_cook_by_id(order.cook_id)
            orders.append(temp)
        return orders

    def get_active_orders(self) -> list[Order]:
        orders = []
        for order in self.db.query(DBOrder).filter(DBOrder.status == OrderStatuses.ACTIVATED):
            temp = Order.from_orm(order)
            if order.cook_id is not None:
                temp.cook = self.cook_repo.get_cook_by_id(order.cook_id)
            orders.append(temp)
            print(*temp)
        return orders

    def get_order_by_id(self, id: UUID) -> Order:
        order = self.db.query(DBOrder).filter(DBOrder.id == id).first()
        if order == None:
            raise KeyError

        return Order.from_orm(order)

    def create_order(self, order: Order) -> Order:
        try:
            db_order = self._map_to_schema(order)
            self.db.add(db_order)
            self.db.commit()
            return order
        except:
            traceback.print_exc()
            raise KeyError

    def set_finish_time(self, order: Order) -> Order:
        db_order: DBOrder = self.db.query(DBOrder).filter(
            DBOrder.id == order.id).first()
        db_order.finish_date = order.finish_date
        self.db.commit()
        return self._map_to_model(db_order)

    def set_status(self, order: Order) -> Order:
        db_order: DBOrder = self.db.query(DBOrder).filter(
            DBOrder.id == order.id).first()
        db_order.status = order.status
        self.db.commit()
        return self._map_to_model(db_order)

    def set_cook(self, order: Order) -> Order:
        db_order: DBOrder = self.db.query(DBOrder).filter(
            DBOrder.id == order.id).first()
        db_order.cook_id = order.cook.id
        self.db.commit()
        return self._map_to_model(db_order)