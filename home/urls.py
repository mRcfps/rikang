from django.conf.urls import url

from home import views

urlpatterns = [
    url(
        r'^posts/$',
        views.PostListView.as_view(),
        name='post-list'
    ),
    url(
        r'^posts/(?P<pk>\d+)/$',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),
    url(
        r'^hospitals/$',
        views.HospitalListView.as_view(),
        name='hospital-list'
    ),
    url(
        r'^hospitals/$',
        views.HospitalDetailView.as_view(),
        name='hospital-detail'
    ),
]
