from sqlalchemy.orm.attributes import flag_modified


class PayloadProperty(object):

    def __init__(self, key, path="", attribute='payload', force=True):
        self.key = key
        self.attribute = attribute
        self.force = force
        self.path = isinstance(path, str) and path.split('.') or path

    def _findBase(self, obj):
        base = getattr(obj, self.attribute)
        if base is None and self.force:
            base = {}
            setattr(obj, self.attribute, base)
            flag_modified(obj, self.attribute)

        items = self.path[:]
        while items:
            cur = items.pop(0)
            try:
                base = base[cur]
            except KeyError:
                base[cur] = {}
                base = base[cur]
                while items:
                    cur = items.pop(0)
                    base[cur] = {}
                    base = base[cur]

                flag_modified(obj, self.attribute)
                break

        return base

    def __get__(self, obj, _):
        base = self._findBase(obj)
        key = self.key

        return base.get(key, None)

    def __set__(self, obj, value):
        self._findBase(obj)[self.key] = value
        flag_modified(obj, self.attribute)

    def __delete__(self, obj):
        raise NotImplemented()
