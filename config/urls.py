from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import ExploreView

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$',          'app.views.home', name='home'),
    url(r'^explore$',   ExploreView.as_view(), name='explore'),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^api/',       include('liang.modules.api.urls')),
    url(r'^p/',         include('liang.modules.articles.urls', namespace='articles')),
    url(r'^comments/',  include('liang.modules.comments.urls')),
    url(r'^accounts/',  include('liang.modules.accounts.urls')),
    url(r'^people/',    include('liang.modules.peoples.urls', namespace="people")),
    url(r'^auth/',      include('django.contrib.auth.urls')),
)
