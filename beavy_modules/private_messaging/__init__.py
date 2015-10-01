from beavy.app import admin, db
from beavy.common.admin_model_view import AdminPolyModelView
from wtforms.fields import StringField
from .models import PrivateMessage
from .views import *

class PrivateMessageAdminView(AdminPolyModelView):
    column_list = ['created_at', 'title', 'participants']
    form_columns = ['created_at', 'title', 'participants']
    form_extra_fields = {'title': StringField()}


def init_app(app):
    admin.add_view(PrivateMessageAdminView(PrivateMessage, db.session,
                                      name="PrivateMessage",
                                      menu_icon_type='glyph',
                                      menu_icon_value='glyphicon-envelope'))