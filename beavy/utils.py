from werkzeug.exceptions import UnsupportedMediaType, NotAcceptable
from werkzeug.wrappers import Response as ResponseBase
from flask import request, render_template, Response, jsonify
from functools import wraps

import importlib


def load_modules(app):
    for modl in app.config.get("MODULES", []):
        # load module
        subm = importlib.import_module("beavy_modules.{}".format(modl))
        # call init on module if found
        if hasattr(subm, "init_app"):
            print(subm, subm.init_app)
            subm.init_app(app)


def fallbackRender(template, nativeTypes=('application/json', )):
    nativeTypes = set(nativeTypes)

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            resp = fn(*args, **kwargs)
            if isinstance(resp, ResponseBase):
                return resp

            accepted = set(request.accept_mimetypes.values())
            if len(accepted & nativeTypes):
                # we've found one, return json
                return Response(jsonify(resp),
                                200, content_type='application/json')

            return Response(render_template(template, data=resp),
                            200, content_type="text/html")
        return decorated_view
    return wrapper


def as_page(query, per_page=30, **kwargs):
    page = 1
    try:
        page = int(request.args.get("page") or 1)
    except (KeyError, ValueError):
        pass

    if page <= 0:
        page = 1

    return query.paginate(page, per_page, **kwargs)
