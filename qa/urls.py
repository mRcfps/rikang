from django.conf.urls import url

from qa import views

urlpatterns = [
    url(
        r'^questions/$',
        views.QuestionListView.as_view(),
        name='question-list'
    ),
    url(
        r'^questions/new$',
        views.QuestionListView.as_view(),
        name='new-question'
    ),
    url(
        r'^questions/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(),
        name='question-detail'
    ),
    url(
        r'^questions/(?P<pk>\d+)/star$',
        views.QuestionStarView.as_view(),
        name='star-question'
    ),
    url(
        r'questions/(?P<pk>\d+)/answers/$',
        views.AnswersListView.as_view(),
        name='answer-list'
    ),
    url(
        r'answers/(?P<pk>\d+)/$',
        views.AnswersDetailView.as_view(),
        name='answer-detail'
    ),
    url(
        r'answers/(?P<pk>\d+)/upvote$',
        views.AnswerUpvoteView.as_view(),
        name='answer-upvote'
    ),
]
