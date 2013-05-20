from django import template
import iptools
register = template.Library()

@register.filter(name='long2ip')
def long2ip(value):
    """Converts a long value to dotted IP address String""
    return iptools.long2ip(value)
