import mistune

from django.db import models
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态'
    )
    is_nav = models.BooleanField(default=False, verbose_name='是否置顶导航')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        """获取置顶/普通分类"""
        nav_categories = []
        normal_categories = []
        for category in cls.objects.filter(status=cls.STATUS_NORMAL):
            if category.is_nav:
                nav_categories.append(category)
            else:
                normal_categories.append(category)
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态'
    )
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    ]

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为Markdown格式')
    content_html = models.TextField(verbose_name='HTML格式正文', editable=False, blank=True)
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态'
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1, verbose_name='访问量')
    uv = models.PositiveIntegerField(default=1, verbose_name='访问者')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.desc:
            self.desc = self.content[:20]
        if settings.USE_CK_EDITOR:
            self.content_html = self.content
        else:
            self.content_html = mistune.markdown(self.content)
        super().save(**kwargs)

    @staticmethod
    def get_by_category(category_id):
        """按分类过滤文章"""
        category = None
        try:
            category = Category.objects.get(pk=category_id)
        except ObjectDoesNotExist:
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('category')
        return post_list, category

    @staticmethod
    def get_by_tag(tag_id):
        """按标签过滤文章"""
        tag = None
        try:
            tag = Tag.objects.get(pk=tag_id)
        except ObjectDoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).prefetch_related('tags')
        return post_list, tag

    @classmethod
    def latest_posts(cls, with_related=True):
        """最新文章列表"""
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('category', 'owner')
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
