"""drf序列化器"""
from rest_framework import serializers

from .models import Post, Category, Tag


class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tags', 'owner', 'created_time']


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tags', 'owner', 'content_html', 'created_time']


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Category
        fields = ['id', 'name', 'owner', 'status']


class TagSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'owner', 'status', 'created_time']
