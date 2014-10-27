from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from logcollector import views

urlpatterns = patterns('',
    url(r'^log/$', views.LogList.as_view()),
    url(r'^log/(?P<pk>\d+)/$', views.LogDetail.as_view()),
    url(r'^log/(?P<ts1>\d+)/(?P<ts2>\d+)/Max(?:/(?P<dim1>\d+))?(?:/(?P<dim2>\d+))?/$', views.LogMax.as_view()),
    url(r'^log/(?P<ts1>\d+)/(?P<ts2>\d+)/Min(?:/(?P<dim1>\d+))?(?:/(?P<dim2>\d+))?/$', views.LogMin.as_view()),
    url(r'^log/(?P<ts1>\d+)/(?P<ts2>\d+)/Avg(?:/(?P<dim1>\d+))?(?:/(?P<dim2>\d+))?/$', views.LogAvg.as_view()),
    url(r'^log/(?P<ts1>\d+)/(?P<ts2>\d+)/StdDev(?:/(?P<dim1>\d+))?(?:/(?P<dim2>\d+))?/$', views.LogStdDev.as_view()),
    url(r'^log/(?P<ts1>\d+)/(?P<ts2>\d+)/(?P<n>\d+)/MvgAvg(?:/(?P<dim1>\d+))?(?:/(?P<dim2>\d+))?/$', views.LogMvgAvg.as_view())
)

urlpatterns = format_suffix_patterns(urlpatterns)