from django import template

# mathical functions in templates
register = template.Library()


@register.filter
def add(value, arg):
    return value + arg


@register.filter
def subtract(value, arg):
    return value - arg
