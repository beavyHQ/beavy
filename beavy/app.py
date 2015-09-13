from flask import Flask, session, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.marshmallow import Marshmallow
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.security import Security, SQLAlchemyUserDatastore

from flask_social_blueprint.core import SocialBlueprint as SocialBp
from flask.ext.babel import Babel

from flask_environments import Environments

from .utils import load_modules

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# The app
app = Flask(__name__)

# environment-based configuration loading
env = Environments(app, var_name="BEAVY_ENV")

env.from_yaml(os.path.join(BASE_DIR, 'config.yml'))
env.from_yaml(os.path.join(os.getcwd(), 'config.yml'))

if env.env == 'DEVELOPMENT':
    env.from_yaml(os.path.join(os.getcwd(), 'dev_config.yml'))

# update social buttons
_FLBLPRE = "flask_social_blueprint.providers.{}"
if not "SOCIAL_BLUEPRINT" in app.config:
    app.config["SOCIAL_BLUEPRINT"] = dict([
        ("." in name and name or _FLBLPRE.format(name), values)
        for name, values in app.config.get("SOCIAL_LOGINS").items()])


# start database
db = SQLAlchemy(app)
# and database migrations
migrate = Migrate(app, db)

# initialize Resource-Based API-System
ma = Marshmallow(app)

# scripts manager
manager = Manager(app)
# add DB+migrations commands
manager.add_command('db', MigrateCommand)

# initialize i18n
babel = Babel(app)


from beavy.models.user import User
from beavy.models.role import Role
from beavy.models.social_connection import SocialConnection

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class SocialBlueprint(SocialBp):
    def login_failed_redirect(self, profile, provider):
        if not app.config.get("SECURITY_REGISTERABLE"):
            return redirect("/")

        session["_social_profile"] = profile.data
        # keep the stuff around, so we can set it up after
        # the user provided us with a nice email address
        return redirect(url_for('security.register',
                name="{} {}".format(profile.data.get("first_name"),
                                    profile.data.get("last_name"))))


# add social authentication
SocialBlueprint.init_bp(app, SocialConnection, url_prefix="/_social")



load_modules(app)
