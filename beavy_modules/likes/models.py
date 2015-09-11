
from beavy.app import db
from beavy.models import User, Object

import datetime


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime())
    user = db.relationship(User)


Object.likes_count = db.Column(db.Integer)