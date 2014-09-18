# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^(?P<pk>\d+)$', views.PeopleDetail.as_view(), name='detail'),
)
