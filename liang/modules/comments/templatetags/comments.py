# -*- coding: utf-8 -*-

from django.contrib.comments.templatetags.comments import *
from django.core import urlresolvers
from django.template import Node
from django.utils.html import format_html


class CommentsNode(Node):
    def __init__(self, object_name):
        self.object_name = object_name


    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse get_comment_list/count/form and return a Node."""
        tokens = token.split_contents()
        return cls(object_name=tokens[1])

    def render(self, context):
        content = context.get(self.object_name)
        ct = ContentType.objects.get_for_model(content)
        return format_html("<comments "
                           "data-content-type='{0}' "
                           "data-content-pk='{1}'/>",
                           ct.pk,
                           content.pk)
        # return super(CommentsNode, self).render(context)


@register.tag
def render_comments_tag(parser, token):
    return CommentsNode.handle_token(parser=parser, token=token)

@register.filter(name='comments_link')
def comments_link(obj):
    ct = ContentType.objects.get_for_model(obj)
    return "/comments/%s.%s/%s" % (ct.app_label, ct.model, str(obj.pk))