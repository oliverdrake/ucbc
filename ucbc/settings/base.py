import os
from .secret import EMAIL_HOST_PASSWORD, SECRET_KEY, ORDER_EMAIL_HOST_PASSWORD
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"), )

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

DEBUG = False
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
APPEND_SLASH = True


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
    'gravatar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

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
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
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
PAYPAL_RECEIVER_EMAIL = "orders@ucbc.org.nz"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_ADAPTER = "main.other.AuthAdaptor"
