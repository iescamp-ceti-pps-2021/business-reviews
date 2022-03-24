import uuid
from datetime import datetime

from app import db
from app.models.utils.types import GUID


class BaseModelMixin(object):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    # created_at = db.Column(db.DateTime, default=db.func.current_timestamp)
    # updated_at = db.Column(db.DateTime, default=db.func.current_timestamp, onupdate=db.func.current_timestamp)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def retrieve_all(cls):
        return cls.query.all()

    @classmethod
    def retrive_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def filter_all(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
