from datetime import datetime

from app import db
from app.models.utils.mixins import BaseModelMixin
from app.models.utils.types import GUID


class Review(BaseModelMixin, db.Model):
    __tablename__ = 'review'
    # __table_args__ = (db.UniqueConstraint('business_id', 'author_id', name='uc_reviews_business_user'),)

    business_id = db.Column(GUID(), db.ForeignKey('business.id'))
    author_id = db.Column(GUID(), db.ForeignKey('user.id'))
    rating = db.Column(db.Integer())
    review_text = db.Column(db.String(500))
    review_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __str__(self):
        return f"Review {self.business.name} {self.review_date.isoformat()}"
