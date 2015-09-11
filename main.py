from beavy.utils import fallbackRender
from beavy.app import app

@app.route("/")
@fallbackRender('home.html')
def hello():
    return {"title": "home"}
