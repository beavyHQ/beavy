from sqlalchemy.dialects.postgresql import JSONB
from beavy.common.access_query import AccessQuery

from .user import User
from beavy.app import db
from collections import defaultdict


class Object(db.Model):
    """
    This is the primary base class for all kind of objects
    we know of inside the system
    """
    __tablename__ = "objects"
    query_class = AccessQuery

    id = db.Column(db.Integer, primary_key=True)
    discriminator = db.Column('type', db.String(100))
    created_at = db.Column('created_at', db.DateTime())
    payload = db.Column('payload', JSONB)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    owner = db.relationship(User, backref=db.backref('objects'))
    belongs_to = db.Column(db.Integer, db.ForeignKey("objects.id"),
                           nullable=True)
    # children = db.relationship("Object", backref=db.backref('belongs_to',
                                                            # remote_side=id))

    __mapper_args__ = {'polymorphic_on': discriminator}

Object.__access_filters = defaultdict(list)
