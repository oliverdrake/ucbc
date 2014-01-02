"""
Django settings for ucbc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1zh-0h0eb=1@yk6+)f05(+3a2p5^l^xu*6^ho3*wffx9(#xijj'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

APPEND_SLASH = True

#AUTH_USER_MODEL = 'django.contrib.auth.models.User'

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sessions',

    'south',
    #'shop',
    'pipeline',
    'django_extensions',
    'twitter_bootstrap',
    'bootstrapform',
    #'django_generic_flatblocks',
    #'bootstrap_toolkit',


    'main',
    #'inventory',
    'orders',

)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', 'django_nose', 'django_webtest')
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
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

#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#    'apptemplates.Loader',
#)

SITE_ID = 1

ROOT_URLCONF = 'ucbc.urls'

WSGI_APPLICATION = 'ucbc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ADMIN_URL_PREFIX = "/admin/"


INTERNAL_IPS = ("127.0.0.1", "localhost")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "ucbc", "static"),
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

#PIPELINE_CSS = {
#    'bootstrap': {
#        'source_filenames': (
#            'less/bootstrap.less',
#        ),
#        'output_filename': 'css/b.css',
#        'extra_context': {
#            'media': 'screen,projection',
#        },
#    },
#}

PIPELINE_JS = {
    'bootstrap': {
        'source_filenames': (
          'js/transition.js',
          'js/modal.js',
          'js/dropdown.js',
          'js/scrollspy.js',
          'js/tab.js',
          'js/tooltip.js',
          'js/popover.js',
          'js/alert.js',
          'js/button.js',
          'js/collapse.js',
          'js/carousel.js',
          'js/affix.js',
        ),
        'output_filename': 'js/b.js',
    },
}


