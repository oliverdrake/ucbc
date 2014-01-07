from orders import models

NZ_GST = 1.015


def add_gst(amount):
    return float(amount) * NZ_GST


def get_ingredient(name):
    try:
        return models.Hop.objects.get(name=name)
    except models.Hop.DoesNotExist:
        return models.Grain.objects.get(name=name)
