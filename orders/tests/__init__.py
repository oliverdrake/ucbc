import random
from django.contrib.auth import get_user_model
from orders.models import OrderItem, Ingredient, UserOrder, SupplierOrder, Supplier, Hop, Grain
from orders.templatetags.currency import currency
from nose.tools import assert_equal

User = get_user_model()


class TestModels(object):
    @staticmethod
    def create_order_row(order, unit_cost=1.0, quantity=1, supplier_order=None):
        ingredient = Ingredient(
            unit_cost=unit_cost,
            name="test_ingredient_%d" % random.randint(0, 999))
        ingredient.save()
        order_item = OrderItem(
            ingredient=ingredient,
            user_order=order,
            quantity=quantity,
            supplier_order=supplier_order)
        order_item.save()
        return order_item

    def test_singleingredientorder_total_gst_excl(self):
        order = UserOrder()
        order.user = User.objects.create_user("a")
        order.save()
        for (unit_cost, quantity) in ((2.5, 3), (4.6, 400.5)):
            order_row = self.__class__.create_order_row(order, unit_cost, quantity)
            assert_equal(quantity*unit_cost, order_row.total)

    def test_order_total_gst_excl(self):
        order = UserOrder()
        order.user = User.objects.create_user("b")
        order.save()
        self.__class__.create_order_row(order, 3.5, 2)
        self.__class__.create_order_row(order, 2.1, 5)
        order.save()
        assert_equal(17.5, order.total)

    def test_supplier_order_total_gst_excl(self):
        supplier_order = SupplierOrder.objects.create(
            status=SupplierOrder.STATUS_PENDING,
            supplier=Supplier.objects.create(name="testsupplier"))
        order = UserOrder()
        order.user = User.objects.create_user("c")
        order.save()
        self.__class__.create_order_row(order, unit_cost=3, quantity=5, supplier_order=supplier_order)
        self.__class__.create_order_row(order, unit_cost=1, quantity=7, supplier_order=supplier_order)
        assert_equal(22, supplier_order.total)

    def test_ingredient_type_property(self):
        assert_equal("grain", Grain(name="grain").ingredient_type)
        assert_equal("hops", Hop(name="hops").ingredient_type)


class TestTemplateTags(object):
    def test_currency(self):
        assert_equal("$22.50", currency(22.5))
        assert_equal("$3.00", currency(3))
        assert_equal("-$5.00", currency(-5))
        assert_equal("$?", currency(""))
        assert_equal("$?", currency(None))
        assert_equal("$0.00", currency(0))
