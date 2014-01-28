from collections import OrderedDict
import csv
from http.client import CREATED, OK, BAD_REQUEST, FORBIDDEN, FOUND, NOT_FOUND
import mimetypes
from io import StringIO
import os
import tempfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase
from django_nose.tools import assert_ok, assert_code
from django_webtest import WebTest
import mock
from nose.tools import raises
from webtest import AppError

from orders.models import Grain, Supplier, Hop, UserOrder, OrdersEnabled, SupplierOrder, OrderItem, Ingredient
from orders import utils

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
        self.orders_enabled, success = OrdersEnabled.objects.get_or_create(id=1)
        self.orders_enabled.enabled = True
        self.orders_enabled.save()


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

    def test_get_orders_disabled(self):
        self.orders_enabled.enabled = False
        self.orders_enabled.save()
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(self.url)
        assert_code(response, BAD_REQUEST)


class _WebTest(WebTest, _CommonMixin):
    def setUp(self):
        _CommonMixin.setUp(self)

    def _login(self):
        form = self.app.get(reverse('login')).form
        form['username'] = 'temporary'
        form['password'] = 'temporary'
        response = form.submit().follow()
        assert_code(response, OK)



class _IngredientPostBase(_WebTest):
    url = None

    @raises(AppError)
    def test_post_orders_disabled_returns_400(self):
        self._login()
        response = self.app.get(self.url)
        self.orders_enabled.enabled = False
        self.orders_enabled.save()
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = 5
        add_grain_to_order_form.submit()

    @raises(AppError)
    def test_post_invalid_data_returns_400(self):
        self._login()
        response = self.app.get(self.url)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = "bad_quantity"
        add_grain_to_order_form.submit()


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
    url = ORDER_GRAINS_URL

    def test_post_happy_path(self):
        self._login()
        response = self.app.get(self.url)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = 5
        response = add_grain_to_order_form.submit()
        self.assertRedirects(response, self.url)
        response = response.follow()

        cart_form = response.forms.get(1)
        self.assertEqual(str(self.munich.id), cart_form.get('cart-0-ingredient').value)
        self.assertEqual('5', cart_form.get('cart-0-quantity').value)


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
    url = ORDER_HOPS_URL

    def test_post_happy_path(self):
        self._login()
        response = self.app.get(self.url)
        add_grain_to_order_form = response.forms.get(0)
        add_grain_to_order_form['ingredients-0-quantity'] = 5
        response = add_grain_to_order_form.submit()
        self.assertRedirects(response, self.url)
        response = response.follow()
        cart_form = response.forms.get(1)
        self.assertEqual(str(self.sauvin.id), cart_form.get('cart-0-ingredient').value)
        self.assertEqual('5', cart_form.get('cart-0-quantity').value)


class TestCartDeleteItem(_WebTest):
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


class TestCheckout(_WebTest):
    @mock.patch('django.core.mail.send_mail')
    def test_email_sent(self, send_mail):
        from flatblocks.models import FlatBlock


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
        cart_form.submit()
        order_number = UserOrder.objects.count()


        self.assertGreater(UserOrder.objects.get(id=order_number).total, 0)


class TestSupplierOrderSummaryCSV(TestCase, _CommonMixin):
    def setUp(self):
        super(TestSupplierOrderSummaryCSV, self).setUp()
        _CommonMixin.setUp(self)
        self.client = Client()
        self.order = UserOrder.objects.create(user=User.objects.create_user("c"))
        OrderItem.objects.create(
            ingredient=self.munich,
            quantity=5,
            user_order=self.order,
        )
        OrderItem.objects.create(
            ingredient=self.sauvin,
            quantity=3,
            user_order=self.order,
        )
        self.order2 = UserOrder.objects.create(user=User.objects.create_user("d"))
        OrderItem.objects.create(
            ingredient=self.munich,
            quantity=7,
            user_order=self.order2,
        )
        OrderItem.objects.create(
            ingredient=self.sauvin,
            quantity=2,
            user_order=self.order2,
        )

    def test(self):
        self.assertTrue(self.client.login(username='temporary', password='temporary'))
        order = SupplierOrder.objects.create(
            supplier=self.gladfields,
            status=SupplierOrder.STATUS_ORDERED)
        OrderItem.objects.filter(supplier_order=None, ingredient__supplier=self.gladfields).update(supplier_order=order)
        response = self.client.get(reverse('supplier_order_summary_csv', args=(order.id,)))
        assert_ok(response)
        self.assertEqual(mimetypes.types_map['.csv'], response['Content-Type'])
        self.assertEqual('attachment; filename="Gladfields_order.csv"', response['Content-Disposition'])
        response_body = response.content.decode(encoding='UTF-8')
        f = StringIO(response_body)
        reader = csv.reader(f)
        self.assertIn(["Name", "Quantity"], reader)
        self.assertIn(["Munich", "12 sacks"], reader)

    def test_login_required(self):
        order = SupplierOrder.objects.create(
            supplier=self.gladfields,
            status=SupplierOrder.STATUS_ORDERED)
        response = self.client.get(reverse('supplier_order_summary_csv', args=(order.id,)))
        assert_code(response, FOUND)
        self.assertIn('login', response['Location'])


class TestImportIngredientsFromCSV(_WebTest, _CommonMixin):
    def setUp(self):
        # super(TestSupplierOrderSummaryCSV, self).setUp()
        _CommonMixin.setUp(self)
        # self.client = Client()

    def create_csv(self, tempdir, *rows):
        filename = os.path.join(tempdir, "temp.csv")
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'unit_cost', 'unit_size', 'supplier_name', 'type'])
            writer.writerows(rows)
        return filename

    def submit_file_form(self, filename, response):
        form = response.form
        form['file'] = StringIO(filename)
        return form.submit()

    def _assert_ingredient(self, model, name, cost, size, supplier_name):
        new_ingredient = model.objects.get(name=name)
        self.assertEqual(new_ingredient.unit_cost, cost)
        self.assertEqual(new_ingredient.unit_size, size)
        self.assertEqual(new_ingredient.supplier, Supplier.objects.get(name=supplier_name))

    def assert_grain(self, name, cost, size, supplier_name):
        return self._assert_ingredient(Grain, name, cost, size, supplier_name)

    def assert_hop(self, name, cost, size, supplier_name):
        return self._assert_ingredient(Hop, name, cost, size, supplier_name)

    def assert_no_ingredient(self, name):
        self.assertRaises(Ingredient.DoesNotExist, Ingredient.objects.get, name=name)

    def test_grains_created(self):
        self._login()
        for name, cost, size, supplier_name in (('Test Grain', '12', 'sack', 'Gladfields'),
                                                ('Test 2', '23', 'Kg', 'Gladfields')):
            response = self.app.get(reverse('import_ingredients', args=('Grain',)))
            with tempfile.TemporaryDirectory() as tempdir:
                filename = self.create_csv(tempdir, [name, cost, size, supplier_name])
                response = self.submit_file_form(filename, response)
                assert_code(response, FOUND)
                self.assertIn(reverse('import_ingredients', args=('Grain',)), response['Location'])
            self.assert_grain(name, float(cost), size, supplier_name)


    def test_hops_created(self):
        self._login()
        for name, cost, size, supplier_name in (('Saaz', '12', '100g', 'NZ Hops'),
                                                ('Test Hop', '23', 'Kg', 'NZ Hops')):
            response = self.app.get(reverse('import_ingredients', args=('Hop',)))
            with tempfile.TemporaryDirectory() as tempdir:
                filename = self.create_csv(tempdir, [name, cost, size, supplier_name])
                response = self.submit_file_form(filename, response)
                assert_code(response, FOUND)
                self.assertIn(reverse('import_ingredients', args=('Hop',)), response['Location'])
            self.assert_hop(name, float(cost), size, supplier_name)

    @raises(AppError)
    def test_supplier_doesnt_exist_404(self):
        self._login()
        response = self.app.get(reverse('import_ingredients', args=('Grain',)))
        with tempfile.TemporaryDirectory() as tempdir:
            filename = self.create_csv(tempdir, ["Test Grain", 13, "Kg", "bad supplier"])
            self.submit_file_form(filename, response)

    def test_bad_unit_size(self):
        self._login()
        response = self.app.get(reverse('import_ingredients', args=('Grain',)))
        with tempfile.TemporaryDirectory() as tempdir:
            filename = self.create_csv(tempdir, ["Test Grain", 13, "bad unit size", "Gladfields"])
            response = self.submit_file_form(filename, response)
            assert_code(response, FOUND)
            self.assertIn(reverse('import_ingredients', args=('Grain',)), response['Location'])
        self.assert_no_ingredient("Test Grain")


    def test_login_required(self):
        response = self.app.get(reverse('import_ingredients', args=('Hop',)))
        assert_code(response, FOUND)
        self.assertIn(reverse('login'), response['Location'])
