"""https://djangosnippets.org/snippets/552/"""
from django import template
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
register = template.Library()
from orders import utils


# https://djangosnippets.org/snippets/1825/
@register.filter
def currency(value, arg = '', symbol = True):
    '''
    Currency formatting template filter.

    Takes a number -- integer, float, decimal -- and formats it according to
    the locale specified as the template tag argument (arg). Examples:

      * {{ value|currency }}
      * {{ value|currency:"en_US" }}
      * {{ value|currency:"pt_BR" }}
      * {{ value|currency:"pt_BR.UTF8" }}

    If the argument is omitted, the default system locale will be used.

    The third parameter, symbol, controls whether the currency symbol will be
    printed or not. Defaults to true.

    As advised by the Django documentation, this template won't raise
    exceptions caused by wrong types or invalid locale arguments. It will
    return an empty string instead.

    Be aware that currency formatting is not possible using the 'C' locale.
    This function will fall back to 'en_US.UTF8' in this case.
    '''

    saved = '.'.join([x for x in locale.getlocale() if x]) or (None, None)
    given = arg and ('.' in arg and str(arg) or str(arg) + '.UTF-8')

    # Workaround for Python bug 1699853 and other possibly related bugs.
    if '.' in saved and saved.split('.')[1].lower() in ('utf', 'utf8'):
        saved = saved.split('.')[0] + '.UTF-8'

    if saved == (None, None) and given == '':
        given = 'en_US.UTF-8'

    try:
        locale.setlocale(locale.LC_ALL, given)

        return locale.currency(value or 0, symbol, True)

    except (TypeError, locale.Error):
        return ''

    finally:
        locale.setlocale(locale.LC_ALL, saved)


@register.filter()
def add_gst(amount):
    try:
        return utils.add_gst(float(amount))
    except TypeError:
        return ''
    except ValueError:
        return ''

