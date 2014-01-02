"""https://djangosnippets.org/snippets/552/"""
from django import template
import locale
locale.setlocale(locale.LC_ALL, '')
register = template.Library()
from orders import utils


@register.filter()
def currency(value):
    try:
        return locale.currency(value, grouping=True)
    except TypeError:
        return "$?"


@register.filter()
def add_gst(amount):
    return utils.add_gst(float(amount))
