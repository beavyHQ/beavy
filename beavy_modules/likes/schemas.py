from beavy.common.paging_schema import makePaginationSchema
from beavy.common.including_hyperlink_related import IncludingHyperlinkRelated
from beavy.schemas.object import ObjectField
# from marshmallow import Schema, fields

from marshmallow_jsonapi import Schema, fields
from marshmallow import pre_dump


# class BaseLike(Schema):
#     subject = fields.Nested(BaseUser)
#     created_at = fields.DateTime()

# ActivityField.registry['like'] = BaseLike


class UserLike(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()

    TUPLE_KEY = 'Like'
    REMAP_TUPLE_KEYS = ('Object', )

    class Meta:
        type_ = "like"

    @pre_dump
    def extract_items(self, item):
        if isinstance(item, tuple):
            tup = item
            item = getattr(item, self.TUPLE_KEY)
            for key in self.REMAP_TUPLE_KEYS:
                setattr(item, key.lower(), getattr(tup, key))

        return item

    object = IncludingHyperlinkRelated(ObjectField())


user_likes_paged = makePaginationSchema(UserLike)(many=False)
