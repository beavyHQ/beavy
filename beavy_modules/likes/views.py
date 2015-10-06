from beavy.utils import fallbackRender, as_page, get_or_create, api_only
from flask.ext.security import login_required, current_user
from sqlalchemy.orm import contains_eager, aliased
from beavy.blueprints import (users as users_bp,
                              obj as objects_bp,
                              account as account_bp)

from beavy.models.object import Object
from .models import Like
from .schemas import user_likes_paged

from beavy.app import db


def _load_likes(user):
    cur_like = aliased(Like)
    return as_page(Object.query
                         .by_capability(Object.Capabilities.listed,
                                        Object.Capabilities.listed_for_activity)
                         .with_my_activities()
                         .join(Like, Like.object_id == Object.id)
                         .filter(Like.subject_id == user.id)
                         .add_entity(Like))

    # return user_likes_paged.dump(as_page(
    #     Like.query
    #         .filter(Like.subject_id == user.id)
    #         .filter_visible(Like.object_id, Object.id)
    #         .join(Like.object),
    #     error_out=False))


@users_bp.route("/<user:user>/likes/")
@fallbackRender('user_likes.html')
def user_likes(user):
    return _load_likes(user)


@account_bp.route("/likes/")
@login_required
@fallbackRender('user_likes.html')
def user_likes():
    return _load_likes(current_user)


@objects_bp.route("/<model:obj>/has_liked", methods=["GET"])
@login_required
@api_only
def liked_object(obj):
    return {"liked": Like.query
                         .filter(Like.subject_id == current_user.id)
                         .filter(Like.object_id == obj.id).count() > 0}


@objects_bp.route("/<model:obj>/like", methods=["POST"])
@login_required
@api_only
def like_object(obj):
    like, created = get_or_create(db.session, Like,
                                  subject_id=current_user.id,
                                  object_id=obj.id)
    if created:
        db.session.commit()
    return {"liked": True}


@objects_bp.route("/<model:obj>/unlike", methods=["POST"])
@login_required
@api_only
def unlike_object(obj):
    db.session.delete(Like.query.filter_by(subject_id=current_user.id,
                                           object_id=obj.id))
    db.session.commit()
    return {"liked": False}

