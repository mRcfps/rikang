from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from qa.models import Question, Answer, QuestionImage
from qa.serializers import QuestionSerializer, AnswerSerializer, QuestionImageSerializer
from users.models import Patient


class QuestionListView(generics.ListAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class NewQuestionView(generics.CreateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(questioner=self.request.user.patient)


class QuestionAddImageView(generics.CreateAPIView):

    queryset = QuestionImage.objects.all()
    serializer_class = QuestionImageSerializer

    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs['pk'])
        serializer.save(question=question)


class QuestionDetailView(generics.RetrieveUpdateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionImageListView(generics.ListAPIView):

    serializer_class = QuestionImageSerializer
    pagination_class = None

    def get_queryset(self):
        question = Question.objects.get(id=self.kwargs['pk'])
        return question.images.all()


class QuestionStarView(APIView):

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.doctor)


class AnswersDetailView(generics.RetrieveUpdateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerUpvoteView(APIView):

    def get(self, request, pk):
        answer = Answer.objects.get(id=pk)
        answer.upvotes += 1
        answer.save()

        return Response({'id': int(pk), 'upvoted': True})
