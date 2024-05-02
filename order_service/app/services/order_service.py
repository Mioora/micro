from app.repositories.bd_order_repo import OrderRepo
from app.repositories.local_order_repo import OrderRepo as LocalOrderRepo
from app.repositories.local_cook_repo import CookRepo
from app.models.order import Order, OrderStatuses
from app.models.cook import Cook
from logging import Logger, getLogger
from app.logger.logger_settings import LoggerSetup
from app.settings import settings
from app.rabbitmq import send_queue_msg
from uuid import UUID, uuid4
from datetime import datetime

if (not settings.for_test):
    logger_setup = LoggerSetup()


class OrderService:
    logger: Logger
    cook_repo: CookRepo
    order_repo: OrderRepo

    def __init__(self) -> None:
        self.logger = getLogger(__name__)
        if settings.for_test is None:
            self.order_repo = LocalOrderRepo()
        else:
            self.order_repo = OrderRepo()
        self.cook_repo = CookRepo()

    def get_orders(self) -> list[dict]:
        self.logger.info("GET ORDERS")
        output = []
        for i in self.order_repo.get_orders():
            if i is not None:
                data = i.dict()
                output.append(data)
        return output

    def get_order(self, order_id) -> dict:
        self.logger.info("GET ORDER")
        return self.order_repo.get_order_by_id(order_id).dict()

    def get_cook(self) -> list[Cook]:
        self.logger.info("GET COOK")
        return self.cook_repo.get_cook()

    def create_order(self, address=None, order_id=None) -> Order:
        self.logger.info("CREATE ORDER")
        if order_id == None:
            order_id = uuid4()
        order = Order(
            id=order_id,
            date=datetime.now(),
            finish_date=None,
            status=OrderStatuses.CREATED,
            cook=None,
            address=address
        )
        return self.order_repo.create_order(order)

    def activate_order(self, order_id) -> Order:
        order = self.order_repo.get_order_by_id(order_id)
        if order == None:
            self.logger.warning("TRY TO ACTIVATE NOT EXISTED ORDER")
            raise KeyError
        if order.status != OrderStatuses.CREATED:
            self.logger.warning("TRY TO ACTIVATE NOT CREATED ORDER")
            raise ValueError
        cook_id = self.get_free_cook()
        if cook_id is None:
            self.logger.warning("FREE COOKS COUNT == 0")
            raise ValueError
        order.status = OrderStatuses.ACTIVATED
        order.cook = self.cook_repo.get_cook_by_id(cook_id)
        self.order_repo.set_cook(order)
        self.logger.info("ACTIVATED ORDER")
        return self.order_repo.set_status(order)

    def get_free_cook(self) -> UUID:
        cooks = self.cook_repo.get_cook().copy()
        orders = self.order_repo.get_active_orders()
        for order in orders:
            if order.cook in cooks:
                cooks.remove(order.cook)
        if len(cooks) != 0:
            return cooks[0].id
        return None

    def finish_order(self, order_id) -> Order:
        order = self.order_repo.get_order_by_id(order_id)
        if order == None:
            self.logger.warning("TRY TO FINISH NOT EXISTED ORDER")
            raise KeyError
        if order.status != OrderStatuses.ACTIVATED:
            self.logger.warning("TRY TO FINISH NOT ACTIVATED ORDER")
            raise ValueError
        order.status = OrderStatuses.DONE
        order.finish_date = datetime.now()
        if order.address != None:
            self.logger.info("ORDER SEND TO DELIVERY SERVICE")
            if (settings.for_test is not None):
                send_queue_msg(order.id)
        self.order_repo.set_finish_time(order)
        self.logger.info("FINISH ORDER")
        return self.order_repo.set_status(order)

    def cancel_order(self, order_id) -> Order:
        order = self.order_repo.get_order_by_id(order_id)
        if order == None:
            self.logger.warning("TRY TO CANCEL NOT EXISTED ORDER")
            raise KeyError
        if order.status == OrderStatuses.DONE:
            self.logger.warning("TRY TO CANCEL COMPLETED ORDER")
            raise ValueError
        order.status = OrderStatuses.CANCELED
        self.logger.info("ORDER CANCELED")
        return self.order_repo.set_status(order)
    