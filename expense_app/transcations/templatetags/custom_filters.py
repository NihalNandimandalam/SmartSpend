from django import template
register = template.Library()

@register.filter(name='to_list')
def to_list(value):
    return [value]