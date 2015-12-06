from beavy.utils import fallbackRender, as_page
from beavy.blueprints import account as account_bp
from flask_security import login_required, current_user
from flask import abort

from .schemas import pm_paged, pm


@account_bp.route("/private_messages/")
@login_required
@fallbackRender('home.html', 'private_messages')
def private_messages():
    return pm_paged.dump(as_page(current_user.private_messages,
                                 error_out=False)).data


@account_bp.route("/private_messages/<model(private_message):message>/")
@login_required
@fallbackRender('home.html', 'private_message')
def private_message(message):
    if current_user not in message.participants:
        return abort(403)
    return pm.dump(message).data
