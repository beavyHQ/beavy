from flask import Blueprint

user_bp = Blueprint('users', 'beavy.users')
account_bp = Blueprint('account', 'beavy.account')
object_bp = Blueprint('object', 'beavy.object')
activity_bp = Blueprint('activity', 'beavy.activity')
lists_bp = Blueprint('lists', 'beavy.lists')

# Deprecated – Legacy support
users = user_bp
account = account_bp
obj = object_bp
activity = activity_bp


def setup(app):
    app.register_blueprint(user_bp,
                           url_prefix=app.config.get('USERS_URL', '/u'))
    app.register_blueprint(account_bp,
                           url_prefix=app.config.get('ACCOUNT_URL',
                                                     '/account'))
    app.register_blueprint(object_bp,
                           url_prefix=app.config.get('OBJECT_URL', '/o'))
    app.register_blueprint(activity_bp,
                           url_prefix=app.config.get('ACTIVITY_URL', '/a'))
    app.register_blueprint(lists_bp,
                           url_prefix='/')
