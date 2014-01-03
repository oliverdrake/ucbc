from orders import models

NZ_GST = 1.015


def add_gst(amount):
    return float(amount) * NZ_GST


def get_ingredient(name):
    try:
        return models.Grain.objects.get(name=name)
    except models.Grain.DoesNotExist:
        return models.Hop.objects.get(name=name)


def get_ingredient_name(ingredient_id):
    return models.Ingredient.objects.get(id=ingredient_id).name
