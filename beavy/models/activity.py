from beavy.app import db
from sqlalchemy.dialects.postgresql import JSONB

from .user import User

class Activity(db.Model):
    """
    We record activities on objects through this
    """
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Integer, db.ForeignKey(User.id))
    discriminator = db.Column('verb', db.String(100))
    created_at = db.Column('created_at', db.DateTime())
    object = db.Column(db.Integer, db.ForeignKey("objects.id"), nullable=True)
    whom = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    payload = db.Column('payload', JSONB)

    __mapper_args__ = {'polymorphic_on': discriminator}
