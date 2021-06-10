from django.template import Library

from comment.forms import CommentForm
from comment.models import Comment


register = Library()


@register.inclusion_tag('comment/block.html')
def show_comment(target):
    return {
        'target': target,
        'comment_form': CommentForm,
        'comment_list': Comment.get_by_target(target),
    }
