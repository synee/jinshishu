# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models


class VisitCount(models.Model):
    content_type = models.ForeignKey(to="contenttypes.ContentType", verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')
    visit_count = models.IntegerField()
    last_visit = models.ForeignKey(to='VisitObject')
    last_user = models.ForeignKey(to="contenttypes.ContentType")
    last_datetime = models.DateTimeField(default=lambda *args: timezone.now())


class VisitObject(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL)
    content_type = models.ForeignKey(to="contenttypes.ContentType", verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')
    datetime = models.DateTimeField(default=lambda *args: timezone.now())

    @classmethod
    def visit(cls, user, obj):
        return

    class Meta:
        db_table = "analysis_visit_object"