from beavy.app import db
from flask.ext.security import SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin

from sqlalchemy.dialects.postgresql import JSONB

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Object(db.Model):
    """
    This is the primary base class for all kind of objects
    we know of inside the system
    """
    __tablename__ = "objects"

    id = db.Column(db.Integer, primary_key=True)
    discriminator = db.Column('type', db.String(100))
    created_at = db.Column('created_at', db.DateTime())
    payload = db.Column('payload', JSONB)
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    belongs_to = db.Column(db.Integer, db.ForeignKey("objects.id"), nullable=True)
    children = db.relationship("Object", backref=db.backref('belongs_to',
                                                            remote_side=id))

    __mapper_args__ = {'polymorphic_on': discriminator}


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
