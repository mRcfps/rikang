from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^register/$',
        views.UserRegistrationView.as_view(),
        name='register'
    ),
    url(
        r'^login/$',
        views.UserLoginView.as_view(),
        name='login'
    ),
    url(
        r'^doctor-init/$',
        views.DoctorInitView.as_view(),
        name='doctor-init'
    ),
    url(
        r'^patient-init/$',
        views.PatientInitView.as_view(),
        name='patient-init'
    ),
]
