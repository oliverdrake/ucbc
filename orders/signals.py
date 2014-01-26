from paypal.standard.ipn.signals import payment_was_successful

def order_paid(sender, **kwargs):
    ipn_obj = sender
    print("Paid!")

payment_was_successful.connect(order_paid)
