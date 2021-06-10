from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from blog.models import Post


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]

    # 评论关联文章的三种方法:
    # 1. 外键关联文章类
    # target = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name='评论目标')
    # 2. 保存文章详情页的URL
    target = models.CharField(max_length=100, verbose_name='评论目标')
    # 3. 通用外键关联文章类(或任意类)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # target = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    content = models.CharField(max_length=2000, verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态'
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)
