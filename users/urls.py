from django.conf.urls import url

from users import views

urlpatterns = [
    # `POST` /users/register
    url(
        r'^register$',
        views.UserRegistrationView.as_view(),
        name='register'
    ),

    # `POST` /users/login/
    url(
        r'^login/$',
        views.UserLoginView.as_view(),
        name='login'
    ),

    # `PUT` /users/change-password
    url(
        r'^change-password$',
        views.UserChangePasswordView.as_view(),
        name='change-password'
    ),

    # `POST` /users/request-sms-code
    url(
        r'^request-sms-code$',
        views.RequestSmsCodeView.as_view(),
        name='request-sms-code'
    ),

    # `POST` /users/verify-sms-code
    url(
        r'^verify-sms-code$',
        views.VerifySmsCodeView.as_view(),
        name='verify-sms-code'
    ),

    # `POST` /users/doctor/init
    url(
        r'^doctor/init$',
        views.DoctorInitView.as_view(),
        name='doctor-init'
    ),

    # `GET``PUT` /users/doctor/profile/
    url(
        r'^doctor/profile/$',
        views.DoctorProfileView.as_view(),
        name='doctor-profile'
    ),

    # `GET``PUT` /users/doctor/info/
    url(
        r'^doctor/info/$',
        views.DoctorInfoView.as_view(),
        name='doctor-info'
    ),

    # `GET``PUT` /users/patient/profile/
    url(
        r'^patient/profile/$',
        views.PatientProfileView.as_view(),
        name='patient-profile'
    ),

    # `GET` /users/patient/questions/
    url(
        r'^patient/questions/$',
        views.PatientQuestionsView.as_view(),
        name='patient-questions'
    ),

    # `GET` /users/patient/starred-questions/
    url(
        r'^patient/starred-questions/$',
        views.PatientStarredQuestionsView.as_view(),
        name='patient-starred-questions'
    ),

    # `GET` /users/patient/fav-doctors/
    url(
        r'^patient/fav-doctors/$',
        views.PatientFavDoctorsView.as_view(),
        name='patient-fav-doctors'
    ),

    # `GET` /users/patient/fav-posts/
    url(
        r'^patient/fav-posts/$',
        views.PatientFavPostsView.as_view(),
        name='patient-fav-posts'
    ),
]
