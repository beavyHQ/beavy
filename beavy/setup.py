from .app import app, mail, celery, security
from .utils import load_modules_and_app, url_converters, fallbackRender
from .schemas.user import CurrentUser
from collections import namedtuple

from flask_security import current_user

app.url_map.converters['model'] = url_converters.ModelConverter
app.url_map.converters['user'] = url_converters.UserConverter

# LOAD all external modules
load_modules_and_app(app)

# then load our views:
from beavy import views     # noqa

# allows them to register on blueprints before we do that setup


# register blueprints
from .blueprints import setup as register_blueprints
register_blueprints(app)


# inject current_user in the template
@app.context_processor
def inject_user():
    if current_user.is_anonymous:
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


# ---- generate object capabilities
def generate_capability_maps(obj):
    capabilities_map = dict((x.value, []) for x in obj.Capabilities)
    for typ, kls in obj.__mapper__.polymorphic_map.items():
        if hasattr(kls.class_, 'CAPABILITIES'):
            for cap in kls.class_.CAPABILITIES:
                cap = getattr(cap, "value", cap)
                capabilities_map.setdefault(cap, []).append(typ)

    caps = namedtuple('Cababilities', capabilities_map.keys())
    obj.TypesForCapability = caps(**capabilities_map)


def replaceHomeEndpoint(app):
    HOME_URL = app.config["URLS"]["HOME"]
    original_endpoint = None
    for rule in app.url_map.iter_rules():
        if HOME_URL == rule.rule:
            original_endpoint = rule.endpoint
            rule.rule = "/"
            rule.compile()
            break

    if original_endpoint:
        app.url_map.add(
            app.url_rule_class(HOME_URL, alias=True,
                               endpoint=original_endpoint))


# default home, blank.

@app.route("/hello")
@fallbackRender('home.html')
def hello():
    return {"title": "home"}
