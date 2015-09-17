from flask import Blueprint

users = Blueprint('users', 'beavy.users')
account = Blueprint('account', 'beavy.account')


def setup(app):
    app.register_blueprint(users, url_prefix=app.config.get('USERS_URL', '/u'))
    app.register_blueprint(account, url_prefix=app.config.get('ACCOUNT_URL', '/account'))
