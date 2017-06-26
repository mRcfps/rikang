from rest_framework import generics

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


class AnswersUpdateView(generics.UpdateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
