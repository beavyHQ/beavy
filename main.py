from flask.ext.security import login_required
from beavy.utils import fallbackRender
from beavy.app import app

@app.route("/private")
@login_required
@fallbackRender('home.html')
def private():
    return {"title": "home"}
