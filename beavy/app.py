from flask import Flask
from flask_environments import Environments

from .utils import load_modules

import os

app = Flask(__name__)
env = Environments(app, var_name="BEAVY_ENV")

env.from_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml'))
env.from_yaml(os.path.join(os.getcwd(), 'config.yml'))

load_modules(app)
