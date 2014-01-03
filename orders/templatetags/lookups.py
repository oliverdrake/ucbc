from django import template
from orders import utils

register = template.Library()

@register.filter
def ingredient_name(ingredient_id):
    return utils.get_ingredient_name(ingredient_id)
