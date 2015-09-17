from marshmallow import Schema, fields
from beavy.common.morphing_field import MorphingField


class BaseObject(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    owner_id = fields.Integer()
    belongs_to_id = fields.Integer()  # don't leak
    klass = fields.String(attribute="discriminator")


class ObjectField(MorphingField):
    FALLBACK = BaseObject
    registry = {}
