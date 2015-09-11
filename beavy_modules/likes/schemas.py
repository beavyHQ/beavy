from beavy.common.paging_schema import makePaginationSchema
from beavy.schemas.user import BaseUser
from beavy.schemas.object import ObjectField
from marshmallow import Schema, fields


class BaseLike(Schema):
    subject = fields.Nested(BaseUser)
    created_at = fields.DateTime()


class UserLike(Schema):
    created_at = fields.DateTime()
    object = ObjectField()


user_likes_paged = makePaginationSchema(UserLike)()
