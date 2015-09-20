
from marshmallow_jsonapi.fields import HyperlinkRelated
from marshmallow_jsonapi.utils import get_value_or_raise


class IncludingHyperlinkRelated(HyperlinkRelated):

    def __init__(self, nestedObj, *args,  **kwargs):
        if callable(nestedObj):
            nestedObj = nestedObj(many=False)
        self.nestedObj = nestedObj
        super(IncludingHyperlinkRelated, self).__init__(*args, **kwargs)

    def add_resource_linkage(self, value):
        if self.many:
            included_data = [
                {'type': self.type_,
                 'id': get_value_or_raise(self.id_field, each),
                 'attributes': self._extract_attributes(each)}
                for each in value]
        else:
            included_data = {
                'type': self.type_,
                'id': get_value_or_raise(self.id_field, value),
                'attributes': self._extract_attributes(value)}
        return included_data

    def _extract_attributes(self, value):
        sub = self.nestedObj.dump(value).data
        try:
            return sub["data"]["attributes"]
        except (KeyError, TypeError):
            # we are a classic type
            pass
        return sub
