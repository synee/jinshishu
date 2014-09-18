# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',

    url(regex=r'^profile$',
        view=views.ProfileView.as_view(),
        name='accounts_profile'),

    url(regex=r'^setting$',
        view=views.SettingView.as_view(),
        name='accounts_setting'),

    url(regex=r'^setting/basic$',
        view=views.SettingBasicView.as_view(),
        name='accounts_setting_basic'),

    url(regex=r'^register$',
        view=views.RegisterView.as_view(),
        name='accounts_register'),
)