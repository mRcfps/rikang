from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(questioner=self.request.user.patient)


class QuestionDetailView(generics.RetrieveUpdateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionStarView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        question.stars += 1
        question.save()

        patient = Patient.objects.get(user=request.user)
        patient.starred_questions.add(question)
        patient.save()

        return Response({'id': int(pk), 'starred': True})


class AnswersListView(generics.ListAPIView):

    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(question__id=self.kwargs['pk'])


class NewAnswerView(generics.CreateAPIView):

    serializer_class = AnswerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.doctor)


class AnswersDetailView(generics.RetrieveUpdateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerUpvoteView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        answer = Answer.objects.get(id=pk)
        answer.upvotes += 1
        answer.save()

        return Response({'upvoted': True})
