import random
from datetime import datetime

from flask import Response
from flask_login import UserMixin

from app import argon2, cache, db, lm
from app.models.reviews import Review  # noqa:F401,E402
from app.models.utils.mixins import BaseModelMixin


class User(UserMixin, BaseModelMixin, db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(300), nullable=False)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    date_last_visited = db.Column(db.DateTime(), default=datetime.utcnow)
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    is_admin = db.Column(db.Boolean, default=False)

    @staticmethod
    def hash_password(password):
        return argon2.generate_password_hash(password)

    def verify_password(self, password):
        return argon2.check_password_hash(self.password_hash, password)

    def update_password(self, password):
        self.hash_password = User.hash_password(password)
        User.update(self)

    def avatar(self):
        import hashlib

        import requests

        digest = hashlib.sha1(self.email.lower().encode("utf-8")).hexdigest()
        variants = ["normal", "stagger", "spider", "flower", "gem"]
        variant = random.choice(variants)

        # return f"http://localhost:3000/blockie/{digest}"
        # return f"http://localhost:3000/identicon/{digest}"

        avatar = cache.get(str(self.id))
        if avatar is None:
            # r = requests.get(f"https://hashvatar.vercel.app/{digest}/{variant}")
            r = requests.get(f"http://localhost:3000/sha256avatar/{digest}?v={variant}")
            avatar = r.text.replace("\"", "'")
            cache.set(str(self.id), avatar)
        else:
            avatar = avatar.decode("utf-8")
        return f"data:image/svg+xml;charset=utf-8,{avatar}"

    def __repr__(self):
        return f"<User {self.username}>"


@lm.user_loader
def load_user(user_id):
    return User.retrive_by_id(user_id)
