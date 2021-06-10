from django.contrib import admin

from .models import Link, SideBar
from blogsite.custom_site import custom_site
from blogsite.base_admin import MyAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(MyAdmin):
    list_display = ['title', 'href', 'status', 'weight', 'created_time']
    fields = ['title', 'href', 'status', 'weight']


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(MyAdmin):
    list_display = ['title', 'display_type', 'content', 'created_time']
    fields = ['title', 'display_type', 'content', 'status']
