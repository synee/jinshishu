from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns(
    '',
    url(regex=r'^session$',
        view=views.session_call,
        name='api_session_call'),

    url(regex=r'^success_call$',
        view=views.success_call,
        name='api_success_call'),

    url(regex=r'^view_call$',
        view=views.view_call,
        name='api_view_call'),

    # url(regex=r'^dataset/(?P<app>\S+).(?P<model>\S+)/(?P<pk>\d+)/(?P<method>\S+)$',
    #     view=views.DatasetView.as_view(),
    #     name='dataset'),

    url(regex=r'^model_call/(?P<contenttype_id>\d+)/(?P<action>\S+)$',
        view=views.ModelCall.as_view(),
        name='api_model_call'),

    url(regex=r'^recordCall/(?P<contenttype_id>\d+)-(?P<model_id>\d+)/(?P<action>\S+)$',
        view=views.RecordCall.as_view(),
        name='api_record_call'),

    url(regex=r'^fieldCall/(?P<contenttype_id>\d+)-(?P<model_id>\d+)/(?P<field>\S+)$',
        view=views.FieldCall.as_view(),
        name='api_field_call')
)
