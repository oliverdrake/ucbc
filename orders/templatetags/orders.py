from django import template
from orders import models
from orders import utils

register = template.Library()
get_ingredient = models.Ingredient.objects.get


@register.filter
def ingredient_name(ingredient_id):
    return get_ingredient(id=int(ingredient_id)).name


@register.assignment_tag
def ingredient_id(ingredient_name):
    return get_ingredient(name=ingredient_name).id


@register.assignment_tag
def order_item_total(ingredient_id, quantity):
    unit_cost = float(get_ingredient(id=ingredient_id).unit_cost_excl_gst_incl_surcharge)
    return unit_cost * float(quantity)


@register.assignment_tag
def order_total(formset):
    ingredient = lambda id_: get_ingredient(id=id_)
    ingredients = map(ingredient, [int(f['ingredient'].value()) for f in formset])
    quantities = [int(f['quantity'].value()) for f in formset]
    return utils.order_total_incl_gst(ingredients, quantities)


@register.assignment_tag
def unit_size_plural(ingredient_id, quantity):
    ingredient = get_ingredient(id=ingredient_id)
    try:
        return models.Ingredient.unit_size_plural(ingredient.unit_size, quantity)
    except Exception:
        return quantity
