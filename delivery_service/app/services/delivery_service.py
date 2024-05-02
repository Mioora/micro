from app.repositories.local_delivery_repo import DeliveryRepo
from app.repositories.local_deliveryman_repo import DeliverymanRepo
from app.request.request_module import get_address
from app.models.Delivery import Delivery, DeliveryStatuses
from app.models.Deliveryman import Deliveryman
from logging import Logger, getLogger
from app.logger.logger_settings import LoggerSetup
from app.settings import settings
from uuid import UUID, uuid4
from datetime import datetime

logger_setup = LoggerSetup()

class DeliveryService:
    delivery_repo: DeliveryRepo
    deliveryman_repo: DeliverymanRepo
    logger: Logger

    def __init__(self) -> None:
        self.logger = getLogger(__name__)
        self.delivery_repo = DeliveryRepo()
        self.deliveryman_repo = DeliverymanRepo()

    def get_delivery(self) -> list[dict]:
        self.logger.info("GETTED DELIVERIES")
        output = []
        for delivery in self.delivery_repo.get_delivery():
            if delivery is not None:
                data = {}
                data['id'] = delivery.id
                data['order_id'] = delivery.order_id
                data['status'] = delivery.status
                data['deliveryman'] = delivery.deliveryman
                data['address'] = delivery.address
                data['start_time'] = delivery.start_time
                data['end_time'] = delivery.end_time
                output.append(data)
        return output
    
    def get_delivery_by_id(self, delivery_id) -> dict:
        for delivery in self.delivery_repo.get_delivery():
            if delivery.id == delivery_id:
                self.logger.info("GETTED DELIVERY")
                return delivery
        raise KeyError

    def get_deliveryman(self, ) -> list[Deliveryman]:
        self.logger.info('GET ALL DELIVERYMAN')
        return self.deliveryman_repo.get_deliveryman()

    def get_free_deliveryman(self) -> UUID:
        deliveryman = self.deliveryman_repo.get_deliveryman()
        deliveries = self.delivery_repo.get_delivery()
        for delivery in deliveries:
            if delivery.deliveryman in deliveryman:
                deliveryman.remove(delivery.deliveryman)
        if len(deliveryman) != 0:
            self.logger.info("GET FREE DELIVERYMAN")
            return deliveryman[0].id
        else:
            self.logger.warning("ALL DELIVERYMANS IS BUSY")
            raise ValueError

    def create_delivery(self, order_id, delivery_id = None) -> Delivery:
        if delivery_id == None:
            delivery_id = uuid4()
        if self.delivery_repo.get_delivery_by_order_id(order_id) != None:
            self.logger.warning("TRY TO CREATE EXISTED DELIVERY")
            raise ValueError
        delivery = Delivery(
            id=delivery_id,
            order_id=order_id,
            status=DeliveryStatuses.CREATED,
            deliveryman=None,
            address=get_address(order_id),
            start_time=datetime.now()
        )
        self.logger.info("CREATED DELIVERY")
        return self.delivery_repo.create_delivery(delivery)


    def activate_delivery(self, delivery_id) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(delivery_id)
        if delivery == None:
            self.logger.warning("TRY TO GET NOT EXISTED DELIVERY")
            raise KeyError
        delivery = self.delivery_repo.get_delivery_by_id(delivery_id)
        if delivery.status != DeliveryStatuses.CREATED:
            self.logger.warning("TRY TO ACTIVATE NOT CREAETED DELIVERY")
            raise ValueError
        deliveryman_id = self.get_free_deliveryman()
        delivery.status = DeliveryStatuses.ACTIVE
        delivery.deliveryman = self.deliveryman_repo.get_deliveryman_by_id(deliveryman_id)
        self.delivery_repo.set_deliveryman(delivery)
        self.logger.info("ACTIVATE DELIVERY")
        return self.delivery_repo.set_status(delivery)

    def finish_delivery(self, delivery_id) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(delivery_id)
        if delivery == None:
            self.logger.warning("TRY TO GET NOT EXISTED DELIVERY")
            raise KeyError
        if delivery.status != DeliveryStatuses.ACTIVE:
            self.logger.warning("TRY TO FINISH NOT ACTIVATED DELIVERY")
            raise ValueError
        delivery.status = DeliveryStatuses.DONE
        delivery.end_time = datetime.now()
        self.logger.info("FINISH DELIVERY")
        return self.delivery_repo.set_status(delivery)
    
    


