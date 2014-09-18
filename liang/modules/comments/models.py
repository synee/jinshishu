# -*- coding: utf-8 -*-
from django.contrib.comments import Comment
from django.contrib.comments.managers import CommentManager
from django.db import models
from django.utils import timezone
from liang.modules.api.dataset import DatasetMixin
from liang.modules.comments.datasets import CommentDataset


class CustomComment(DatasetMixin, Comment):
    _dataset = CommentDataset

    date_updated = models.DateTimeField(default=lambda *args: timezone.now())

    objects = CommentManager()

    @classmethod
    def load_comments(cls, app, model, pk, offset=0, size=10):
        return

    @classmethod
    def post_comment(cls, app, model, pk, content):
        return