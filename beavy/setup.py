from .app import app, mail, celery, security
from .schemas.user import CurrentUser
from flask_security import current_user
from .utils import load_modules

#  LOAD all external modules
load_modules(app)


# inject current_user in the template
@app.context_processor
def inject_user():
    if current_user.is_anonymous():
        return dict(SERIALIZED_USER='false')
    return dict(SERIALIZED_USER=CurrentUser().dumps(current_user).data)


# defer emails send by security
# to do so via celery
@celery.task
def send_security_email(msg):
    mail.send(msg)


@security.send_mail_task
def delay_security_email(msg):
    send_security_email.delay(msg)

