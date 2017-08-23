﻿from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^use-serializer/$', views.UseSerializer.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
