from beavy.models.object import Object
from beavy.models.object import User
from flask_security.core import current_user
from sqlalchemy.sql import and_

from beavy.app import db

PM_ID = "private_message"


# Define models
PMParticipants = db.Table('{}_participants'.format(PM_ID),
                          db.Column('user_id',
                                    db.Integer(),
                                    db.ForeignKey(User.id),
                                    nullable=False),
                          db.Column('pm_id',
                                    db.Integer(),
                                    db.ForeignKey("objects.id"),
                                    nullable=False))


class PrivateMessage(Object):
    __mapper_args__ = {
        'polymorphic_identity': PM_ID
    }

    title = db.Column(db.String(255), nullable=False)

    participants = db.relationship('User', secondary=PMParticipants,
                                   backref=db.backref('{}s'.format(PM_ID),
                                                      lazy='dynamic'))


# def filter_private_messages_for_view(cls, method):
#     if not current_user or current_user.is_anonymous():
#         return
#     return and_(cls.discriminator == PM_ID,
#                 cls.id.in_(current_user.private_messages))

# Object.__access_filters['view'].append(filter_private_messages_for_view)