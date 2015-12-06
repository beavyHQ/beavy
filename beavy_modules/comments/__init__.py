from beavy.app import admin, db
from beavy.common.admin_model_view import AdminPolyModelView
from .models import CommentObject
from .views import *   # noqa


def init_app(app):
    admin.add_view(AdminPolyModelView(CommentObject, db.session,
                                      name="Comments",
                                      menu_icon_type='glyph',
                                      menu_icon_value='glyphicon-comment'))
