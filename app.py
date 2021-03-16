from core import app, db
from flask_restful import Api
from core.routers.ping import Ping
from core.routers.user import User
from core.routers.health_check import HealthCheck
from flask_jwt import JWT, jwt_required, current_identity
import core.models as models


# JWT Auth
def authenticate(username, password):
    user = db.session.query(models.user.User). \
        filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return user


def identity(payload):
    user_id = payload['identity']
    return db.session.query(models.user.User).filter_by(id=user_id).first()


JWT(app, authenticate, identity)

# endpoints
api = Api(app)
api.add_resource(
    Ping,
    '/pings',
    '/pings/<int:ping_id>'
)

api.add_resource(
    User,
    '/users',
    '/users/<int:user_id>'
)

api.add_resource(HealthCheck, '/', '/health-check')


if __name__ == '__main__':
    app.run(host='127.0.0.1')
