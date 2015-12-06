from marshmallow import pre_dump


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
