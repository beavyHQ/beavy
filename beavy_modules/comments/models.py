from beavy.models.object import Object
from beavy.models.activity import Activity
from flask_security.core import current_user
from sqlalchemy.sql import and_


class CommentObject(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'comment'
    }


class CommentActivity(Activity):
    __mapper_args__ = {
        'polymorphic_identity': 'activity'
    }


def filter_comments_for_view(cls, method):
    if not current_user or current_user.is_anonymous():
        return
    return and_(cls.discriminator == 'comment',
                cls.owner_id == current_user.id)

Object.__access_filters['view'].append(filter_comments_for_view)
