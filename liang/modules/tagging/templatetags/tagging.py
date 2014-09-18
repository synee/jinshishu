# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import Node
from django.utils.html import format_html
from liang.modules.tagging.models import Tag

register = template.Library()


class NgTagbarNode(Node):
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
        tags = Tag.objects.get_for_object(content).all()[0:4]
        return format_html("<tagbar "
                           "data-content-type='{0}' "
                           "data-content-pk='{1}'"
                           "ng-init='tags={2}; newable=true; shownew=false'>"
                           "<i class='fa fa-tag'></i>  "
                           "<i class='fa fa-plus' ng-show='newable' ng-click='shownew=!shownew'> "
                           "</i> <input ng-model='newTag' ng-show='shownew' ng-keydown='addTag(newTag)' ng-blur='addBlur()'/></tagbar>",
                           ct.pk,
                           content.pk,
                           '[%s]' % ''.join([tag.name for tag in tags]))


@register.tag
def tagbar(parser, token):
    return NgTagbarNode.handle_token(parser=parser, token=token)

@register.tag
def ng_tagbar(parser, token):
    return NgTagbarNode.handle_token(parser=parser, token=token)
