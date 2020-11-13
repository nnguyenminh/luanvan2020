from django import template

register = template.Library()


@register.filter
def raw(value):
    return value.replace("=", "")
