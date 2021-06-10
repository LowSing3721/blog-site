"""定制用于admin的表单"""
from dal import autocomplete
from ckeditor.widgets import CKEditorWidget

from django import forms
from django.conf import settings

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        # 组件使用dal的自动查询组件
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类'
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        # 组件使用dal的自动查询组件
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签'
    )
    # 使用de的富文本编辑器组件
    if settings.USE_CK_EDITOR:
        content = forms.CharField(widget=CKEditorWidget, label='正文', required=True)

    # class Meta:
    #     model = Post
    #     fields = ['tags', 'category', 'title', 'desc', 'status', 'content']
