class MorphingSchema():

    def dump(self, obj):
        return self._get_serializer(obj).dump(obj)

    def _obj_to_name(self, obj):
        return obj.__mapper__.polymorphic_identity

    def _get_serializer(self, obj):
        name = self._obj_to_name(obj)
        return self.registry.get(name, self.FALLBACK)()
