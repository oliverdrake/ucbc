from collections import OrderedDict
from http.client import CREATED, OK, BAD_REQUEST
from unittest import skip
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.backends.dummy.base import ignore
from django.forms.formsets import formset_factory
from django.conf import settings
from django.test.client import Client
from django.test import TestCase
from django_nose.tools import assert_ok, assert_code
from django_webtest import WebTest
import mock
from nose.tools import raises
from webtest import AppError

from orders.models import Grain, Supplier, Hop, UserOrder
from orders import utils
from orders.views import CONFIRMATION_EMAIL

ORDER_GRAINS_URL = reverse('order_grain')
ORDER_HOPS_URL = reverse('order_hops')
CHECKOUT_URL = reverse('checkout')


class _CommonMixin(object):
    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.gladfields = Supplier.objects.create(name="Gladfields")
        self.nzhops = Supplier.objects.create(name="NZ Hops")
        self.munich = Grain.objects.create(
            name="Munich",
            unit_cost=12.5,
            unit_size=Grain.UNIT_SIZE_SACK,
            supplier=self.gladfields)
        self.sauvin = Hop.objects.create(
            name="Nelson Sauvin",
            unit_cost=4,
            unit_size=Hop.UNIT_SIZE_100G,
            supplier=self.nzhops)


class _IngredientGetBase(TestCase, _CommonMixin):
    url = None

    def setUp(self):
        _CommonMixin.setUp(self)
        self.client = Client()

    def tearDown(self):
        self.client.logout()

    def test_not_logged_in_redirected_to_login_page(self):
        expected_url = "%s?next=%s" % (reverse('login'), self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url)
        response = self.client.post(self.url, data={})
        self.assertRedirects(response, expected_url)


class _IngredientPostBase(WebTest, _CommonMixin):
    def setUp(self):
        _CommonMixin.setUp(self)

    def _login(self):
        form = self.app.get(reverse('login')).form
        form['username'] = 'temporary'
        form['password'] = 'temporary'
        response = form.submit().follow()
        assert_code(response, OK)


class TestGrainsGet(_IngredientGetBase):
    url = ORDER_GRAINS_URL

    def test_get_happy_path(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.url)
        assert_ok(response)
        formset_ = response.context['ingredient_formset']

        ingredient_names = [f.initial.get('ingredient_name') for f in formset_]
        self.assertIn(self.munich.name, ingredient_names)


class TestGrainsPost(_IngredientPostBase):
    def test_post_happy_path(self):
        self._login()
        response = self.app.get(ORDER_GRAINS_URL)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = 5
        response = add_grain_to_order_form.submit()
        self.assertRedirects(response, ORDER_GRAINS_URL)
        response = response.follow()

        cart_form = response.forms.get(1)
        self.assertEqual(str(self.munich.id), cart_form.get('cart-0-ingredient').value)
        self.assertEqual('5', cart_form.get('cart-0-quantity').value)

    @raises(AppError)
    def test_post_invalid_data_returns_400(self):
        self._login()
        response = self.app.get(ORDER_GRAINS_URL)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = "bad_quantity"
        add_grain_to_order_form.submit()


class TestHopsGet(_IngredientGetBase):
    url = ORDER_HOPS_URL

    def test_get_happy_path(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.url)
        assert_ok(response)
        formset_ = response.context['ingredient_formset']
        ingredient_names = [f.initial.get('ingredient_name') for f in formset_]
        self.assertIn(self.sauvin.name, ingredient_names)


class TestHopsPost(_IngredientPostBase):
    def test_post_happy_path(self):
        self._login()
        response = self.app.get(ORDER_HOPS_URL)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = 5
        response = add_grain_to_order_form.submit()
        self.assertRedirects(response, ORDER_HOPS_URL)
        response = response.follow()

        cart_form = response.forms.get(1)
        self.assertEqual(str(self.sauvin.id), cart_form.get('cart-0-ingredient').value)
        self.assertEqual('5', cart_form.get('cart-0-quantity').value)

    @raises(AppError)
    def test_post_invalid_data_returns_400(self):
        self._login()
        response = self.app.get(ORDER_HOPS_URL)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = "bad_quantity"
        add_grain_to_order_form.submit()


class TestCartDeleteItem(_IngredientPostBase):
    def test_happy_path(self):
        self._login()
        # Add some hops to cart:
        response = self.app.get(ORDER_HOPS_URL)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = 5
        response = add_grain_to_order_form.submit()
        self.assertRedirects(response, ORDER_HOPS_URL)
        response = response.follow()

        cart_form = response.forms.get(1)
        self.assertEqual(str(self.sauvin.id), cart_form.get('cart-0-ingredient').value)
        self.assertEqual('5', cart_form.get('cart-0-quantity').value)

        # delete from cart:
        params=cart_form.submit_fields()
        params.append(('ingredient_id', self.sauvin.id))
        response.goto(reverse('remove_item'), method='post', params=params)
        assert_ok(response)
        response = self.app.get(ORDER_HOPS_URL)
        cart_form = response.forms.get(1)
        self.assertNotIn('cart-0-ingredient', cart_form.fields)


class TestCheckout(_IngredientPostBase):
    @mock.patch('django.core.mail.send_mail')
    def test_email_sent(self, send_mail):
        self._login()
        # Add some hops to cart:
        response = self.app.get(ORDER_HOPS_URL)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = 5
        response = add_grain_to_order_form.submit()
        self.assertRedirects(response, ORDER_HOPS_URL)
        response = response.follow()

        cart_form = response.forms.get(1)
        self.assertEqual(str(self.sauvin.id), cart_form.get('cart-0-ingredient').value)
        self.assertEqual('5', cart_form.get('cart-0-quantity').value)

        response = cart_form.submit()
        cart_form = response.forms.get(0)
        response = cart_form.submit()
        order_number = UserOrder.objects.count()
        message = CONFIRMATION_EMAIL % dict(
            order_number=order_number,
            total=utils.add_gst(UserOrder.objects.get(id=order_number).total),
            account_number=settings.ACCOUNT_NUMBER,
        )
        send_mail.assert_called_once_with(
            'Your UCBC Order #%d' % order_number,
            message,
            None,
            [self.user.email],
            fail_silently=True
        )
