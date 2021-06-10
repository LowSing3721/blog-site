from django.shortcuts import render
from django.views.generic import ListView

from .models import Link
from blog.views import CommonViewMixin


class LinkListView(CommonViewMixin, ListView):
    model = Link
    queryset = Link.get_all()
    template_name = 'config/links.html'
    context_object_name = 'link_list'
