# -*- coding: utf-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags import humanize
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models.fields import related as fields_related
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.decorators import http as http_decorators
from django.views.generic import View

from liang.base.decorator import prep_params, time_spend
from liang.base.kits import jsonify
from liang.base.views import ApiView
from liang.modules.accounts.models import User


def render_json(obj):
    return HttpResponse(jsonify(obj), content_type='application/json')


@http_decorators.require_GET
def view_call(request, **kwargs):
    """
    借口调用规则
    @:param template - template path in server
    @:param models - models typed by list that call as args
        <code type='javascript'>
        this.viewCall('tribe/notification/notification_list.html', [
            {
                name: "notifications",
                model: this.model.getModelId(),
                fnct: {
                    name: 'updated_notifications',
                    kwargs: {
                        page: this.page,
                        size: 20
                    }
                }
            }
        ])
        </code>
    :param request:
    :param kwargs:
    :return:
    """
    models_json = json.loads(request.GET.get('models'))
    data = {}
    for model_json in models_json:
        ct = ContentType.objects.get(pk=model_json['model']['content_id'])
        model = ct.get_object_for_this_type(pk=model_json['model']['model_id'])
        if model_json.has_key("fnct") and model_json['fnct'].has_key('name') and hasattr(model, model_json['fnct'][
            'name']):  # if exists function
            fnct = getattr(model, model_json['fnct']['name'])
            margs = model_json['fnct'].get("args") or []
            mkwargs = model_json['fnct'].get("kwargs") or {}
            data[model_json['name']] = fnct(*margs, **mkwargs)
        else:
            data[model_json['name']] = model

    try:
        return render(request, request.GET.get("template"), data)
    except TemplateDoesNotExist as e:
        raise


class ModelCall(View):
    def get(self, request, contenttype_id, action, **kwargs):
        kwargs.update(request.GET)
        return self.call_function(request, contenttype_id, action, **kwargs)

    def post(self, request, contenttype_id, action, **kwargs):
        kwargs.update(dict(request.GET))
        kwargs.update(dict(request.POST))
        return self.call_function(request, contenttype_id, action, **kwargs)

    def call_function(self, request, contenttype_id, action, **kwargs):
        """
        调用某model的某方法
        :param request:
        :param contenttype_id:
        :param action:
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            if not str(k).endswith('[]') and isinstance(v, list) and len(v) == 1:
                kwargs[k] = v[0]
        contenttype = ContentType.objects.get(pk=contenttype_id)
        try:
            model = contenttype.model_class()()
            if hasattr(model, "web_%s" % action):
                resp = render_json(getattr(model, "web_%s" % action)(request=request, **kwargs))
            else:
                resp = HttpResponseNotFound()
        except contenttype.model_class().DoesNotExist:
            resp = HttpResponseNotFound()
        return resp


class RecordCall(View):
    def get(self, request, contenttype_id, action, model_id, **kwargs):
        kwargs.update(request.GET)
        return self.call_function(request, contenttype_id, action, model_id, **kwargs)

    def post(self, request, contenttype_id, action, model_id, **kwargs):
        kwargs.update(dict(request.GET))
        kwargs.update(dict(request.POST))
        return self.call_function(request, contenttype_id, action, model_id, **kwargs)

    def call_function(self, request, contenttype_id, action, model_id, **kwargs):
        """
        调用某model的某方法
        :param request:
        :param contenttype_id: model 类型
        :param action: 在获取的model的调用方法
        :param model_id: model的id
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            if not str(k).endswith('[]') and isinstance(v, list) and len(v) == 1:
                kwargs[k] = v[0]
        contenttype = ContentType.objects.get(pk=contenttype_id)
        try:
            model = contenttype.get_object_for_this_type(pk=model_id)
            if hasattr(model, "web_%s" % action):
                resp = render_json(getattr(model, "web_%s" % action)(request=request, **kwargs))
            else:
                resp = HttpResponseNotFound()
        except contenttype.model_class().DoesNotExist:
            resp = HttpResponseNotFound()
        return resp


class FieldCall(View):
    def get_field_type(self, model_class, field_name):
        """
        获取字段类型
        :param model_class:
        :param field_name:
        :return:
        """
        field_descriptor = getattr(model_class, field_name)
        if hasattr(field_descriptor, 'field'):
            return type(field_descriptor.field)
        else:
            related_field_type = field_descriptor.related.field

            if isinstance(related_field_type, fields_related.OneToOneField):
                return fields_related.OneToOneRel

            if isinstance(related_field_type, fields_related.ForeignKey):
                return fields_related.ManyToOneRel

            if isinstance(related_field_type, fields_related.ManyToManyField):
                return fields_related.ManyToManyRel

    def get_field_value(self, model_class, model, field_name, filter=None, limit=(0, 50), **kwargs):
        """
        获取字段值
        :param model_class:
        :param model:
        :param field_name:
        :param filter:
        :param limit:
        :param kwargs:
        :return: @field_name value
        """
        field_type = self.get_field_type(model_class, field_name)
        if field_type in [fields_related.ManyToManyField, fields_related.ManyToOneRel, fields_related.ManyToManyRel]:
            return getattr(model, field_name).all()
        elif field_type in [fields_related.OneToOneField, fields_related.OneToOneRel, fields_related.ForeignKey]:
            return getattr(model, field_name)
        else:
            return getattr(model, field_name)

    def get(self, request, contenttype_id, model_id, field, **kwargs):
        """
        请求 GET
        :param request:
        :param contenttype_id:
        :param model_id:
        :param field:
        :param kwargs:
        :return:
        """
        contenttype = ContentType.objects.get(pk=contenttype_id)
        try:
            model = contenttype.get_object_for_this_type(pk=model_id)  # 获取对象
            if hasattr(contenttype.model_class(), field):
                resp_data = dict()
                resp_data[field] = self.get_field_value(contenttype.model_class(), model, field, **request.GET)
                resp = render_json(resp_data)
            else:
                resp = HttpResponseNotFound()
        except contenttype.model_class().DoesNotExist:
            resp = HttpResponseNotFound()
        return resp


def session_call(request, *args, **kwargs):
    return render_json({
        'contenttypes': ContentType.objects.all()
    })


def success_call(request, *args, **kwargs):
    return render_json({
        'success': True
    })


class SearchApiView(ApiView):
    prefix = 'search'

    @prep_params(q='')
    def search_book(self, request, q, page_index, page_size, *args, **kwargs):
        from ..articles.models import Book

        return Book.search(q=q)[page_index * page_size: page_index * page_size + page_size]

    @prep_params(q='')
    @time_spend
    def search_article(self, request, q, page_index, page_size, *args, **kwargs):
        from ..articles.models import Article

        articles = Article.objects.raw("""SELECT a.*, u.nickname as author_name, b.name as book_name
                                          FROM articles_article as a, auth_user as u, articles_book as b
                                          WHERE a.author_id=u.id AND a.book_id=b.id
                                                                 AND a.enable=1
                                                                 AND a.title LIKE '%%%s%%'
                                          ORDER BY date_updated DESC
                                      """ % q)[page_index * page_size: page_index * page_size + page_size]
        article_list = []
        for article in articles:
            d = article.__dict__
            d.update({
                'author': {
                    'id': d['author_id']
                },
                'book': {
                    'id': d['book_id'],
                    'name': d['book_name']
                },
                'date_created': humanize.naturaltime(d['date_created']),
                'date_updated': humanize.naturaltime(d['date_updated']),
            })
            article_list.append(d)
        return article_list

    @prep_params(q='')
    def search_author(self, request, q, page_index, page_size, *args, **kwargs):
        authors = User.objects.filter(Q(nickname__contains=q) | Q(username__contains=q))[
                  page_index * page_size: page_index * page_size + page_size]
        return authors