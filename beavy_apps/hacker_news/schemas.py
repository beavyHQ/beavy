from beavy.common.paging_schema import makePaginationSchema
from beavy.schemas.object import ObjectField
# , Schema, fields
from beavy.common.including_hyperlink_related import IncludingHyperlinkRelated
from marshmallow_jsonapi import Schema, fields
from beavy.schemas.user import BaseUser

from .models import TOPIC_ID, LINK_ID


class TopicSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    owner_id = fields.Integer()
    type = fields.String(attribute="discriminator")
    title = fields.String(attribute='title')
    slug = fields.String(attribute='slug')
    text = fields.String(attribute='cooked')

    class Meta:
        type_ = TOPIC_ID  # Required

    author = IncludingHyperlinkRelated(BaseUser,
                                       '/users/{user_id}',
                                       url_kwargs={'user_id': '<owner_id>'},
                                       many=False, include_data=True,
                                       type_='user')

topic = TopicSchema()
topic_paged = makePaginationSchema(TopicSchema)()

ObjectField.registry[TOPIC_ID] = TopicSchema


class LinkSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    owner_id = fields.Integer()
    type = fields.String(attribute="discriminator")
    title = fields.String(attribute='title')
    slug = fields.String(attribute='slug')
    url = fields.String(attribute='url')

    class Meta:
        type_ = LINK_ID  # Required

    author = IncludingHyperlinkRelated(BaseUser,
                                       '/users/{user_id}',
                                       url_kwargs={'user_id': '<owner_id>'},
                                       many=False, include_data=True,
                                       type_='user')


link = LinkSchema()
link_paged = makePaginationSchema(LinkSchema)()

ObjectField.registry[LINK_ID] = LinkSchema
