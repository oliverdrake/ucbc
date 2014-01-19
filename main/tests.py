from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND
from django.core.urlresolvers import reverse
from django_nose.tools import assert_ok, assert_code
from nose.tools import assert_equal, assert_in
from django.test import Client
from main import __version__
from main.templatetags.ucbc import version
from flatblocks.models import FlatBlock


def test_version_template_tag():
    assert_equal(__version__, version())


def test_howto_view():
    content = "<p>Testing 123</p>"
    block = FlatBlock.objects.create(
        slug='test.howto',
        header='Test Heading',
        content=content)
    client = Client()
    response = client.get(reverse('main.views.howto', kwargs=dict(name='test.howto')))
    assert_ok(response)
    assert_in('Test Heading', str(response.content))
    assert_in(content, str(response.content))


def test_howto_flatblock_doesnt_exist_500():
    client = Client()
    response = client.get(reverse('main.views.howto', kwargs=dict(name='bad.flatblock')))
    assert_code(response, NOT_FOUND)

