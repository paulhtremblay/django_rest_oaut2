from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('henry.urls')),
    url(r'^login/$', login),
    url(r'^accounts/login/$', login),
    url('^', include('django.contrib.auth.urls')),
    url(r'^o/', include('my_oauth2.urls', namespace='myoauth2_provider')),
    url(r'^custom/', include('custom.urls', namespace='custom')),
    url(r'^contents/', include('contents.urls', namespace='contents')),
]
