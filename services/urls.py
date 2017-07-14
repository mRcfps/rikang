from django.conf.urls import url

from services import views

urlpatterns = [
    url(
        r'^new-order$',
        views.NewOrderView.as_view(),
        name='new-order'
    ),
    url(
        r'^pay$',
        views.PayView.as_view(),
        name='pay'
    ),
    url(
        r'^cancel$',
        views.CancelView.as_view(),
        name='cancel'
    ),
    url(
        r'^refund$',
        views.RefundView.as_view(),
        name='refund'
    ),
]
