from flask import Blueprint
from beavy.schemas.object import ObjectField, fields

blueprint = Blueprint('likes', __name__,
                      template_folder='templates')

from .views import *


def init_app(app):
    # patch all objects to have likes_counts when serialized
    for cls in ObjectField.registry.values():
        cls._declared_fields['likes_count'] = fields.Integer(default=0)

    # tell flask about our own templates
    app.register_blueprint(blueprint)
