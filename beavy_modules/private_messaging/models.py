from beavy.models.object import Object
from beavy.models.object import User
from beavy.common.payload_property import PayloadProperty
from beavy.utils.url_converters import ModelConverter

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

    title = PayloadProperty('title')
    # db.Column(db.String(255), nullable=False)

    participants = db.relationship('User', secondary=PMParticipants,
                                   backref=db.backref('{}s'.format(PM_ID),
                                                      lazy='dynamic'))

ModelConverter.__OBJECTS__['private_message'] = PrivateMessage

# def filter_private_messages_for_view(cls, method):
#     if not current_user or current_user.is_anonymous:
#         return
#     return and_(cls.discriminator == PM_ID,
#                 cls.id.in_(current_user.private_messages))

# Object.__access_filters['view'].append(filter_private_messages_for_view)
