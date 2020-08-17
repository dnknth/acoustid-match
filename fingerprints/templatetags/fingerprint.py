from django import template
from json import dumps


register = template.Library()


@register.filter
def json(obj):
    "Format a Python object as JSON"
    return dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
