from mixer.backend.flask import mixer
from flask.ext.security.utils import encrypt_password
from datetime import datetime


def ensure_personas():
    return {
        'malcolm': mixer.blend('beavy.models.user.User',
                               name="Malcolm Reynolds",
                               password=encrypt_password('password'),
                               active=True,
                               confirmed_at=datetime.now()),
        'zoe':  mixer.blend('beavy.models.user.User',
                            name="Zoe Washburne",
                            password=encrypt_password('password'),
                            active=True,
                            confirmed_at=datetime.now()),
        'inara':  mixer.blend('beavy.models.user.User',
                              name="Inara Serra",
                              password=encrypt_password('password'),
                              active=True,
                              confirmed_at=datetime.now())
    }
