from beavy.models.object import Object
from beavy.models.activity import Activity
from beavy.schemas.object import ObjectField, Schema, fields
from flask_security.core import current_user
from sqlalchemy.sql import and_


class CommentObject(Object):
    __mapper_args__ = {
        'polymorphic_identity': 'comment'
    }

    @property
    def text(self):
        return '(EMPTY)'


class CommentActivity(Activity):
    __mapper_args__ = {
        'polymorphic_identity': 'activity'
    }


class CommentSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    owner_id = fields.Integer()
    text = fields.String()
    belongs_to_id = fields.Integer()


def filter_comments_for_view(cls, method):
    if not current_user or current_user.is_anonymous():
        return
    return and_(cls.discriminator == 'comment',
                cls.owner_id == current_user.id)

Object.__access_filters['view'].append(filter_comments_for_view)

ObjectField.registry['comment'] = CommentSchema

