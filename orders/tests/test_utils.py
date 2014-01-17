from django.test import TestCase
from nose.tools import assert_equal, raises
from orders.models import Hop, Ingredient, Supplier, Grain
from orders.utils import get_ingredient


class TestGetIngredient(TestCase):

    def setUp(self):
        self.nzhops = Supplier(name="NZ Hops")
        self.cryer = Supplier(name="Cryer")

    def test_no_grain(self):
        hop = Hop.objects.create(name="saaz", unit_cost=12.3, unit_size=Ingredient.UNIT_SIZE_100G, supplier=self.nzhops)
        assert_equal(hop, get_ingredient("saaz"))

    def test_no_hops(self):
        grain = Grain.objects.create(name="munich", unit_cost=12.3, unit_size=Ingredient.UNIT_SIZE_SACK, supplier=self.cryer)
        assert_equal(grain, get_ingredient("munich"))

    @raises(Grain.DoesNotExist)
    def test_no_hops_or_grain(self):
        get_ingredient("wheat")

