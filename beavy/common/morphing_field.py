from marshmallow.fields import Field


class MorphingField(Field):

    # registry = {
    # }

    def __init__(self, many=False, fallback=None, overwrite=None, **metadata):
        self.many = False
        self.fallback = fallback or self.FALLBACK
        self.overwrite = overwrite

    # Common alternative:
    # def _obj_to_name(self, obj):
    #     return obj.__class__.__name__

    def _obj_to_name(self, obj):
        return obj.__mapper__.polymorphic_identity

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        if self.many:
            return [self._get_serializer(value).dump(x).data for x in value]
        return self._get_serializer(value).dump(value).data

    def _get_serializer(self, obj):
        name = self._obj_to_name(obj)
        if self.overwrite:
            kls = self.overwrite(obj, name)
            if isinstance(kls, str):
                name = kls
            elif callable(kls):
                return kls()

        return self.registry.get(name, self.fallback)()
