# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^create$', views.ArticleCreate.as_view(), name='article_create'),
    url(r'^(?P<book_id>\d+)/create$', views.ArticleCreate.as_view(), name='article_create_in_book'),
    url(r'^(?P<pk>\d+)$', views.ArticleView.as_view(), name='article_detail'),
    url(r'^(?P<pk>\d+)/update$', views.ArticleUpdate.as_view(), name='article_update'),

    url(r'^book/create$', views.BookCreate.as_view(), name='book_create'),
    url(r'^book/(?P<pk>\d+)$', views.BookView.as_view(), name='book_detail'),
    url(r'^book$', views.BookList.as_view(), name='book_list'),
)
