from nose.tools import assert_equal
from orders.templatetags.currency import currency, add_gst


def test_currency():
    assert_equal("$22.50", currency(22.5))
    assert_equal("$3.00", currency(3))
    assert_equal("-$5.00", currency(-5))
    assert_equal("$0.00", currency(""))
    assert_equal("$0.00", currency(None))
    assert_equal("$0.00", currency(0))


def test_add_gst():
    for value in (22.5, 134.23, 27.2, 4.5):
        assert_equal(value * 1.15, add_gst(value))
    assert_equal(0, add_gst(0))
    assert_equal(23 * 1.15, add_gst("23"))
    assert_equal('', add_gst(None))
    assert_equal('', add_gst(""))
    assert_equal(-3 * 1.15, add_gst(-3))
