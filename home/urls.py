from django.conf.urls import url

from home import views

urlpatterns = [
    # `GET` /home/posts/
    url(
        r'^posts/$',
        views.PostListView.as_view(),
        name='post-list'
    ),

    # `GET` /home/posts/{post_id}/
    url(
        r'^posts/(?P<pk>\d+)/$',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),

    # `GET` /home/posts/{post_id}/fav
    url(
        r'^posts/(?P<pk>\d+)/fav$',
        views.PostFavView.as_view(),
        name='post-fav'
    ),

    # `GET` /home/posts/{post_id}/unfav
    url(
        r'^posts/(?P<pk>\d+)/unfav$',
        views.PostUnfavView.as_view(),
        name='post-unfav'
    ),

    # `GET` /home/hospitals/
    url(
        r'^hospitals/$',
        views.HospitalListView.as_view(),
        name='hospital-list'
    ),

    # `GET` /home/hospitals/{hospital_id}/
    url(
        r'^hospitals/(?P<pk>\d+)/$',
        views.HospitalDetailView.as_view(),
        name='hospital-detail'
    ),

    # `GET` /home/hospitals/{hospital_id}/doctors/
    url(
        r'^hospitals/(?P<pk>\d+)/doctors/$',
        views.HospitalDoctorsView.as_view(),
        name='hospital-doctors'
    ),

    # `GET` /home/doctors/
    url(
        r'^doctors/$',
        views.DoctorListView.as_view(),
        name='doctor-list'
    ),

    # `GET` /home/doctors/{doctor_id}/
    url(
        r'^doctors/(?P<pk>\d+)/$',
        views.DoctorDetailView.as_view(),
        name='doctor-detail'
    ),

    # `GET` /home/doctors/{doctor_id}/info/
    url(
        r'^doctors/(?P<pk>\d+)/info/$',
        views.DoctorInfoView.as_view(),
        name='doctor-info'
    ),

    # `GET` /home/doctors/{doctor_id}/fav
    url(
        r'^doctors/(?P<pk>\d+)/fav$',
        views.DoctorFavView.as_view(),
        name='doctor-fav'
    ),

    # `GET` /home/doctors/{doctor_id}/unfav
    url(
        r'^doctors/(?P<pk>\d+)/unfav$',
        views.DoctorUnfavView.as_view(),
        name='doctor-unfav'
    ),

    # `GET` /home/doctors/{doctor_id}/answers/
    url(
        r'^doctors/(?P<pk>\d+)/answers/$',
        views.DoctorAnswersView.as_view(),
        name='doctor-answers'
    ),

    # `GET` /home/doctors/{doctor_id}/comments/
    url(
        r'^doctors/(?P<pk>\d+)/comments/$',
        views.DoctorCommentsView.as_view(),
        name='doctor-comments'
    ),

    # `POST` /home/doctors/{doctor_id}/comments/new
    url(
        r'^doctors/(?P<pk>\d+)/comments/new$',
        views.DoctorNewCommentView.as_view(),
        name='doctor-new-comment'
    ),
]
