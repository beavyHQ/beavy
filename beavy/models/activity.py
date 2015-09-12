from sqlalchemy.dialects.postgresql import JSONB
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
    subject_id = db.Column(db.Integer, db.ForeignKey(User.id))
    subject = db.relationship(User, backref=db.backref("activities"),
                              foreign_keys=subject_id)
    discriminator = db.Column('verb', db.String(100))
    created_at = db.Column('created_at', db.DateTime())
    object_id = db.Column(db.Integer, db.ForeignKey("objects.id"),
                          nullable=True)
    object = db.relationship('Object', backref=db.backref("activities"))
    whom_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    payload = db.Column('payload', JSONB)

    __mapper_args__ = {'polymorphic_on': discriminator}


Activity.__access_filters = defaultdict(list)
