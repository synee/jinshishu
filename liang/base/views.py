# -*- coding: utf-8 -*-
import functools
from django import http
from django.views.generic import View
from liang.base.decorator import prep_params
from liang.base.kits import render_json


class ApiView(View):
    prefix = 'action'

    @prep_params(page_index=0, page_size=10)
    def dispatch(self, request, action=None, page_index=0, page_size=10, *args, **kwargs):
        action_name = "%s_%s" % (self.prefix, action)
        if hasattr(self, action_name):
            return render_json(getattr(self, action_name)(request,
                                                          page_index=int(page_index),
                                                          page_size=int(page_size), *args, **kwargs))
        else:
            return http.HttpResponseNotFound()