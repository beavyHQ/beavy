# from sqlalchemy.orm import subqueryload

# from beavy.models.object import Object
from beavy.utils import fallbackRender, as_page
from beavy.blueprints import account as account_bp
from beavy.blueprints import users as users_bp
from flask.ext.security import login_required, current_user

from .models import CommentObject
from .schemas import comment_paged


def _load_threads(user):
    query = CommentObject.query.filter(CommentObject.owner_id == user.id)
# .filter_visible(CommentObject.)
    return comment_paged.dump(as_page(query, error_out=False)).data


@account_bp.route("/comments/")
@login_required
@fallbackRender('home.html', 'comments')
def account_comment():
    return _load_threads(current_user)


@users_bp.route("/<user:user>/comments/")
@fallbackRender('user_comments.html')
def user_comments(user):
    return _load_threads(user)
