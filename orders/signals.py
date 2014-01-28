import logging
from django.core import mail
from flatblocks.models import FlatBlock


def order_paid(sender, **kwargs):
    from orders import models
    log = logging.getLogger("orders.signals.order_paid")
    ipn_obj = sender
    try:
        user_order_id = int(ipn_obj.invoice)
    except ValueError:
        log.error("Invalid invoice id: %s" % ipn_obj.invoice)
        return
    log.info("payment success, order #%d" % user_order_id)
    if models.UserOrder.objects.filter(
            id=user_order_id,
            status=models.UserOrder.STATUS_PAID).count() > 0:
        log.error("UserOrder #%d already paid!" % user_order_id)
    try:
        user_order = models.UserOrder.objects.get(id=user_order_id)
        user_order.status = models.UserOrder.STATUS_PAID
        user_order.save()
        _email_order_confirmation(user_order)
    except models.UserOrder.DoesNotExist:
        log.error("No UserOrder with id: %d" % user_order_id)


def _email_order_confirmation(user_order):
    message = FlatBlock.objects.get(slug='orders.email.confirmation').content % dict(
        order_number=user_order.id,
        total=user_order.total,
    )
    mail.send_mail(
        'Your UCBC Order #%d' % user_order.id,
        message,
        None,
        [user_order.user.email],
        fail_silently=True)
