from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^qa/', include('qa.urls', namespace='qa')),
    url(r'^admin/', admin.site.urls),
]
