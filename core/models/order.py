from core import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import text
from core.components.helper import Helper


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey(
            "user.id",
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        nullable=False,
        primary_key=True
    )
    vehicle_manufacturer = db.Column(db.String(16), nullable=False, unique=True)
    model = db.Column(db.String(16), nullable=False)
    price = db.Column(INTEGER())
    currency = db.Column(db.String(3), nullable=False)
    created = db.Column(
        db.DateTime,
        server_default=text('CURRENT_TIMESTAMP')
    )
    updated = db.Column(
        db.DateTime,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    def serialize(self):
        return {
            'id': self.id,
            'vehicle_manufacturer': self.vehicle_manufacturer,
            'model': self.model,
            'price': self.price,
            'currency': self.currency,
            'created': Helper.date_format(self.created),
            'updated': Helper.date_format(self.updated)
        }

    def get_by_id(self, order_id):

        results = self.query.filter(self.__class__.id == order_id).first()
        if results is None:
            return None
        return results.serialize()

    def save_and_get_id(self):
        self.save()
        db.session.refresh(self)
        return self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
