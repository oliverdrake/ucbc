from orders import models
from orders.models import Surcharge

NZ_GST = 1.15


def add_gst(amount):
    return float(amount) * NZ_GST


def order_total_incl_gst(ingredients, quantities):
    item_total = lambda i, q: float(i.unit_cost_excl_gst_incl_surcharge) * q
    total = sum(map(item_total, ingredients, quantities))
    total = add_gst(total)
    total += Surcharge.get_order_surcharge()
    return total


def get_ingredient(name):
    try:
        return models.Hop.objects.get(name=name)
    except models.Hop.DoesNotExist:
        return models.Grain.objects.get(name=name)
