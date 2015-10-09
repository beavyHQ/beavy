from flask import request, abort
from beavy.app import db, current_user
from beavy.utils import fallbackRender
from flask.ext.security import login_required

from .blueprint import hn_bp
from .models import Topic, Link


@hn_bp.route("/submit/", methods=["GET", "POST"])
@fallbackRender('hacker_news/submit.html')
@login_required
def submit_story():
    if request.method == "POST":
        params = request.get_json()
        title, url = params['title'].strip(), params['url'].strip()
        text = params['text'].strip()
        if not title:
            return abort(400, "You have to provide a 'title'");

        if url:
            link = Link(title=title, url=url, owner_id=current_user.id)
            db.session.add(link)
            db.session.commit()
            return {}
        elif text:
            topic = Topic(title=title, text=text, owner_id=current_user.id)
            db.session.add(topic)
            db.session.commit()
            return {}

        return abort(400, "You have to provide either 'url' or 'text', too")

    return {}
