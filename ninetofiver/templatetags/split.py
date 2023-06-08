from django import template

register = template.Library()

@register.filter
def split(value,arg:str):
    """Splits a string using the given argument"""
    if not value or not arg:
        return value

    return value.split(arg)