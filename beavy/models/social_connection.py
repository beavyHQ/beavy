from flask_babel import gettext as _
from sqlalchemy import orm
from ..app import db, app
from .user import User

import logging
import datetime


class SocialConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = orm.relationship(User, foreign_keys=user_id,
                            backref=orm.backref('connections', order_by=id))
    provider = db.Column(db.String(255))
    profile_id = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    cn = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))

    def get_user(self):
        return self.user

    @classmethod
    def by_profile(cls, profile):
        provider = profile.data["provider"]
        return cls.query.filter(cls.provider == provider, cls.profile_id == profile.id).first()

    @classmethod
    def from_profile(cls, user, profile):
        if not user or user.is_anonymous():
            if not app.config.get("SECURITY_REGISTERABLE"):
                msg = "User not found. Registration disabled."
                logging.warning(msg)
                raise Exception(_(msg))
            email = profile.data.get("email")
            if not email:
                msg = "Please provide an email address."
                logging.warning(msg)
                raise Exception(_(msg))
            conflict = User.query.filter(User.email == email).first()
            if conflict:
                msg = "Email {} is already used. Login and then connect external profile."
                msg = _(msg).format(email)
                logging.warning(msg)
                raise Exception(msg)

            now = datetime.now()
            user = User(
                email=email,
                name="{} {}".format(profile.data.get("first_name"),
                                    profile.data.get("last_name")),
                confirmed_at=now,
                active=True)

            db.session.add(user)
            db.session.flush()

        assert user.id, "User does not have an id"
        connection = cls(user_id=user.id, **profile.data)
        db.session.add(connection)
        db.session.commit()
        return connection