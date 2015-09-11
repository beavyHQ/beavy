from beavy.utils import fallbackRender, as_page
from beavy_modules.likes import blueprint

from .models import Like
from .schemas import user_likes_paged


@blueprint.route("/users/<int:user_id>/likes")
@fallbackRender('user_likes.html')
def user_likes(user_id):
    return user_likes_paged.dump(as_page(
        Like.query.filter(Like.subject == user_id),
        error_out=False))
