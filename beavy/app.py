from flask import Flask
from flask_environments import Environments

import os

app = Flask(__name__)
env = Environments(app, var_name="BEAVY_ENV", default_env="PRODUCTION")

env.from_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml'))
env.from_yaml(os.path.join(os.getcwd(), 'config.yml'))

