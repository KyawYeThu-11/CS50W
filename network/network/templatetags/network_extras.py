from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    one_unit = value.split(delimiter)[0]
    if one_unit.startswith('0'):
        return 'Just Now'
    else:
        return f'{one_unit}'
upto.is_safe = True