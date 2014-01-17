from django.contrib.auth import get_user_model
from django.test import TestCase
from nose.tools import assert_equal
from orders.forms import SupplierOrderAdminForm
from orders.models import Supplier, Grain, Ingredient, Hop, UserOrder, OrderItem, SupplierOrder


class TestSupplierOrderAdminForm(TestCase):
    def test_no_supplier_no_exception_raised(self):
        form = SupplierOrderAdminForm()

    def test_happy_path(self):
        supplier = Supplier.objects.create(name="Gladfields")
        munich = Grain.objects.create(
            name="Munich",
            unit_cost=36,
            unit_size=Ingredient.UNIT_SIZE_SACK,
            supplier=supplier)
        saaz = Hop.objects.create(
            name="Saaz",
            unit_cost=10,
            unit_size=Ingredient.UNIT_SIZE_100G,
            supplier=supplier)
        user = get_user_model().objects.get(id=1)
        user_order = UserOrder.objects.create(user=user)
        item1 = OrderItem.objects.create(
            ingredient=munich,
            quantity=2,
            user_order=UserOrder.objects.create(user=user))
        item2 = OrderItem.objects.create(
            ingredient=saaz,
            quantity=3,
            user_order=UserOrder.objects.create(user=user))
        form = SupplierOrderAdminForm(data={
            'ingredient_orders': [item1.id, item2.id],
            'supplier': supplier.id,
            'status': SupplierOrder.STATUS_PENDING,
        })
        supplier_order = form.save()
        assert_equal(supplier_order.supplier, supplier)
        assert_equal(supplier_order.ingredient_orders.get(id=item1.id), item1)
        assert_equal(supplier_order.ingredient_orders.get(id=item2.id), item2)
