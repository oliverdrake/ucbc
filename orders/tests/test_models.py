from functools import partial
import random
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from nose.tools import assert_equal, raises
from orders.models import Ingredient, OrdersEnabled, OrderItem, UserOrder, SupplierOrder, Supplier, Grain, Hop

User = get_user_model()


class TestIngredient(object):
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

    def test_ingredient_type_property(self):
        assert_equal("grain", Grain(name="grain").ingredient_type)
        assert_equal("hops", Hop(name="hops").ingredient_type)


class TestOrdersEnabled(TestCase):
    def test_is_singleton(self):
        one = OrdersEnabled.objects.create(enabled=False)
        with self.assertRaises(IntegrityError):
            OrdersEnabled.objects.create(enabled=True)
        assert_equal(1, one.id)

    def test_is_enabled(self):
        assert_equal(0, OrdersEnabled.objects.count())
        self.assertFalse(OrdersEnabled.is_enabled())
        self.assertFalse(OrdersEnabled.is_enabled())
        assert_equal(1, OrdersEnabled.objects.count())


def create_order_item(order, unit_cost=1.0, quantity=1, supplier_order=None):
        ingredient = Ingredient(
            unit_cost=unit_cost,
            name="test_ingredient_%d" % random.randint(0, 9999))
        ingredient.save()
        order_item = OrderItem(
            ingredient=ingredient,
            user_order=order,
            quantity=quantity,
            supplier_order=supplier_order)
        order_item.save()
        return order_item


class TestOrderItem(TestCase):
    def test_singleingredientorder_total_gst_excl(self):
        order = UserOrder()
        order.user = User.objects.create_user("a")
        order.save()
        for (unit_cost, quantity) in ((2.5, 3), (4.6, 400.5)):
            order_item = create_order_item(order, unit_cost, quantity)
            assert_equal(quantity*unit_cost, order_item.total)


class TestUserOrder(TestCase):
    def test_order_total_gst_excl(self):
        order = UserOrder()
        order.user = User.objects.create_user("b")
        order.save()
        create_order_item(order, 3.5, 2)
        create_order_item(order, 2.1, 5)
        order.save()
        assert_equal(17.5, order.total)


class TestSupplierOrder(TestCase):
    def test_supplier_order_total_gst_excl(self):
        supplier_order = SupplierOrder.objects.create(
            status=SupplierOrder.STATUS_PENDING,
            supplier=Supplier.objects.create(name="testsupplier"))
        order = UserOrder()
        order.user = User.objects.create_user("c")
        order.save()
        create_order_item(order, unit_cost=3, quantity=5, supplier_order=supplier_order)
        create_order_item(order, unit_cost=1, quantity=7, supplier_order=supplier_order)
        assert_equal(22, supplier_order.total)
