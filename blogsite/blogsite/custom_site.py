"""自定义admin站点"""
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Blogsite 管理'
    site_title = 'Blogsite 站点管理'
    index_title = '首页'


custom_site = CustomSite(name='custom_admin')
