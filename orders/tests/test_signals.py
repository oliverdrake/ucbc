from django.conf import settings
import mock
from django.contrib.auth import get_user_model
from django.test import TestCase
from flatblocks.models import FlatBlock
from nose.tools import assert_equal
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.signals import payment_was_successful

from orders.signals import order_paid
from orders.models import UserOrder, OrderItem, Ingredient


class TestPaymentWasSuccessful(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.email_patch = mock.patch('django.core.mail.send_mail')
        cls.send_mail = cls.email_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls.email_patch.stop()

    def setUp(self):
        self.user = get_user_model().objects.create(username="test", password="test")
        self.user_order = UserOrder.objects.create(
            user=self.user)
        OrderItem.objects.create(
            ingredient=Ingredient.objects.create(name="Munich", unit_cost=2, unit_size="sack"),
            quantity=5,
            user_order=self.user_order)
        assert_equal(UserOrder.STATUS_UNPAID, self.user_order.status)
        self.email_message = FlatBlock.objects.create(
            slug='orders.email.confirmation',
            content="Order %(order_number)s, total: $%(total)s").content
        self.__class__.send_mail.reset_mock()

    def test_handler_flags_user_order_as_paid(self):
        ipn = PayPalIPN()
        ipn.invoice = str(self.user_order.id)
        payment_was_successful.send(sender=ipn)
        self.assert_order_paid()

    def test_handler_sends_email(self):
        ipn = PayPalIPN()
        ipn.invoice = str(self.user_order.id)
        payment_was_successful.send(sender=ipn)
        message = self.email_message % dict(
            order_number=self.user_order.id,
            total=UserOrder.objects.get(id=self.user_order.id).total,
        )
        self.__class__.send_mail.assert_called_once_with(
            'Your UCBC Order #%d' % self.user_order.id,
            message,
            settings.ORDER_FROM_EMAIL,
            [self.user.email, settings.ORDER_FROM_EMAIL],
            fail_silently=True,
            auth_user=settings.ORDER_EMAIL_HOST_USER,
            auth_password=settings.ORDER_EMAIL_HOST_PASSWORD,
        )

    @mock.patch("logging.getLogger")
    def test_order_already_paid(self, getLogger):
        log = getLogger()
        self.user_order.status = UserOrder.STATUS_PAID
        self.user_order.save()
        self.test_handler_flags_user_order_as_paid()
        log.error.assert_called_once_with("UserOrder #%d already paid!" % self.user_order.id)

    @mock.patch("logging.getLogger")
    def test_payment_was_successful_handler_no_invoice(self, getLogger):
        log = getLogger()
        payment_was_successful.send(sender=PayPalIPN())
        log.error.assert_called_once_with("Invalid invoice id: ")

    @mock.patch("logging.getLogger")
    def test_payment_was_successful_handler_user_order_doesnt_exist(self, getLogger):
        log = getLogger()
        ipn = PayPalIPN()
        ipn.invoice = "5"
        payment_was_successful.send(sender=ipn)
        log.error.assert_called_once_with("No UserOrder with id: %d" % 5)

    def assert_order_paid(self):
        user_order = UserOrder.objects.get(id=self.user_order.id)
        assert_equal(UserOrder.STATUS_PAID, user_order.status)
