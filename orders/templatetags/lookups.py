from django import template
from orders import utils
from orders import models

register = template.Library()


@register.filter
def ingredient_name(ingredient_id):
    return models.Ingredient.objects.get(id=int(ingredient_id)).name


@register.assignment_tag
def order_item_total(ingredient_id, quantity):
    unit_cost = float(models.Ingredient.objects.get(id=ingredient_id).unit_cost)
    return unit_cost * float(quantity)


@register.assignment_tag
def order_total(formset):
    ingredient = lambda id_: models.Ingredient.objects.get(id=id_)
    ingredients = map(ingredient, [f['ingredient'].value() for f in formset])
    quantities = [f['quantity'].value() for f in formset]
    total = lambda i, q: float(i.unit_cost) * q
    return sum(map(total, ingredients, quantities))
