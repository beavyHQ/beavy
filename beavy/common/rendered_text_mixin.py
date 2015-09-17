from .payload_property import PayloadProperty


class RenderedTextMixin(object):
    # to be used on activity or object models

    raw = PayloadProperty('raw', 'text')
    chopped = PayloadProperty('chopped', 'text')
    cooked = PayloadProperty('cooked', 'text')
