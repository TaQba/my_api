from flask_restful import Resource, request
from flask_jwt import jwt_required
from core.controllers.user import User as Controller


class User(Resource):
    @jwt_required()
    def get(self, user_id):
        return Controller.get(user_id)

    @jwt_required()
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        return Controller.post(username, password)
