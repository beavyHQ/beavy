from flask.ext.security import UserMixin
from flask_security.forms import ConfirmRegisterForm, RegisterForm, StringField
from sqlalchemy import func
from beavy.app import db

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id',
                                 db.Integer(),
                                 db.ForeignKey('user.id'),
                                 nullable=False),
                       db.Column('role_id',
                                 db.Integer(),
                                 db.ForeignKey('role.id'),
                                 nullable=False))


RegisterForm.name = StringField('Full Name')
ConfirmRegisterForm.name = StringField('Full Name')


class User(db.Model, UserMixin):
    __LOOKUP_ATTRS__ = []
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column('created_at', db.DateTime(), nullable=False,
                           server_default=func.now())
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer())
    language_preference = db.Column(db.String(2))

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return "<User #{} '{}' ({})>".format(self.id,
                                             self.name or "",
                                             self.email)
