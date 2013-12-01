from django.contrib.auth import get_user_model
from orders.models import SingleIngredientOrder, Ingredient, UserOrder
from nose.tools import assert_equal

User = get_user_model()


class TestModels(object):
    @staticmethod
    def create_order_row(order, unit_cost=1.0, quantity=1):
        #order = Order()
        ingredient = Ingredient(unit_cost=unit_cost)
        ingredient.save()
        order_row = SingleIngredientOrder(
            ingredient=ingredient,
            order=order,
            quantity=quantity)
        order_row.save()
        return order_row

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
