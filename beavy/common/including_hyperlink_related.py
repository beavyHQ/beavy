
from marshmallow_jsonapi.fields import HyperlinkRelated
from marshmallow_jsonapi.utils import get_value_or_raise


class IncludingHyperlinkRelated(HyperlinkRelated):

    def __init__(self, nestedObj, *args,  **kwargs):
        if callable(nestedObj):
            nestedObj = nestedObj(many=False)
        self.nestedObj = nestedObj
        kwargs['type_'] = " "
        kwargs['include_data'] = True
        super(IncludingHyperlinkRelated, self).__init__(*args, **kwargs)

    def add_resource_linkage(self, value):
        def render(item):
            attributes = self._extract_attributes(item)
            type_ = attributes.pop('type', self.type_)
            return {'type': type_,
                    'id': get_value_or_raise(self.id_field, item),
                    'attributes': attributes}
        if self.many:
            included_data = [render(each) for each in value]
        else:
            included_data = render(value)
        return included_data

    def _extract_attributes(self, value):
        sub = self.nestedObj.dump(value).data
        try:
            return sub["data"]["attributes"]
        except (KeyError, TypeError):
            # we are a classic type
            pass
        return sub
