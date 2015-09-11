from marshmallow import Schema, fields
from beavy.common.morphing_field import MorphingField

from .user import BaseUser


class BaseObject(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    owner = fields.Nested(BaseUser)
    belongs_to = fields.Integer()  # don't leak


class ObjectField(MorphingField):
    FALLBACK = BaseObject
    registry = {}
