from werkzeug.wrappers import Response as ResponseBase
from flask import request, render_template, make_response, json, abort
from logging import getLogger
from marshmallow import MarshalResult

from functools import wraps

import importlib


API_MIMETYPES = set((
                    'application/json',
                    'application/vnd.api+json'
                    ))


def load_modules_and_app(app):
    logger = getLogger("beavy.loadModules")
    loaders = []
    for modl in app.config.get("MODULES", []):
        # load module
        logger.debug("Importing Module {}".format(modl))
        subm = importlib.import_module("beavy_modules.{}".format(modl))
        # defer call init on module if found
        if hasattr(subm, "init_app"):
            loaders.append((modl, subm.init_app))

    # Load the app
    app_modl = app.config.get('APP')
    logger.debug("Importing APP {}".format(app_modl))
    app_subm = importlib.import_module("beavy_apps.{}".format(app_modl))

    for (modl, init_app) in loaders:
        logger.debug("Init Module {}".format(modl))
        init_app(app)

    # call init on app if found
    if hasattr(app_subm, "init_app"):
        app_subm.init_app(app)


def api_only(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        accepted = set(request.accept_mimetypes.values())
        if not (accepted & API_MIMETYPES) and not request.args.get("json"):
            return abort(415, "Unsupported Media Type")

        resp = fn(*args, **kwargs)
        if not isinstance(resp, ResponseBase):
            data, code, headers = unpack(resp)
            # we've found one, return json
            if isinstance(data, MarshalResult):
                data = data.data
            resp = make_response(json.dumps(data), code)

            if headers:
                resp.headers.update(headers)
            resp.headers["Content-Type"] = 'application/json'
        return resp
    return wrapped


def fallbackRender(template, key=None):

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            resp = fn(*args, **kwargs)
            if isinstance(resp, ResponseBase):
                return resp

            data, code, headers = unpack(resp)

            accepted = set(request.accept_mimetypes.values())
            if len(accepted & API_MIMETYPES) or request.args.get("json"):
                # we've found one, return json
                if isinstance(data, MarshalResult):
                    data = data.data
                resp = make_response(json.dumps(data), code)
                ct = 'application/json'
            else:
                resp = make_response(render_template(template,
                                                     key=key,
                                                     data=data),
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


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


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
