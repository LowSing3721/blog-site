from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]

    title = models.CharField(max_length=50, verbose_name='标题')
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态'
    )
    weight = models.PositiveIntegerField(
        default=1, choices=zip(range(1, 6), range(1, 6)), verbose_name='权重'
    )
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '友链'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = [
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    ]
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = [
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    ]
    title = models.CharField(max_length=50, verbose_name='标题')
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name='展示类型')
    content = models.CharField(
        max_length=500, blank=True, verbose_name='内容',
        help_text='如果展示的不是HTML类型, 可为空'
    )
    status = models.PositiveIntegerField(
        default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name='状态'
    )
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '侧边栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        """根据不同展示类型返回不同结果"""
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.latest_posts(with_related=False)
            }
            # 获取经过渲染的HTML文本
            result = render_to_string('config/block/sidebar_posts.html', context=context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.hot_posts()
            }
            result = render_to_string('config/block/sidebar_posts.html', context=context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            result = render_to_string('config/block/sidebar_comments.html', context=context)
        return result
