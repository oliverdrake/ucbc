from django.test import TestCase
from nose.tools import assert_equal, raises
from orders.models import Hop, Ingredient, Supplier, Grain, Surcharge
from orders.utils import get_ingredient, order_total_incl_gst, add_gst


class TestGetIngredient(TestCase):
    def setUp(self):
        self.nzhops = Supplier(name="NZ Hops")
        self.cryer = Supplier(name="Cryer")

    def test_no_grain(self):
        hop = Hop.objects.create(name="saaz", unit_cost=12.3, unit_size="100g", supplier=self.nzhops)
        assert_equal(hop, get_ingredient("saaz"))

    def test_no_hops(self):
        grain = Grain.objects.create(name="munich", unit_cost=12.3, unit_size="sack", supplier=self.cryer)
        assert_equal(grain, get_ingredient("munich"))

    @raises(Grain.DoesNotExist)
    def test_no_hops_or_grain(self):
        get_ingredient("wheat")


def test_order_total():
    nzhops = Supplier.objects.create(name="NZ Hops")
    cryer = Supplier.objects.create(name="Cryer")
    Surcharge.objects.filter(id=1).update(surcharge_percentage=4.7, order_surcharge=12.70)
    grain = Grain.objects.create(name="munich", unit_cost=12.3, unit_size="sack", supplier=cryer)
    hop = Hop.objects.create(name="saaz", unit_cost=34.4, unit_size="100g", supplier=nzhops)
    total = order_total_incl_gst([grain, hop], [5, 6])
    expected_total = grain.unit_cost * 5 + hop.unit_cost * 6
    expected_total *= 1.047
    expected_total = add_gst(expected_total)
    expected_total += 12.70
    assert_equal(round(expected_total, 3), round(total, 3))
