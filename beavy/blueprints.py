from flask import Blueprint

users = Blueprint('users', 'beavy.users')


def setup(app):
    app.register_blueprint(users, url_prefix=app.config.get('USERS_URL', '/u'))
