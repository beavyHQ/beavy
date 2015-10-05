from marshmallow import Schema, fields
from beavy.common.morphing_schema import MorphingSchema

from .user import BaseUser


class BaseActivity(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    subject = fields.Nested(BaseUser)
    object_id = fields.Integer()  # don't leak


class ActivityField(MorphingSchema):
    FALLBACK = BaseActivity
    registry = {}
