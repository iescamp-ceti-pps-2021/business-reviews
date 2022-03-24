from app import db
from app.models.reviews import Review  # noqa:F401,E402
from app.models.utils.mixins import BaseModelMixin


class Business(BaseModelMixin, db.Model):
    __tablename__ = 'business'

    name = db.Column(db.String(50), nullable=False)
    address_street = db.Column(db.String(100))
    address_city = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    reviews = db.relationship('Review', backref='business', lazy='dynamic')

    def __str__(self):
        return f"<Business {self.name}>"
