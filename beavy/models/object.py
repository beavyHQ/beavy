from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import contains_eager, aliased
from enum import Enum, unique
from sqlalchemy import func
from flask.ext.security import current_user
from beavy.common.access_query import AccessQuery
from itertools import chain
from flask import abort

from .user import User
from beavy.app import db
from collections import defaultdict


class ObjectQuery(AccessQuery):

    def by_capability(self, *caps, aborting=True, abort_code=404):
        caps = set(chain.from_iterable(map(lambda c:
                                            getattr(Object.TypesForCapability,
                                                getattr(c, 'value', c), []),
                                            caps)))
        if not caps:
            # No types found, break right here.
            if aborting:
                raise abort(abort_code)
            return self.filter("1=0")

        return self.filter(Object.discriminator.in_(caps))

    def with_my_activities(self):
        if not current_user or not current_user.is_authenticated():
            return self

        from .activity import Activity

        my_activities = aliased(Activity)

        return self.outerjoin(my_activities
                  ).filter(my_activities.subject_id == current_user.id
                  ).options(contains_eager(Object.my_activities,
                                           alias=my_activities))


class Object(db.Model):
    """
    This is the primary base class for all kind of objects
    we know of inside the system
    """
    @unique
    class Capabilities(Enum):
        # This type is to be shown in default lists
        # like 'top', 'latest' etc
        listed = 'listed'

        # If the type isn't listed but has `listed_for_activity`
        # it can show up in lists about activitys, for example
        # when an object got liked
        listed_for_activity = 'a_listable'

        # This can be searched for
        searchable = 'searchable'


    __tablename__ = "objects"
    query_class = ObjectQuery

    id = db.Column(db.Integer, primary_key=True)
    discriminator = db.Column('type', db.String(100), nullable=False)
    created_at = db.Column('created_at', db.DateTime(), nullable=False,
                           server_default=func.now())
    payload = db.Column('payload', JSONB, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    belongs_to = db.Column(db.Integer, db.ForeignKey("objects.id"),
                           nullable=True)
    # children = db.relationship("Object", backref=db.backref('belongs_to',
                                                            # remote_side=id))

    __mapper_args__ = {'polymorphic_on': discriminator}

    owner = db.relationship(User, backref=db.backref('objects'))


Object.__access_filters = defaultdict(list)
