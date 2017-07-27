from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^qa/', include('qa.urls', namespace='qa')),
    url(r'^services/', include('services.urls', namespace='services')),
    url(r'^feedback/', include('feedback.urls', namespace='feedback')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
