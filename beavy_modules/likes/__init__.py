from flask import Blueprint

blueprint = Blueprint('likes', __name__,
                      template_folder='templates')

from .views import *

def init_app(app):
    app.register_blueprint(blueprint)