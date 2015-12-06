from functools import wraps

def rate_limit(default, *args, **kwargs):
    from beavy.app import limiter, app
    def inner(fn):
        key = "{}.{}".format(fn.__module__, fn.__name__)
        return limiter.limit(app.config.get("RATELIMITS", {}).get(key, default), *args, **kwargs)(fn)
    return inner
