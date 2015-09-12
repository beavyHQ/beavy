from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy.sql import or_


class AccessQuery(BaseQuery):

    def _gen_filters(self, class_, fltr):
        return [x for x in filter(lambda x: x is not None, [
            t(class_, fltr)
            # weirdly class_.__access_filters fails on us
            # probably some sqlalchemy magic
            for t in getattr(class_, "__access_filters")[fltr]]
            )
        ]

    def filter_visible(self, attr, remoteAttr):
        filters = self._gen_filters(remoteAttr.class_, 'view')
        if not filters:
            return self.filter(False)

        return self.filter(attr.in_(
            remoteAttr.class_.query.filter(or_(*filters))
                             .with_entities(remoteAttr)
                             .subquery()
            )
        )
