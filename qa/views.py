from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from qa.models import Question, Answer, QuestionImage
from qa.serializers import (QuestionSerializer,
                            QuestionImageSerializer,
                            AnswerDisplaySerializer,
                            AnswerEditSerializer,
                            AnswerCommentDisplaySerializer,
                            NewAnswerCommentSerializer)
from users.models import Patient, StarredQuestion
from users.permissions import RikangKeyPermission, IsOwnerOrReadOnly, IsDoctor, IsPatient


class QuestionListView(generics.ListAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class NewQuestionView(generics.CreateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.patient)


class QuestionAddImageView(generics.CreateAPIView):

    queryset = QuestionImage.objects.all()
    serializer_class = QuestionImageSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs['pk'])
        serializer.save(question=question)


class QuestionDetailView(generics.RetrieveUpdateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsOwnerOrReadOnly)


class QuestionImageListView(generics.ListAPIView):

    serializer_class = QuestionImageSerializer
    pagination_class = None

    def get_queryset(self):
        question = Question.objects.get(id=self.kwargs['pk'])
        return question.images.all()


class QuestionStarView(APIView):

    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        patient = Patient.objects.get(user=request.user)
        starred_question, created = StarredQuestion.objects.get_or_create(patient=patient,
                                                                          question=question)

        # Ensure a question can only be starred once by one user
        # where a StarredQuestion object has just been created
        if created:
            question.stars += 1
            question.save()

        return Response({'id': int(pk), 'starred': True})


class PickAnswerView(APIView):

    def post(self, request, pk):
        question = Question.objects.get(id=pk)
        if question.owner == request.user.patient:
            question.solved = True
            question.save()
            answer = Answer.objects.get(id=request.data['pick'])
            answer.picked = True
            answer.save()
            return Response({'picked': True})
        else:
            # this request does not come from owner of this question
            return Response({'error': "无权执行此操作"}, status=status.HTTP_403_UNAUTHORIZED)


class AnswersListView(generics.ListAPIView):

    serializer_class = AnswerDisplaySerializer

    def get_queryset(self):
        return Answer.objects.filter(question__id=self.kwargs['pk'])


class NewAnswerView(generics.CreateAPIView):

    serializer_class = AnswerEditSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsDoctor)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.doctor)


class AnswersDetailView(generics.RetrieveUpdateAPIView):

    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AnswerDisplaySerializer
        else:
            # The request method is PUT
            return AnswerEditSerializer


class AnswerUpvoteView(APIView):

    def get(self, request, pk):
        answer = Answer.objects.get(id=pk)
        answer.upvotes += 1
        answer.save()

        return Response({'id': int(pk), 'upvoted': True})


class AnswerCommentsView(generics.ListAPIView):

    serializer_class = AnswerCommentDisplaySerializer

    def get_queryset(self):
        answer = Answer.objects.get(id=self.kwargs['pk'])
        return answer.comments.all()


class AnswerNewCommentView(generics.CreateAPIView):

    serializer_class = NewAnswerCommentSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(replier=self.request.user.doctor)
        except ObjectDoesNotExist:
            # this user is a patient
            serializer.save(replier=self.request.user.patient)
