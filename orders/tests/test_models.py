from functools import partial
from nose.tools import assert_equal, raises
from orders.models import Ingredient


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
