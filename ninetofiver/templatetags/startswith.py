from django import template

register = template.Library()

@register.filter
def startswith(value,arg:str):
    """Checks if value starts with arg"""
    if not value or not arg:
        return value

    return value.startswith(arg)