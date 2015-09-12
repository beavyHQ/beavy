from werkzeug.wrappers import Response as ResponseBase
from flask import request, render_template, make_response, json
from marshmallow import MarshalResult

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

            data, code, headers = unpack(resp)

            accepted = set(request.accept_mimetypes.values())
            if len(accepted & nativeTypes) or request.args.get("json"):
                # we've found one, return json
                if isinstance(data, MarshalResult):
                    data = data.data
                resp = make_response(json.dumps(data), code)
                ct = 'application/json'
            else:
                resp = make_response(render_template(template, data=data),
                                     code)
                ct = "text/html"

            if headers:
                resp.headers.update(headers)
            resp.headers["Content-Type"] = ct
            return resp

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


# --- start of Flask-RESTful code ---
# Copyright (c) 2013, Twilio, Inc.
# All rights reserved.
# This code is part of Flask-RESTful and is governed by its
# license. Please see the LICENSE file in the root of this package.
def unpack(value):
    """Return a three tuple of data, code, and headers"""
    if not isinstance(value, tuple):
        return value, 200, {}

    try:
        data, code, headers = value
        return data, code, headers
    except ValueError:
        pass

    try:
        data, code = value
        if not isinstance(code, int):
            raise ValueError()
        return data, code, {}
    except ValueError:
        pass

    return value, 200, {}
