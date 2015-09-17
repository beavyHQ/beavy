from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func
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
