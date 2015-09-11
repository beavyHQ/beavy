from beavy.app import db
from beavy.models.activity import Activity
from beavy.models.object import Object


class Like(Activity):
    __mapper_args__ = {
        'polymorphic_identity': 'like'
    }


Object.likes_count = db.Column(db.Integer)
