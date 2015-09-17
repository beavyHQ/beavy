from beavy.utils import fallbackRender, as_page
from beavy.blueprints import account as account_bp
from flask_security import login_required, current_user

from .schemas import pm_paged


@account_bp.route("/private_messages/")
@login_required
@fallbackRender('home.html')
def private_messages():
    print("IN")
    return pm_paged.dump(as_page(current_user.private_messages, error_out=False))
