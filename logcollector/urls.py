from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from logcollector import views

urlpatterns = patterns('',
    url(r'^log/', views.LogFun.as_view()),
#    url(r'^log/listall/$', views.LogList.as_view()),
#    url(r'^log/(?P<pk>\d+)/$', views.LogDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)