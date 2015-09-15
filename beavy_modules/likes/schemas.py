from beavy.common.paging_schema import makePaginationSchema
from beavy.schemas.user import BaseUser
from beavy.schemas.activity import ActivityField
from beavy.schemas.object import ObjectField, BaseObject
from beavy.app import app
from marshmallow import Schema, fields


class BaseLike(Schema):
    subject = fields.Nested(BaseUser)
    created_at = fields.DateTime()

ActivityField.registry['Like'] = BaseLike

# Patching the base class to include likes_count
# internal marshmallow things...
BaseObject._declared_fields['likes_count'] = fields.Integer(default=0)

# FIXME: there must be a nicer way to manage this integration
if 'comments' in app.config.get("MODULES"):
    from beavy_modules.comments.models import CommentSchema
    CommentSchema._declared_fields['likes_count'] = fields.Integer(default=0)


class UserLike(Schema):
    created_at = fields.DateTime()
    object_id = fields.Integer()
    object = ObjectField()


user_likes_paged = makePaginationSchema(UserLike)(many=False)
