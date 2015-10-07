from flask import request
from beavy.utils import fallbackRender
from flask.ext.security import login_required

from .blueprint import hn_bp
from .models import Topic, Link


@hn_bp.route("/submit/", methods=["GET", "POST"])
@fallbackRender('hacker_news/submit.html')
@login_required
def submit_story():
    if request.method == "POST":
        print(request.params)
    return {}
