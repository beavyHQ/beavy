from flask import Flask, session, url_for, redirect, json, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.marshmallow import Marshmallow
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.security import Security, SQLAlchemyUserDatastore, current_user
from flask.ext.security.utils import encrypt_password
from flask.ext.cache import Cache
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr
from flask_admin import Admin, AdminIndexView

from flask_social_blueprint.core import SocialBlueprint as SocialBp
from beavy.utils.deepmerge import deepmerge

from flask_environments import Environments
from pprint import pprint

from celery import Celery

import os
import yaml


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, '..', 'assets')

# The app
app = Flask(__name__,
            static_url_path='/assets',
            static_folder=STATIC_FOLDER)


# --------- helpers for setup ----------------------------


def make_env(app):
    # environment-based configuration loading
    env = Environments(app, var_name="BEAVY_ENV")

    env.from_yaml(os.path.join(BASE_DIR, 'config.yml'))
    # env.from_yaml(os.path.join(os.getcwd(), 'config.yml'))
    with open(os.path.join(os.getcwd(), 'config.yml'), "r") as r:
        deepmerge(app.config, yaml.load(r))

    # allow for environment variables to update items
    if os.environ.get("BEAVY_CONFIG_FROM_ENV", False):
        app.config.update(os.environ)

        if "DATABASE_URL" in os.environ:
            app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
        if "RABBITMQ_URL" in os.environ:
            app.config["CELERY_BROKER_URL"] = os.environ["RABBITMQ_URL"]
        if "REDIS_URL" in os.environ:
            app.config["RATELIMIT_STORAGE_URL"] = os.environ["REDIS_URL"]
            app.config["CACHE_REDIS_URL"] = os.environ["REDIS_URL"]

    # update social buttons
    _FLBLPRE = "flask_social_blueprint.providers.{}"
    if "SOCIAL_BLUEPRINT" not in app.config:
        app.config["SOCIAL_BLUEPRINT"] = dict([
            ("." in name and name or _FLBLPRE.format(name), values)
            for name, values in app.config.get("SOCIAL_LOGINS").items()])

    return env


def setup_statics(app):
    files = dict(main_js="main.js", main_css="main.css")
    if not app.debug:
        with open(os.path.join(STATIC_FOLDER, "manifest.json")) as r:
            manifest = json.load(r)

        files = dict([(key.replace(".", "_"), value)
                     for (key, value) in manifest.items()])

    @app.context_processor
    def injnect_manifest():
        return dict(static_files=files)


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


class BeavyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False


def _limiter_key():
    if current_user.is_authenticated:
        return "u_{}".format(current_user.id)
    return "ip_{}".format(get_ipaddr())
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

# initialize email support
mail = Mail(app)

# limit access to the app
limiter = Limiter(app, key_func=_limiter_key)
# configure logging for limiter
for handler in app.logger.handlers:
    limiter.logger.addHandler(handler)

# add caching support
cache = Cache(app)

#  -------------- initialize i18n --------------
from flask.ext.icu import ICU, get_messages
icu = ICU(app, app.config.get("DEFAULT_LANGUAGE"))


# Inject ICU messages for delivery to client via _preload.html template
@app.context_processor
def inject_messages():
    return dict(MESSAGES=json.dumps(get_messages()))


@icu.localeselector
def get_locale():
    locale = None
    if current_user is not None and current_user.is_authenticated:
        locale = current_user.language_preference
    elif app.config.get("LANGUAGES") is not None:
        languages = app.config.get("LANGUAGES")
        locale = request.accept_languages.best_match(languages)
    return locale  # If no locale, Flask-ICU uses the default setting.


#  ------ Database setup is done after here ----------
from beavy.models.user import User
from beavy.models.role import Role
from beavy.models.social_connection import SocialConnection

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# add social authentication
SocialBlueprint.init_bp(app, SocialConnection, url_prefix="/_social")

# initialize admin backend
admin = Admin(app,
              '{} Admin'.format(app.config.get("NAME")),
              index_view=BeavyAdminIndexView(),
              # base_template='my_master.html',
              template_mode='bootstrap3',)


from beavy.common.admin_model_view import AdminModelView
# setup admin UI stuff
admin.add_view(AdminModelView(User, db.session,
                              name="Users",
                              menu_icon_type='glyph',
                              menu_icon_value='glyphicon-user'))


#  ----- finally, load all configured modules ---------
from .setup import replaceHomeEndpoint, generate_capability_maps

# set up static files loading using the manifest in production
setup_statics(app)

# and set the home endpoint
replaceHomeEndpoint(app)

from .models.object import Object
generate_capability_maps(Object)

from .models.activity import Activity
generate_capability_maps(Activity)

# ----- some debug features

if app.debug:

    @app.before_first_request
    def ensure_users():
        from datetime import datetime
        admin_role = user_datastore.find_or_create_role('admin')
        pw = encrypt_password("password")

        if not user_datastore.find_user(email="user@example.org"):
            user_datastore.create_user(email="user@example.org",
                                       confirmed_at=datetime.now(),
                                       active=True,
                                       password=pw)

        if not user_datastore.find_user(email="admin@example.org"):
            user_datastore.add_role_to_user(
                user_datastore.create_user(email="admin@example.org",
                                           confirmed_at=datetime.now(),
                                           active=True,
                                           password=pw),
                admin_role)

        user_datastore.commit()

    @app.before_first_request
    def print_routes():
        pprint(["{} -> {}".format(rule.rule, rule.endpoint)
                for rule in app.url_map.iter_rules()
                if rule.endpoint != 'static'])
