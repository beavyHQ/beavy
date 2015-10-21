
from mixer.backend.flask import mixer
from flask.ext.security.utils import encrypt_password
from datetime import datetime


def ensure_personas():
    return {
        'admin': mixer.blend('beavy.models.user.User',
                             password=encrypt_password('password'),
                             active=True,
                             confirmed_at=datetime.now()),
        'ben':  mixer.blend('beavy.models.user.User',
                            password=encrypt_password('password'),
                            active=True,
                            confirmed_at=datetime.now(),
                            name="ben"),
        'anouk':  mixer.blend('beavy.models.user.User',
                              password=encrypt_password('password'),
                              active=True,
                              confirmed_at=datetime.now(),
                              name="anouk")
    }
