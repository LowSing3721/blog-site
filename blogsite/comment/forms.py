import mistune

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']
        widgets = {
            'nickname': forms.TextInput(
                attrs={'class': 'form-control', 'style': "width: 60%;"}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'style': "width: 60%;"}
            ),
            'website': forms.URLInput(
                attrs={'class': 'form-control', 'style': "width: 60%;"}
            ),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 6, 'cols': 60}
            ),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('评论长度不能小于10')
        return mistune.markdown(content)
