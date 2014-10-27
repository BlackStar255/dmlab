from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from logcollector import views

urlpatterns = patterns('',
    url(r'^logcollector/$', views.LogcollectorList.as_view()),
    url(r'^logcollector/(?P<pk>\d+)/$', views.LogcollectorDetail.as_view()),
    url(r'^logcollector/(?P<pk1>\d+)/(?P<pk2>\d+)/Max/$', views.LogcollectorMax.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)