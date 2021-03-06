﻿from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^base-64/$', views.Content.as_view()),
    url(r'^multipart/$', views.ContentMultiPart.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
