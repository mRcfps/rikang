from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^questions/$',
        views.QuestionListView.as_view(),
        name='question-list'
    ),
    url(
        r'^questions/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(),
        name='question-detail'
    ),
    url(
        r'questions/(?P<pk>\d+)/answers/$',
        views.AnswersListView.as_view(),
        name='answer-list'
    ),
    url(
        r'answers/(?P<pk>\d+)/$',
        views.AnswersUpdateView.as_view(),
        name='answer-update'
    ),
]
