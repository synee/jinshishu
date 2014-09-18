# -*- coding: utf-8 -*-
from django.contrib.auth import decorators as auth_decorators
from django.contrib.comments.urls import *
from . import views


urlpatterns += patterns(
    '',
    url(regex=r'^(?P<ct_pk>\d+)/(?P<pk>\S+)/(?P<offset>\d+)-(?P<size>\d+)$',
        view=views.CommentView.as_view(),
        name='comments-page'),

    url(regex=r'^(?P<ct_pk>\d+)/(?P<pk>\S+)$',
        view=views.CommentView.as_view(),
        name='comments-post'),
)