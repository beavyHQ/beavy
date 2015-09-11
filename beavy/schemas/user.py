from marshmallow import Schema, fields


class BaseUser(Schema):
    id = fields.Integer()
    name = fields.String()
    active = fields.Boolean()
    created_at = fields.DateTime()
