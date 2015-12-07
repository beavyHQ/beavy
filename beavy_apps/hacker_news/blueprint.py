from flask import Blueprint

hn_bp = Blueprint('hacker_news', __name__,
                  template_folder='templates')
