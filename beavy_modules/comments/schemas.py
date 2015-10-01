from beavy.common.paging_schema import makePaginationSchema
from beavy.schemas.object import ObjectField
# , Schema, fields
from beavy.common.including_hyperlink_related import IncludingHyperlinkRelated
from marshmallow_jsonapi import Schema, fields
from beavy.schemas.user import BaseUser

from .models import COMMENT_ID


class CommentSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    owner_id = fields.Integer()
    type = fields.String(attribute="discriminator")
    text = fields.String(attribute='cooked')
    belongs_to_id = fields.Integer()
    in_reply_to_id = fields.Integer()

    class Meta:
        type_ = COMMENT_ID  # Required

    author = IncludingHyperlinkRelated(BaseUser,
        '/users/{user_id}',
        url_kwargs={'user_id': '<owner_id>'},
        many=False, include_data=True,
        type_='user'
    )


comment = CommentSchema()
comment_paged = makePaginationSchema(CommentSchema)()

ObjectField.registry[COMMENT_ID] = CommentSchema
