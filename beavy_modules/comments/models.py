from beavy.models.object import Object
from flask_security.core import current_user
from sqlalchemy.sql import and_
from beavy.common.rendered_text_mixin import RenderedTextMixin
from beavy.app import db

COMMENT_ID = "comment"


class CommentObject(Object, RenderedTextMixin):
    __mapper_args__ = {
        'polymorphic_identity': COMMENT_ID
    }

    CAPABILITIES = [Object.Capabilities.listed_for_activity]

    in_reply_to_id = db.Column(db.Integer, db.ForeignKey("objects.id"),
                               nullable=True)
    # in_reply_to = db.relationship(Object, backref=db.backref('replies'))


def filter_comments_for_view(cls, method):
    if not current_user or current_user.is_anonymous():
        return
    return and_(cls.discriminator == COMMENT_ID,
                cls.owner_id == current_user.id)

Object.__access_filters['view'].append(filter_comments_for_view)
