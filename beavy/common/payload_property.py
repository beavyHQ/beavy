from sqlalchemy.orm.attributes import flag_modified as sa_flag_modified


class PayloadProperty(object):

    def __init__(self, key, path=[], attribute='payload', force=True):
        self.key = key
        self.attribute = attribute
        self.force = force
        self.path = isinstance(path, str) and path.split('.') or path
        self.flag_modified = sa_flag_modified

    def _findBase(self, obj):
        base = getattr(obj, self.attribute)
        if base is None and self.force:
            base = {}
            setattr(obj, self.attribute, base)
            self.flag_modified(obj, self.attribute)

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

                self.flag_modified(obj, self.attribute)
                break

        return base

    def __get__(self, obj, _):
        if not obj:
            # someone asked on the class
            return self
        base = self._findBase(obj)
        key = self.key

        return base.get(key, None)

    def __set__(self, obj, value):
        self._findBase(obj)[self.key] = value
        self.flag_modified(obj, self.attribute)

    def __delete__(self, obj):
        raise NotImplemented()
