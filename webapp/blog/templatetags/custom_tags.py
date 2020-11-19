from django import template

register = template.Library()


@register.filter
def replace_quotes(value):
    return value.replace("'", '"')

@register.filter
def replace_plus(value):
    return value.replace("+", " ")