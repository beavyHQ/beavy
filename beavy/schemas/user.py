from marshmallow import Schema, fields


class BaseUser(Schema):
    id = fields.Function(lambda obj: obj.__LOOKUP_ATTRS__ and
                         getattr(obj, obj.__LOOKUP_ATTRS__[0])
                         or obj.id)
    beavyId = fields.Integer(attribute="id")
    name = fields.String()
    active = fields.Boolean()
    created_at = fields.DateTime()


class CurrentUser(BaseUser):
    pass
