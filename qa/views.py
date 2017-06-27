from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer


class QuestionListView(generics.ListCreateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetailView(generics.RetrieveUpdateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswersListView(generics.ListCreateAPIView):

    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(question__id=self.kwargs['pk'])


class AnswersDetailView(generics.RetrieveUpdateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerUpvoteView(APIView):

    def get(self, request):
        answer = Answer.objects.get(id=self.kwargs['pk'])
        answer.upvotes += 1
        answer.save()

        return Response({'upvoted': True})
