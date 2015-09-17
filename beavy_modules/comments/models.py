from beavy.models.object import Object
from beavy.models.activity import Activity
from beavy.schemas.object import ObjectField, Schema, fields
from flask_security.core import current_user
from sqlalchemy.sql import and_
from beavy.common.rendered_text_mixin import RenderedTextMixin


class CommentObject(Object, RenderedTextMixin):
    __mapper_args__ = {
        'polymorphic_identity': 'comment'
    }


class CommentActivity(Activity):
    __mapper_args__ = {
        'polymorphic_identity': 'activity'
    }


class CommentSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    owner_id = fields.Integer()
    text = fields.String(attribute='cooked')
    belongs_to_id = fields.Integer()
    klass = fields.String(attribute="discriminator")


def filter_comments_for_view(cls, method):
    if not current_user or current_user.is_anonymous():
        return
    return and_(cls.discriminator == 'comment',
                cls.owner_id == current_user.id)

Object.__access_filters['view'].append(filter_comments_for_view)

ObjectField.registry['comment'] = CommentSchema

