from flask import Flask, session, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.marshmallow import Marshmallow
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail

from flask_social_blueprint.core import SocialBlueprint as SocialBp
from flask.ext.babel import Babel

from flask_environments import Environments

from celery import Celery

from .utils import load_modules

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# The app
app = Flask(__name__)


# --------- helpers for setup ----------------------------


def make_env(app):
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

    return env


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def setup_security_bg_mail(app, security, mail):

    @celery.task
    def send_security_email(msg):
        mail.send(msg)

    @security.send_mail_task
    def delay_security_email(msg):
        send_security_email.delay(msg)


class SocialBlueprint(SocialBp):
    # our own wrapper around the SocialBlueprint
    # to forward for registring
    def login_failed_redirect(self, profile, provider):
        if not app.config.get("SECURITY_REGISTERABLE"):
            return redirect("/")

        session["_social_profile"] = profile.data
        # keep the stuff around, so we can set it up after
        # the user provided us with a nice email address
        return redirect(url_for('security.register',
                        name="{} {}".format(profile.data.get("first_name"),
                                            profile.data.get("last_name"))))


# --------------------------- Setting stuff up in order ----------


# load the environment and configuration
env = make_env(app)

# initialize the celery task queue
celery = make_celery(app)

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

# initialize email support
mail = Mail(app)

#  ------ Database setup is done after here ----------
from beavy.models.user import User
from beavy.models.role import Role
from beavy.models.social_connection import SocialConnection

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# defer emails to be send in teh background
setup_security_bg_mail(app, security, mail)

# add social authentication
SocialBlueprint.init_bp(app, SocialConnection, url_prefix="/_social")


#  ----- finally, load all configured modules ---------
load_modules(app)
