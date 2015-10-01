from beavy.app import admin, db
from beavy.views.admin_model import AdminModelView
from .models import CommentObject
from .views import *


def init_app(app):
    admin.add_view(AdminModelView(CommentObject, db.session,
                                  name="Comments",
                                  menu_icon_type='glyph',
                                  menu_icon_value='glyphicon-comment'))