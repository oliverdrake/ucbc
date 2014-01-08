from .base import *
from .secret import EMAIL_HOST_PASSWORD, ACCOUNT_NUMBER, SECRET_KEY

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DEBUG = False

INSTALLED_APPS += (
    'debug_toolbar',
    'django_nose',
    'django_webtest',
    'django_extensions',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
INTERNAL_IPS = ("127.0.0.1", "localhost")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



