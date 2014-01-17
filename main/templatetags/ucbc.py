from django import template
from main import __version__

register = template.Library()


@register.simple_tag
def version(*args, **kwargs):
    return __version__
