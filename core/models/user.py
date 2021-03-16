from core import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(32),
        index=True,
        unique=True,
        nullable=False
    )
    password_hash = db.Column(db.String(128), nullable=False)
    created = db.Column(
        db.TIMESTAMP,
        server_default=db.text('CURRENT_TIMESTAMP'),
        nullable=False
    )
    updated = db.Column(
        db.TIMESTAMP,
        server_default=db.text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        ),
        nullable=False
    )

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        verify = pwd_context.verify(password, self.password_hash)
        return verify

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token, expiration=600):
        try:
            s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash
        }

    def __repr__(self):
        return "<User: {}>".format(self.name)
