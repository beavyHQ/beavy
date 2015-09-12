from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy.sql import or_


class AccessQuery(BaseQuery):

    def _filter_for(self, class_, fltr):
        return class_.query.filter(or_(
                    *[x for x in filter(lambda x: x is not None, [
                        t(class_, fltr)
                        # weirdly class_.__access_filters fails on us
                        # probably some sqlalchemy magic
                        for t in getattr(class_, "__access_filters")[fltr]
                    ])]))

    def filter_visible(self, attr, remoteAttr):
        return self.filter(attr.in_(
            self._filter_for(remoteAttr.class_, 'view')
                .with_entities(remoteAttr)
                .subquery()
            )
        )
