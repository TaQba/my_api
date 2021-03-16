from flask_restful import Resource
from flask_jwt import jwt_required
from core.controllers.ping import Ping as Controller


class Ping(Resource):
    @jwt_required()
    def get(self, ping_id=None):
        ping = Controller()
        return ping.get(ping_id)

    @jwt_required()
    def delete(self, ping_id):
        ping = Controller()
        return ping.delete(ping_id)
