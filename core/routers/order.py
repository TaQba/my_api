from flask import Flask, jsonify, g, url_for
from flask_restful import Resource, request
from flask_expects_json import expects_json
from flask_jwt import jwt_required
from flask_restful import Resource, request
from core.controllers.order import Order as Controller


# Route class - do basic validation and redirect to controller

class Order(Resource):
    @jwt_required()
    def get(self, id):
        return Controller.get(id)

    @expects_json(
        {
            'type': 'object',
            'properties': {
                'vehicle_manufacturer': {'type': 'string'},
                'model': {'type': 'string'},
                'price': {
                    "type": "number",
                    "minimum": 100
                },
                'currency': {'type': 'string', 'pattern': "^(GBP|EUR|USD)$"}
            },
            'required': [
                'vehicle_manufacturer',
                'model',
                'price',
                'currency'
            ]
        },
        fill_defaults=True
    )
    @jwt_required()
    def post(self):
        return Controller.post(g.data)

    @expects_json(
        {
            'type': 'object',
            'properties': {
                'vehicle_manufacturer': {'type': 'string'},
                'model': {'type': 'string'},
                'price': {
                    "type": "number",
                    "minimum": 100
                },
                'currency': {'type': 'string', 'pattern': "^(GBP|EUR|USD)$"}
            },
            'required': [
                'vehicle_manufacturer',
                'model',
                'price',
                'currency'
            ]
        },
        fill_defaults=True
    )
    @jwt_required()
    def put(self, id):
        return Controller.put(id, g.data)
