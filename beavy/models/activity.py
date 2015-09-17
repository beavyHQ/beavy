from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func
from beavy.common.access_query import AccessQuery
from collections import defaultdict
from beavy.app import db

from .user import User


class Activity(db.Model):
    """
    We record activities on objects through this
    """
    __tablename__ = "activities"
    query_class = AccessQuery

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    discriminator = db.Column('verb', db.String(100), nullable=False)
    created_at = db.Column('created_at', db.DateTime(), nullable=False,
                           server_default=func.now())
    object_id = db.Column(db.Integer, db.ForeignKey("objects.id"),
                          nullable=True)
    whom_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    payload = db.Column('payload', JSONB, nullable=True)

    __mapper_args__ = {'polymorphic_on': discriminator}

    subject = db.relationship(User, backref=db.backref("activities"),
                              foreign_keys=subject_id)
    object = db.relationship('Object', backref=db.backref("activities"))


Activity.__access_filters = defaultdict(list)
