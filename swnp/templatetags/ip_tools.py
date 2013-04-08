'''
Created on 19.9.2012

@author: neriksso
'''
from django import template
import iptools
register = template.Library()

@register.filter(name='long2ip')
def long2ip(value):
    """Removes all values of arg from the given string"""
    return iptools.long2ip(value)
