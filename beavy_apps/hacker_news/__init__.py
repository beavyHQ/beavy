
from .blueprint import hn_bp
from .models import *
from .views import *


def init_app(app):

    app.register_blueprint(hn_bp)
