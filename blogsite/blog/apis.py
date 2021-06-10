"""drf接口"""
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import Post, Category, Tag
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, TagSerializer


@api_view(['GET'])
def post_list(request):
    posts = Post.latest_posts()
    ps = PostSerializer(posts, many=True)
    return Response(ps.data)


class PostList(ListCreateAPIView):
    queryset = Post.latest_posts()
    serializer_class = PostSerializer


class PostViewSet(ReadOnlyModelViewSet):
    """
    list: 最新文章列表
    retrieve: 查询单个文章
    gbc: 根据分类查询文章
    """
    queryset = Post.latest_posts()
    # serializer_class = PostSerializer
    # permission_classes = ['']

    def get_serializer_class(self):
        """根据不同行为指定序列化器"""
        if self.action == 'list':
            return PostSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer

    # def filter_queryset(self, queryset):
    #     """对查询集进行过滤"""
    #     category_id = self.request.query_params.get('category')
    #     if category_id:
    #         queryset = queryset.filter(category=int(category_id))
    #     tag_id = self.request.query_params.get('tag')
    #     if tag_id:
    #         queryset = queryset.filter(tags=int(tag_id))
    #     return queryset

    # @action(detail=False, url_path='gbc', url_name='get_cat')
    # def get_by_category(self, request, category_id):
    #     print(category_id)
    #     queryset = Post.latest_posts()
    #     serializer = PostSerializer(queryset, many=True)
    #     return Response(serializer.data)


@api_view(http_method_names=['GET'])
def get_post_by_category(request, category_id):
    """根据分类查询文章"""
    queryset = Post.objects.filter(category=category_id)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def get_post_by_tag(request, tag_id):
    """根据标签查询文章"""
    queryset = Post.objects.filter(tags=tag_id)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)


class CategoryViewSet(ListModelMixin, GenericViewSet):
    """
    list: 分类列表
    """
    queryset = Category.get_all()
    serializer_class = CategorySerializer


class TagViewSet(ListModelMixin, GenericViewSet):
    """
    list: 标签列表
    """
    queryset = Tag.get_all()
    serializer_class = TagSerializer
