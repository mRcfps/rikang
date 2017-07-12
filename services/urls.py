from django.conf.urls import url

from services import views

urlpatterns = [
    url(
        r'^create-consult$',
        views.CreateConsultationView.as_view(),
        name='create-consult'
    ),
]
