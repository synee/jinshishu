# -*- coding: utf-8 -*-
import datetime
import json
import decimal
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import base as models_base
from django.http import HttpResponse
from django.utils.functional import SimpleLazyObject
from liang.base.decorator import time_spend


def _dumps_model(obj):
    res = obj.__dict__
    if hasattr(obj, 'dict'):
        return obj.dict
    for key, val in res.items():
        if isinstance(val, models.Model) or isinstance(val, SimpleLazyObject):
            res[key] = res.pop(key).__dict__
            for k, v in res[key].items():
                if isinstance(v, models.Model) or isinstance(v, SimpleLazyObject):
                    res[key].pop(k)
    return res


def _dumps_default(obj):
    if isinstance(obj, str) \
            or isinstance(obj, bool) \
            or isinstance(obj, int) \
            or isinstance(obj, float) \
            or isinstance(obj, long) \
            or isinstance(obj, unicode) \
            or isinstance(obj, list) \
            or isinstance(obj, tuple) \
            or isinstance(obj, dict):
        return obj

    if isinstance(obj, decimal.Decimal):
        return int(obj)

    if isinstance(obj, QuerySet):
        return list(obj)

    if isinstance(obj, models.Model) or isinstance(obj, SimpleLazyObject):
        return _dumps_model(obj)

    if isinstance(obj, models_base.ModelState):
        return obj.__dict__

    if isinstance(obj, datetime.datetime):
        return str(obj)

    return str(obj)


def jsonify(obj):
    return json.dumps(obj, default=_dumps_default)


def render_json(obj):
    return HttpResponse(jsonify(obj), content_type='application/json')

