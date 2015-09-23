from beavy.common.paging_schema import makePaginationSchema
from beavy.schemas.object import ObjectField
# , Schema, fields
from beavy.common.including_hyperlink_related import IncludingHyperlinkRelated
from marshmallow_jsonapi import Schema, fields
from beavy.schemas.user import BaseUser

from .models import PM_ID


class PrivateMessageSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    title = fields.String()
    type = fields.String(attribute="discriminator")


    class Meta:
        type_ = 'private_message'  # Required

    participants = IncludingHyperlinkRelated(BaseUser,
        '/users/{user_id}',
        url_kwargs={'user_id': '<id>'},
        many=True, include_data=True,
        type_='user'
    )


pm = PrivateMessageSchema()
pm_paged = makePaginationSchema(PrivateMessageSchema)()

ObjectField.registry[PM_ID] = PrivateMessageSchema
