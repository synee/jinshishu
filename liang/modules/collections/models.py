# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db import models


class CollectionManager(models.Manager):
    def get_for_object(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        return Collection.objects.filter(content_type=ct.pk,
                                         object_id=obj.pk)


class Collection(models.Model):
    user = models.ForeignKey(to='accounts.User', related_name='collection')
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')

    objects = CollectionManager()

    class Meta:
        unique_together = (('user', 'content_type', 'object_id'),)