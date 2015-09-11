
from beavy.app import db
from beavy.models.activity import Activity
from beavy.models.object import Object


class Like(Activity):
    pass


Object.likes_count = db.Column(db.Integer)
