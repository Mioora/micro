from app.models.order import Order, OrderStatuses
from logging import getLogger

from uuid import UUID

orders: list[Order] = []

class OrderRepo:
    def get_orders(self) -> list[Order]:
        return orders

    def get_order_by_id(self, order_id: UUID) -> Order:
        for order in orders:
            if order.id == order_id:
                return order
        return None

    def create_order(self, new_order: Order) -> Order:
        for order in orders:
            if order.id == new_order.id:
                raise KeyError
        orders.append(new_order)
        return new_order
    
    def get_active_orders(self) -> list[Order]:
        active_orders = []
        for order in orders:
            if order.status == OrderStatuses.ACTIVATED:
                active_orders.append(order)
        return active_orders

    def set_status(self, new_order: Order) -> Order:
        for order in orders:
            if order.id == new_order.id:
                order.status = new_order.status
                break
        return new_order
    
    def set_finish_time(self, new_order: Order) -> Order:
        for order in orders:
            if order.id == new_order.id:
                order.finish_date = new_order.finish_date
                break
        return new_order

    def set_cook(self, new_order: Order) -> Order:
        for order in orders:
            if order.id == new_order.id:
                order.cook = new_order.cook
                break
        return new_order
