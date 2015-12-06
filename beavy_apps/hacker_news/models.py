from beavy.models.object import Object
from beavy.common.rendered_text_mixin import RenderedTextMixin
from beavy.common.payload_property import PayloadProperty

# from slugify import slugify_url

TOPIC_ID = "topic"
LINK_ID = "link"


class Topic(Object, RenderedTextMixin):
    __mapper_args__ = {
        'polymorphic_identity': TOPIC_ID
    }

    title = PayloadProperty('title')
    text = PayloadProperty('text')

    CAPABILITIES = [Object.Capabilities.listed, Object.Capabilities.searchable]


class Link(Object):
    __mapper_args__ = {
        'polymorphic_identity': LINK_ID
    }

    title = PayloadProperty('title')
    url = PayloadProperty('url')

    CAPABILITIES = [Object.Capabilities.listed, Object.Capabilities.searchable]
