from beavy.common.paging_schema import makePaginationSchema
from beavy.schemas.object import ObjectField, Schema, fields
from beavy.schemas.user import BaseUser

from .models import PM_ID


class PrivateMessageSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    title = fields.String()
    klass = fields.String(attribute="discriminator")

    participants = fields.Nested(BaseUser)

pm_paged = makePaginationSchema(PrivateMessageSchema)()

ObjectField.registry[PM_ID] = PrivateMessageSchema
