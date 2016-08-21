from marshmallow import pre_dump, fields


class MorphingSchema():

    @pre_dump
    def select_processor(self, obj, many=False,
                         strict=False, update_fields=False):
        if many:
            return [self._get_serializer(item) for item in obj]
        return self._get_serializer(obj)

    def _obj_to_name(self, obj):
        return obj.__mapper__.polymorphic_identity

    def _get_serializer(self, obj):
        name = self._obj_to_name(obj)
        return self.registry.get(name, self.FALLBACK)()


class MorphingNested(fields.Nested, MorphingSchema):

    def _get_serializer(self, obj):
        name = self._obj_to_name(obj)
        rv = self.nested.registry.get(name, self.nested.FALLBACK)()
        return rv

    def _serialize(self, nested_obj, attr, obj):
        rv = [self._get_serializer(obj).dump(obj).data
              for obj in nested_obj]
        return rv
