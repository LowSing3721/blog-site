from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
import debug_toolbar

from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, include
from django.conf import settings

from .custom_site import custom_site
from .autocomplete import CategoryAutocomplete, TagAutocomplete
from blog import views
from blog import apis
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from config.views import LinkListView
from comment.views import CommentView


router = DefaultRouter()
router.register('post', apis.PostViewSet, basename='api-post')
router.register('cate', apis.CategoryViewSet, basename='api-cate')
router.register('tag', apis.TagViewSet, basename='api-tag')

urlpatterns = [
    # FBV
    # path('', post_list, name='index'),
    # path('category/<int:category_id>/', post_list, name='category-list'),
    # path('tag/<int:tag_id>/', post_list, name='tag-list'),
    # path('post/<int:post_id>/', post_detail, name='post-detail'),

    # CBV
    path('', views.PostListView.as_view(), name='index'),
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail'),
    path('category/<int:category_id>/', views.CategoryView.as_view(), name='category-list'),
    path('tag/<int:tag_id>/', views.TagView.as_view(), name='tag-list'),
    path('author/<int:author_id>/', views.AuthorView.as_view(), name='author-list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('links/', LinkListView.as_view(), name='links'),
    path('comment/', CommentView.as_view(), name='comment'),

    # RSS/Sitemap
    path('rss/', LatestPostFeed(), name='rss'),
    path('sitemap.xml/', sitemap_views.sitemap, {
        'sitemaps': {'posts': PostSitemap}
    }),

    # admin
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', custom_site.urls, name='super-admin'),

    # autocomplete
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),

    # drf api
    # path('api/post/', apis.post_list, name='post-list'),
    # path('api/post/', apis.PostList.as_view(), name='post-list'),
    # path('api/post/', apis.PostList.as_view(), name='post-list'),
    path('api/', include(router.urls)),
    path('post_by_category/<int:category_id>', apis.get_post_by_category),
    path('post_by_tag/<int:tag_id>', apis.get_post_by_tag),

    # coreapi
    path('api/docs/', include_docs_urls(title='Blogsite接口文档')),
]

# DEBUG开启时启用django-debug-toolbar
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
