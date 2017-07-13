from django.conf.urls import url

from services import views

urlpatterns = [
    url(
        r'^create-consult$',
        views.CreateConsultationView.as_view(),
        name='create-consult'
    ),
    url(
        r'^pay$',
        views.PayView.as_view(),
        name='pay'
    ),
    url(
        r'^cancel$',
        views.CancelPayView.as_view(),
        name='cancel-pay'
    ),
]
