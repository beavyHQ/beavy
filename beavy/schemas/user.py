# from marshmallow import Schema, fields
from marshmallow_jsonapi import Schema, fields


class BaseUser(Schema):
    class Meta:
        type_ = "user"

    id = fields.Function(lambda obj: obj.__LOOKUP_ATTRS__ and
                         getattr(obj, obj.__LOOKUP_ATTRS__[0])
                         or obj.id)
    beavyId = fields.Integer(attribute="id")
    name = fields.String()
    active = fields.Boolean()
    created_at = fields.DateTime()
    language_preference = fields.String()


class CurrentUser(BaseUser):
    pass


class UserProfile(BaseUser):
    pass
