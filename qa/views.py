from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from qa.models import Question, Answer
from qa.serializers import QuestionSerializer, AnswerSerializer
from users.models import Patient


class QuestionListView(generics.ListAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class NewQuestionView(generics.CreateAPIView):

    queryset = Question.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(questioner=self.request.user.patient)


class QuestionDetailView(generics.RetrieveUpdateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionStarView(APIView):

    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(id=self.kwargs['pk'])
        question.stars += 1
        question.save()

        patient = Patient.objects.get(user=request.user)
        patient.starred_questions.add(question)
        patient.save()

        return Response({'starred': True})


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
