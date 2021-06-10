import os

from django.core.wsgi import get_wsgi_application

# 开发/生产环境配置拆分
_profile = os.environ.get('BLOGSITE_PROFILE', 'product')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'blogsite.settings.{_profile}')

application = get_wsgi_application()
