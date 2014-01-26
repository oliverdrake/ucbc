import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"), )

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

DEBUG = False
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
APPEND_SLASH = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@ucbc.org.nz'
DEFAULT_FROM_EMAIL = 'admin@ucbc.org.nz'

INSTALLED_APPS = (
    'django_admin_bootstrapped',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.formtools',

    'south',
    'bootstrapform',
    'flatblocks',
    'minidetector',
    'paypal.standard.ipn',

    'main',
    'orders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'minidetector.Middleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
)

SITE_ID = 1
ROOT_URLCONF = 'ucbc.urls'
WSGI_APPLICATION = 'ucbc.wsgi.application'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
ADMIN_URL_PREFIX = "/admin/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
PAYPAL_RECEIVER_EMAIL = "president@ucbc.org.nz"

