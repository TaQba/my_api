from flask_restful import abort
from core.models.order import Order as Model

# Controller class - do operation on model , data manipulations

class Order:
    @staticmethod
    def get(order_id):
        orderModel = Model()
        order = orderModel.get_by_id(order_id)
        if not order:
            abort(
                404,
                message="Order with id: " + str(order_id) + " not found."
            )

        return order

    @staticmethod
    def post(data):
        try:
            order = Model()
            # @todo  user_id should be taken form model user by token
            order.user_id = 1
            order.vehicle_manufacturer = data['vehicle_manufacturer']
            order.model = data['model']
            order.price = data['price']
            order.currency = data['currency']
            order.save()
            return order.id
        except Exception as e:
            abort(
                400,
                message=str(e)
            )

    @staticmethod
    def put(order_id, data):
        order = Model.query.filter_by(id=order_id).first()
        if not order:
            abort(
                404,
                message="Order with id: " + str(order_id) + " not found."
            )

        try:
            order.vehicle_manufacturer = data['vehicle_manufacturer']
            order.model = data['model']
            order.price = data['price']
            order.currency = data['currency']
            order.save()
        except Exception as e:
            abort(
                400,
                message=str(e)
            )
        return True
