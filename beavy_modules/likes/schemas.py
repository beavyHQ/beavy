from beavy.common.paging_schema import makePaginationSchema
from beavy.schemas.user import BaseUser
from beavy.schemas.activity import ActivityField
from marshmallow import Schema, fields


class BaseLike(Schema):
    subject = fields.Nested(BaseUser)
    created_at = fields.DateTime()

ActivityField.registry['Like'] = BaseLike


class UserLike(Schema):
    created_at = fields.DateTime()
    object = ObjectField()


user_likes_paged = makePaginationSchema(UserLike)(many=False)
