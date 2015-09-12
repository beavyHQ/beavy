from beavy.utils import fallbackRender, as_page
from beavy_modules.likes import blueprint
from sqlalchemy.orm import subqueryload

from beavy.models.object import Object
from .models import Like
from .schemas import user_likes_paged


@blueprint.route("/u/<int:user_id>/likes")
@fallbackRender('user_likes.html')
def user_likes(user_id):
    print(user_id)
    return user_likes_paged.dump(as_page(
        Like.query
            .filter(Like.subject_id == user_id)
            .filter_visible(Like.object_id, Object.id)
            .options(subqueryload(Like.object)),
        error_out=False))
