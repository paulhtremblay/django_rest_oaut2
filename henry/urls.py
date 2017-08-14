from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from henry import views

urlpatterns = [
    url(r'^henry/$', views.DobList.as_view()),
    url(r'^henry/(?P<pk>[0-9]+)/$', views.DobDetails.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
