from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext import migrate as ext_migrate
from flask.ext.marshmallow import Marshmallow
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

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


from beavy.models.user import User
from beavy.models.role import Role

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

load_modules(app)
