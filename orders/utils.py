NZ_GST = 1.015


def add_gst(amount):
    return float(amount) * NZ_GST


# class Cart(object):
#     def __init__(self, request):
#         self.request = request
#         self.data = request.session.setdefault('cart', {})
#
#     def update(self, new_data):
#         for name, quantity in new_data.items():
#             if quantity and quantity > 0:
#                 self.data[name] = quantity + self.data.get(name, 0)
#                 self.request.session.modified = True
#
