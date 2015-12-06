from .blueprint import blueprint
from .views import *     # noqa


def init_app(app):
    app.register_blueprint(blueprint,
                           url_prefix=app.config.get('URL_EXTRACTOR_URL', '/'))
