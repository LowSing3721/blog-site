from datetime import date

from django.shortcuts import render, get_object_or_404
from django.db.models import ObjectDoesNotExist, Q, F
from django.views.generic import ListView, DetailView
from django.core.cache import cache
from django.http.response import HttpResponse

from .models import Post, Category, Tag
from config.models import SideBar


def post_list(request, category_id=None, tag_id=None):
    category = None
    tag = None
    # 避免ORM操作暴露在视图函数中
    if category_id:
        post_list, category = Post.get_by_category(category_id)
    elif tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'post_list': post_list,
        'category': category,
        'tag': tag,
        'sidebars': SideBar.get_all(),
    }
    # 增加置顶/非置顶分类context
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    # 增加置顶/非置顶分类context
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


class CommonViewMixin:
    """从多个视图类的公共操作提取出混入类"""

    def get_context_data(self, **kwargs):
        """更新context"""
        context = super().get_context_data(**kwargs)
        # 增加侧边栏
        context.update({
            'sidebars': SideBar.get_all(),
        })
        # 增加置顶/非置顶分类
        context.update(Category.get_navs())
        return context


class PostDetailView(CommonViewMixin, DetailView):
    """文章详情"""
    model = Post
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        is_new_pv = False
        is_new_uv = False
        # 从请求中获取UID
        uid = request.uid
        pv_key = f'pv:{uid}:{request.path}'
        uv_key = f'uv:{uid}:{str(date.today())}:{request.path}'
        # 缓存不存在则新增缓存
        if not cache.get(pv_key):
            is_new_pv = True
            cache.set(pv_key, 1, timeout=60)
        if not cache.get(uv_key):
            is_new_uv = True
            cache.set(uv_key, 1, timeout=60 * 60 * 24)
        # 避免产生多次查询
        if is_new_pv and is_new_uv:
            Post.objects.filter(pk=self.kwargs.get('post_id')).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif is_new_pv:
            Post.objects.filter(pk=self.kwargs.get('post_id')).update(pv=F('pv') + 1)
        elif is_new_uv:
            Post.objects.filter(pk=self.kwargs.get('post_id')).update(uv=F('uv') + 1)

        response = super().get(request, *args, **kwargs)
        return response


class PostListView(CommonViewMixin, ListView):
    """文章列表"""
    model = Post
    queryset = Post.latest_posts()
    template_name = 'blog/list.html'
    context_object_name = 'post_list'
    paginate_by = 1


class CategoryView(PostListView):
    """(由)分类(过滤文章)列表"""

    def get_queryset(self):
        """过滤object_list"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category=category_id)

    def get_context_data(self, **kwargs):
        """更新context"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context


class TagView(PostListView):
    """标签列表"""

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tags=tag_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context


class SearchView(PostListView):
    """搜索列表"""

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__contains=keyword) | Q(desc__contains=keyword))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        context.update({
            'keyword': keyword
        })
        return context


class AuthorView(PostListView):
    """作者列表"""

    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('author_id')
        return queryset.filter(owner=author_id)
