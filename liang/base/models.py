# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Manager
from liang.base.kits import jsonify


class BaseManager(models.Manager):
    def all(self):
        return self.filter().all()

    def filter(self, *args, **kwargs):
        kwargs.update({'enable': True})
        return super(BaseManager, self).filter(*args, **kwargs)


class BaseModel(models.Model):
    enable = models.BooleanField(default=True)

    objects = BaseManager()

    def delete(self, using=None):
        self.enable = False
        self.save(using=using, update_fields=['enable'])
        return True

    @property
    def dict(self):
        if hasattr(self, 'to_dict'):
            d = self.to_dict()
        else:
            d = self.__dict__
        return d

    def to_json(self):
        return jsonify(self.dict)

    class Meta:
        abstract = True