"""自定义ModelAdmin基类"""
from django.contrib.admin import ModelAdmin


class MyAdmin(ModelAdmin):
    # 编辑页面排除作者字段
    exclude = ['owner']

    def save_model(self, request, obj, form, change):
        """作者字段自动填充当前用户"""
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """只展示当前用户创建的分类"""
        return super().get_queryset(request).filter(owner=request.user)
