from .base import *

ALLOWED_HOSTS = ['.amazonaws.com', 'ucbc.org.nz', 'www.ucbc.org.nz', '54.206.72.134']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@ucbc.org.nz'
DEFAULT_FROM_EMAIL = 'admin@ucbc.org.nz'
ORDER_FROM_EMAIL = 'orders@ucbc.org.nz'
ORDER_EMAIL_HOST_USER = ORDER_FROM_EMAIL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/ucbc/django.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['logfile'],
            'level': 'ERROR',
        },
    }
}
