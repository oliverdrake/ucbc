from nose.tools import assert_equal
from main import __version__
from main.templatetags.ucbc import version


def test_version_template_tag():
    assert_equal(__version__, version())
