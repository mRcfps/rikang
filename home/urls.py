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
        r'^hospitals/(?P<pk>\d+)/$',
        views.HospitalDetailView.as_view(),
        name='hospital-detail'
    ),
    url(
        r'doctors/$',
        views.DoctorListView.as_view(),
        name='doctor-list'
    ),
    url(
        r'doctors/(?P<pk>\d+)/$',
        views.DoctorDetailView.as_view(),
        name='doctor-detail'
    ),
    url(
        r'doctors/(?P<pk>\d+)/info/$',
        views.DoctorInfoView.as_view(),
        name='doctor-info'
    ),
    url(
        r'doctors/(?P<pk>\d+)/fav$',
        views.DoctorFavView.as_view(),
        name='doctor-fav'
    ),
    url(
        r'doctors/(?P<pk>\d+)/comments/$',
        views.DoctorCommentsView.as_view(),
        name='doctor-comments'
    ),
    url(
        r'doctors/(?P<pk>\d+)/comments/new$',
        views.DoctorNewCommentView.as_view(),
        name='doctor-new-comment'
    ),
]
