from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from logcollector import views

urlpatterns = patterns('',
    url(r'^log/', views.LogFun.as_view(), name='log'),
)

urlpatterns = format_suffix_patterns(urlpatterns)