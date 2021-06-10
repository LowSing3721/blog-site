"""开发环境配置"""
from .base import *

SECRET_KEY = 'django-insecure-3+3_+!d12=qn38e&#jv-$m&!tia59mk7(7qu_ns%ec!r_8obqe'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://192.168.28.128:6379/1",
#         "TIMEOUT": 60 * 5,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "PASSWORD": "test",
#         }
#     }
# }

# 性能排查工具django-debug-toolbar配置
INSTALLED_APPS += [
    'debug_toolbar'
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
INTERNAL_IPS = ['127.0.0.1']
