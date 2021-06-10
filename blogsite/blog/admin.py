from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.shortcuts import reverse

from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from blogsite.custom_site import custom_site
from blogsite.base_admin import MyAdmin


class PostInline(admin.StackedInline):
    """内联编辑文章页"""
    model = Post
    fields = ['title', 'desc']
    extra = 1


@admin.register(Category, site=custom_site)
class CategoryAdmin(MyAdmin):
    list_display = ['name', 'status', 'is_nav', 'created_time', 'post_count']
    fields = ['name', 'status', 'is_nav']
    inlines = [PostInline]

    # 自定义字段
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数'


@admin.register(Tag, site=custom_site)
class TagAdmin(MyAdmin):
    list_display = ['name', 'status', 'created_time', 'post_count']
    fields = ['name', 'status']

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数'


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器: 只展示当前用户创建的分类过滤器"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()  # 返回查询参数
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(MyAdmin):
    form = PostAdminForm
    list_display = ['title', 'owner', 'category', 'status', 'created_time', 'operator', 'pv', 'uv']
    list_display_links = None
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    # filter_horizontal = ['tags']
    # fields = [('title', 'category'), 'desc', 'status', 'content', 'tags']
    fieldsets = [
        ('基础设置', {
            'description': '基础设置描述',
            'fields': [('title', 'category'), 'status'],
        }),
        ('额外信息', {
            # 'classes': ['collapse'],
            'fields': ['tags'],
        }),
        ('内容', {
            'fields': ['desc', 'content'],
        }),
    ]

    def operator(self, obj):
        # 自定义字段显示HTML
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('custom_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
