from app.models.Delivery import Delivery

from uuid import UUID

deliveries: list[Delivery] = []


class DeliveryRepo:
    def get_delivery(self) -> list[Delivery]:
        return deliveries

    def get_delivery_by_id(self, id: UUID) -> Delivery:
        for delivery in deliveries:
            if delivery.id == id:
                return delivery
        return None
    
    def get_delivery_by_order_id(self, order_id: UUID) -> Delivery:
        for delivery in deliveries:
            if delivery.order_id == order_id:
                return delivery
        return None

    def create_delivery(self, new_delivery: Delivery) -> Delivery:
        for delivery in deliveries:
            if delivery.id == new_delivery.id:
                raise KeyError
        deliveries.append(new_delivery)
        return new_delivery

    def set_status(self, new_delivery: Delivery) -> Delivery:
        for delivery in deliveries:
            if delivery.id == new_delivery.id:
                delivery.status = new_delivery.status
                break
        return new_delivery

    def set_deliveryman(self, new_delivery: Delivery) -> Delivery:
        for delivery in deliveries:
            if delivery.id == new_delivery.id:
                delivery.deliveryman = new_delivery.deliveryman
                break
        return new_delivery
