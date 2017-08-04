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
        r'^accept-order$',
        views.AcceptOrderView.as_view(),
        name='accept-order'
    ),
    url(
        r'^finish-order$',
        views.FinishOrderView.as_view(),
        name='finish-order'
    ),
    url(
        r'^comment$',
        views.CommentView.as_view(),
        name='comment'
    ),
    url(
        r'^refund$',
        views.RefundView.as_view(),
        name='refund'
    ),
    url(
        r'^webhooks$',
        views.WebhooksView.as_view(),
        name='webhooks'
    ),
    url(
        r'^test-ip/$',
        views.TestIPView.as_view(),
        name='test-ip'
    ),
]
