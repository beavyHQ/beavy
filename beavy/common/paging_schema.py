from marshmallow import Schema, fields, post_dump


class BasePaging(Schema):
    has_next = fields.Boolean()
    has_prev = fields.Boolean()
    next_num = fields.Integer()
    prev_num = fields.Integer()
    page = fields.Integer()
    pages = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()

    @post_dump(pass_many=False)
    def move_to_meta(self, data):
        items = data.pop("items")
        # FIXME: add support for paging links
        return {
            "meta": data,
            "data": items.get("data", []),
            "links": items.get("links", [])
            }


def makePaginationSchema(itemsCls, field_cls=fields.Nested):
    return type("{}Paging".format(itemsCls.__class__.__name__),
                (BasePaging, ), dict(items=field_cls(itemsCls, many=True)))
