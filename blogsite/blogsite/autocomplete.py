"""自动补全模块"""
from dal import autocomplete

from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # 未登录用户返回空查询集
        if not self.request.user.is_authenticated:
            return Category.objects.none()
        # 已登录用户返回当前用户下的数据集
        qs = Category.objects.filter(owner=self.request.user)
        # 根据输入补全
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()
        qs = Tag.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
