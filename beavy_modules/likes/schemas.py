from beavy.common.paging_schema import makePaginationSchema
from beavy.common.including_hyperlink_related import IncludingHyperlinkRelated
from beavy.schemas.user import BaseUser
from beavy.schemas.activity import ActivityField
from beavy.schemas.object import ObjectField
# from marshmallow import Schema, fields

from marshmallow_jsonapi import Schema, fields


# class BaseLike(Schema):
#     subject = fields.Nested(BaseUser)
#     created_at = fields.DateTime()

# ActivityField.registry['like'] = BaseLike


class UserLike(Schema):
    created_at = fields.DateTime()

    class Meta:
        type_ = "like"

    object = IncludingHyperlinkRelated(ObjectField(),
        '/o/{object_id}',
        url_kwargs={'object_id': '<id>'},
        many=False, include_data=True,
        type_='object'
    )



user_likes_paged = makePaginationSchema(UserLike)(many=False)
