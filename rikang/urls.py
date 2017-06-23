from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^home/', include('home.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', admin.site.urls),
]
