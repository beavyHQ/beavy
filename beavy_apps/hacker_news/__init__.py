from beavy.common.admin_model_view import AdminPolyModelView
from beavy.app import admin, db

from .models import Link, Topic
from .blueprint import hn_bp
from .models import *
from .views import *


def init_app(app):

    app.register_blueprint(hn_bp)
    admin.add_view(AdminPolyModelView(Link, db.session,
                                      name="Links",
                                      menu_icon_type='glyph',
                                      menu_icon_value='glyphicon-resize-full'))
    admin.add_view(AdminPolyModelView(Topic, db.session,
                                      name="Topics",
                                      menu_icon_type='glyph',
                                      menu_icon_value='glyphicon-file'))