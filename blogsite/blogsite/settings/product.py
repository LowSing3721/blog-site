"""生产环境配置"""
import os

from .base import *


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blogsite',
        'HOST': 'mysql',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'root',
        'CONN_MAX_AGE': 5 * 60,
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{asctime} - [{levelname}] - {module}:{funcName}:{lineno} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
