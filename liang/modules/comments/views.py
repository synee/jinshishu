# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View
from liang.base.kits import jsonify
from liang.modules.api.views import render_json
from liang.modules.comments import CustomComment as Comment


def render_comment(comment):
    res = comment.__dict__
    res.update({
        'user': comment.user,
    })
    return res


def render_comments(commnets):
    return [render_comment(comment) for comment in commnets]


class CommentView(View):
    def get(self, request, ct_pk, pk, offset=0, size=10):
        ct = ContentType.objects.get(pk=ct_pk)
        obj = ct.get_object_for_this_type(pk=pk)
        comments = Comment.objects.for_model(obj).all()[int(offset): int(size)]
        return render_json(render_comments(comments))

    def post(self, request, ct_pk, pk):
        ct = ContentType.objects.get(pk=ct_pk)
        obj = ct.get_object_for_this_type(pk=pk)
        comment = Comment()
        comment.comment = request.POST.get('comment')
        comment.content_type = ct
        comment.object_pk = obj.pk
        comment.user = request.user
        comment.site_id = 1
        comment.save()
        return render_json(render_comment(Comment.objects.get(pk=comment.pk)))