from django.conf.urls import url

from users import views

urlpatterns = [
    url(
        r'^register$',
        views.UserRegistrationView.as_view(),
        name='register'
    ),
    url(
        r'^login/$',
        views.UserLoginView.as_view(),
        name='login'
    ),
    url(
        r'change-password$',
        views.UserChangePasswordView.as_view(),
        name='change-password'
    ),
    url(
        r'request-sms-code$',
        views.RequestSmsCodeView.as_view(),
        name='request-sms-code'
    ),
    url(
        r'verify-sms-code$',
        views.VerifySmsCodeView.as_view(),
        name='verify-sms-code'
    ),
    url(
        r'^doctor/init$',
        views.DoctorInitView.as_view(),
        name='doctor-init'
    ),
    url(
        r'^doctor/profile/$',
        views.DoctorProfileView.as_view(),
        name='doctor-profile'
    ),
    url(
        r'^doctor/info/$',
        views.DoctorInfoView.as_view(),
        name='doctor-info'
    ),
    url(
        r'patient/profile/$',
        views.PatientProfileView.as_view(),
        name='patient-profile'
    ),
    url(
        r'patient/questions/$',
        views.PatientQuestionsView.as_view(),
        name='patient-questions'
    ),
    url(
        r'patient/starred-questions/$',
        views.PatientStarredQuestionsView.as_view(),
        name='patient-starred-questions'
    ),
    url(
        r'patient/fav-doctors/$',
        views.PatientFavDoctorsView.as_view(),
        name='patient-fav-doctors'
    ),
    url(
        r'patient/fav-posts/$',
        views.PatientFavPostsView.as_view(),
        name='patient-fav-posts'
    ),
]
