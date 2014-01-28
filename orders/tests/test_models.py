from functools import partial
import random
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from nose.tools import assert_equal, raises
from paypal.standard.ipn.signals import payment_was_successful
from orders.models import Ingredient, OrdersEnabled, OrderItem, UserOrder, SupplierOrder, Supplier, Grain, Hop, Surcharge
from orders.utils import add_gst

User = get_user_model()


class TestIngredient(TestCase):
    @staticmethod
    def test_unit_size_plural_kg():
        kg_plural = partial(Ingredient.unit_size_plural, Ingredient.UNIT_SIZE_KG)
        assert_equal("1 Kg", kg_plural(1))
        assert_equal("2 Kgs", kg_plural(2))
        assert_equal("23 Kgs", kg_plural(23))

    @staticmethod
    def test_unit_size_plural_sack():
        sack_plural = partial(Ingredient.unit_size_plural, Ingredient.UNIT_SIZE_SACK)
        assert_equal("1 sack", sack_plural(1))
        assert_equal("2 sacks", sack_plural(2))
        assert_equal("23 sacks", sack_plural(23))

    @staticmethod
    def test_unit_size_plural_100g():
        gram_plural = partial(Ingredient.unit_size_plural, Ingredient.UNIT_SIZE_100G)
        assert_equal("100 grams", gram_plural(1))
        assert_equal("200 grams", gram_plural(2))
        assert_equal("2.3 Kg", gram_plural(23))
        assert_equal("15.2 Kg", gram_plural(152))

    @staticmethod
    @raises(ValueError)
    def test_unit_size_plural_bad_unit_size():
        Ingredient.unit_size_plural("bad unit size", 5)

    @staticmethod
    @raises(ValueError)
    def test_unit_size_plural_neg_quantity():
        Ingredient.unit_size_plural(Ingredient.UNIT_SIZE_SACK, -2)

    @staticmethod
    @raises(ValueError)
    def test_unit_size_plural_zero_quantity():
        Ingredient.unit_size_plural(Ingredient.UNIT_SIZE_SACK, 0)

    @staticmethod
    @raises(ValueError)
    def test_unit_size_plural_bad_string_quantity():
        Ingredient.unit_size_plural(Ingredient.UNIT_SIZE_SACK, "sdf")

    @staticmethod
    def test_ingredient_type_property():
        assert_equal("grain", Grain(name="grain").ingredient_type)
        assert_equal("hops", Hop(name="hops").ingredient_type)

    def test_unit_cost_excl_gst_incl_surcharge(self):
        Surcharge.objects.create(id=1, surcharge_percentage=3.4)
        grain = Grain(name="test", unit_cost=46.85)
        assert_equal(1.034 * 46.85, grain.unit_cost_excl_gst_incl_surcharge)


class TestOrdersEnabled(TestCase):
    def test_is_singleton(self):
        one = OrdersEnabled.objects.create(enabled=False)
        OrdersEnabled.objects.create(enabled=True)
        assert_equal(1, one.id)

    def test_is_enabled(self):
        assert_equal(0, OrdersEnabled.objects.count())
        self.assertFalse(OrdersEnabled.is_enabled())
        self.assertFalse(OrdersEnabled.is_enabled())
        assert_equal(1, OrdersEnabled.objects.count())


def create_order_item(order, supplier, unit_cost=1.0, quantity=1, supplier_order=None, name=None):
    if not name:
        name = "test_ingredient_%d" % random.randint(0, 9999)
    ingredient, _ = Ingredient.objects.get_or_create(
        unit_cost=unit_cost,
        name=name,
        supplier=supplier)
    order_item = OrderItem(
        ingredient=ingredient,
        user_order=order,
        quantity=quantity,
        supplier_order=supplier_order)
    order_item.save()
    return order_item


class TestOrderItem(TestCase):
    def test_singleingredientorder_total_gst_excl(self):
        supplier = Supplier.objects.create(name="testsupplier")
        order = UserOrder()
        order.user = User.objects.create_user("a")
        order.save()
        for (unit_cost, quantity) in ((2.5, 3), (4.6, 400.5)):
            order_item = create_order_item(order, supplier, unit_cost, quantity)
            assert_equal(quantity*unit_cost, order_item.total)


class TestUserOrder(TestCase):
    def test_order_total_gst_excl(self):
        Surcharge.objects.get_or_create(id=1, surcharge_percentage=3.4, order_surcharge=11.80)
        supplier = Supplier.objects.create(name="testsupplier")
        order = UserOrder()
        order.user = User.objects.create_user("b")
        order.save()
        create_order_item(order, supplier, unit_cost=3.5, quantity=2)
        create_order_item(order, supplier, unit_cost=2.1, quantity=5)
        order.save()
        total = 3.5 * 2 + 2.1 * 5
        total *= 1.034
        total = add_gst(total)
        total += 11.80
        assert_equal(total, order.total)


class TestSupplierOrder(TestCase):
    def test_supplier_order_total_gst_excl(self):
        supplier = Supplier.objects.create(name="testsupplier")
        supplier_order = SupplierOrder.objects.create(
            status=SupplierOrder.STATUS_PENDING,
            supplier=supplier)
        order = UserOrder()
        order.user = User.objects.create_user("c")
        order.save()
        create_order_item(order, supplier, unit_cost=3, quantity=5, supplier_order=supplier_order)
        create_order_item(order, supplier, unit_cost=1, quantity=7, supplier_order=supplier_order)
        assert_equal(22, supplier_order.total)

    def test_summary(self):
        supplier = Supplier.objects.create(name="testsupplier")
        supplier_order = SupplierOrder.objects.create(
            status=SupplierOrder.STATUS_PENDING,
            supplier=supplier)
        order = UserOrder()
        order.user = User.objects.create_user("c")
        order.save()
        create_order_item(order, supplier, unit_cost=3, quantity=5, supplier_order=supplier_order, name="Munich")
        create_order_item(order, supplier, unit_cost=1, quantity=7, supplier_order=supplier_order, name="Wheat")
        order2 = UserOrder()
        order2.user = User.objects.create_user("d")
        order2.save()
        create_order_item(order, supplier, unit_cost=3, quantity=7, supplier_order=supplier_order, name="Munich")
        create_order_item(order, supplier, unit_cost=3, quantity=9, supplier_order=supplier_order, name="Pilsener")
        assert_equal({
                'Munich': (12, 36.0),
                'Wheat': (7, 7.0),
                'Pilsener': (9, 27.0)
            },
            supplier_order.summary)


def test_Surcharge():
    assert_equal(0.0, Surcharge.get_surcharge_percentage())
    assert_equal(1.0, Surcharge.get_factor())
    assert_equal(0.0, Surcharge.get_surcharge_percentage())
    assert_equal(1, Surcharge.objects.count())
    Surcharge.objects.filter(id=1).update(surcharge_percentage=2.35, order_surcharge=23.50)
    assert_equal(2.35, Surcharge.get_surcharge_percentage())
    assert_equal(1.0235, Surcharge.get_factor())
    assert_equal(23.50, Surcharge.get_order_surcharge())

