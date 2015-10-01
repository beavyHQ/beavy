from beavy.app import admin, db
from beavy.common.admin_model_view import AdminModelView
from .models import PrivateMessage
from .views import *


def init_app(app):
    admin.add_view(AdminModelView(PrivateMessage, db.session,
                                  name="PrivateMessage",
                                  menu_icon_type='glyph',
                                  menu_icon_value='glyphicon-envelope'))