from django import template
from main import __version__

register = template.Library()


@register.simple_tag
def version(*args, **kwargs):
    return __version__


@register.assignment_tag
def to_class_name(value):
    return value.__class__.__name__

