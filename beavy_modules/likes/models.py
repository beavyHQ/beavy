from beavy.app import db
from beavy.models.activity import Activity
from beavy.models.object import Object
from sqlalchemy import event


class Like(Activity):
    __mapper_args__ = {
        'polymorphic_identity': 'like'
    }


Object.likes_count = db.Column(db.Integer())


@event.listens_for(Like, 'after_insert')
def update_object_likes_count(mapper, connection, target):
    # unfortunately, we can't do an aggregate in update directly...
    likes_count = Like.query.filter(Like.object_id == target.object_id).count()
    Object.query.filter(Object.id == target.object_id
                        ).update({'likes_count': likes_count})
