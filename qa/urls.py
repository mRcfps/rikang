from django.conf.urls import url

from qa import views

urlpatterns = [
    # `GET` /qa/questions/
    url(
        r'^questions/$',
        views.QuestionListView.as_view(),
        name='question-list'
    ),

    # `POST` /qa/questions/new
    url(
        r'^questions/new$',
        views.NewQuestionView.as_view(),
        name='new-question'
    ),

    # `POST` /qa/questions/{question_id}/addimg
    url(
        r'^questions/(?P<pk>\d+)/addimg$',
        views.QuestionAddImageView.as_view(),
        name='question-add-image'
    ),

    # `GET` /qa/questions/{question_id}/images/
    url(
        r'^questions/(?P<pk>\d+)/images/$',
        views.QuestionImageListView.as_view(),
        name='question-image-list'
    ),

    # `GET``PUT` /qa/questions/{question_id}/
    url(
        r'^questions/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(),
        name='question-detail'
    ),

    # `GET` /qa/questions/{question_id}/star
    url(
        r'^questions/(?P<pk>\d+)/star$',
        views.QuestionStarView.as_view(),
        name='star-question'
    ),

    # `GET` /qa/questions/{question_id}/answers/
    url(
        r'^questions/(?P<pk>\d+)/answers/$',
        views.AnswersListView.as_view(),
        name='answer-list'
    ),

    # `POST` /qa/questions/{question_id}/pick-answer
    url(
        r'^questions/(?P<pk>\d+)/pick-answer$',
        views.PickAnswerView.as_view(),
        name='pick-answer'
    ),

    # `POST` /qa/questions/{question_id}/answers/new
    url(
        r'^questions/(?P<pk>\d+)/answers/new$',
        views.NewAnswerView.as_view(),
        name='new-answer'
    ),

    # `GET``PUT` /qa/answers/{answer_id}/
    url(
        r'^answers/(?P<pk>\d+)/$',
        views.AnswersDetailView.as_view(),
        name='answer-detail'
    ),

    # `GET` /qa/answers/{answer_id}/upvote
    url(
        r'^answers/(?P<pk>\d+)/upvote$',
        views.AnswerUpvoteView.as_view(),
        name='answer-upvote'
    ),

    # `GET` /qa/answers/{answer_id}/comments/
    url(
        r'^answers/(?P<pk>\d+)/comments/$',
        views.AnswerCommentsView.as_view(),
        name='answer-comments'
    ),

    # `POST` /qa/answers/{answer_id}/comments/new
    url(
        r'^answers/(?P<pk>\d+)/comments/new$',
        views.AnswerNewCommentView.as_view(),
        name='answer-new-comment'
    ),
]
