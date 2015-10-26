from flask import request
from beavy.app import app
from .users import *

from .lists import *


if app.config.get("TESTING"):
    # we allow for a shutdown command in the test environment
    @app.route("/__TESTS__/shutdown")
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

        return 'Server shutting down...'
