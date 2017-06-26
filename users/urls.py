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
        r'change-password/$',
        views.UserChangePasswordView.as_view(),
        name='change-password'
    ),
    url(
        r'^doctor-init$',
        views.DoctorInitView.as_view(),
        name='doctor-init'
    ),
    url(
        r'^doctor-profile/$',
        views.DoctorProfileView.as_view(),
        name='doctor-profile'
    ),
    url(
        r'^info/$',
        views.DoctorInfoView.as_view(),
        name='doctor-info'
    ),
    url(
        r'patient-profile/$',
        views.PatientProfileView.as_view(),
        name='patient-profile'
    ),
]
