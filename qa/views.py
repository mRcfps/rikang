from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# import push

from qa.search import search
from qa.models import Question, Answer, QuestionImage, AnswerComment
from qa.serializers import (QuestionSerializer,
                            QuestionImageSerializer,
                            AnswerDisplaySerializer,
                            AnswerEditSerializer,
                            AnswerCommentDisplaySerializer,
                            NewAnswerCommentSerializer)
from users.models import Patient, StarredQuestion
from users.permissions import IsOwnerOrReadOnly, IsDoctor, IsPatient


class QuestionListView(generics.ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        department = self.request.query_params.get('dep', None)
        order = self.request.query_params.get('order', None)
        search_keyword = self.request.query_params.get('search', None)
        solved = self.request.query_params.get('solved', None)

        if search_keyword is None:
            queryset = Question.objects.all()

            if department is not None:
                queryset = queryset.filter(department=department)

            if order is not None:
                queryset = queryset.order_by(order)

            if solved is not None:
                queryset = queryset.filter(solved=solved)

            return queryset
        else:
            # full text search using keywords provided by user
            results = search(search_keyword)
            queryset = list()

            for result in results.hits:
                question = Question.objects.get(id=result.meta['id'])
                queryset.append(question)

            return queryset


class NewQuestionView(generics.CreateAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, IsPatient)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.patient)


class QuestionAddImageView(generics.CreateAPIView):

    queryset = QuestionImage.objects.all()
    serializer_class = QuestionImageSerializer
    permission_classes = (IsAuthenticated, IsPatient)

    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs['pk'])
        serializer.save(question=question)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class QuestionImageListView(generics.ListAPIView):

    serializer_class = QuestionImageSerializer
    pagination_class = None

    def get_queryset(self):
        question = Question.objects.get(id=self.kwargs['pk'])
        return question.images.all()


class QuestionStarView(APIView):

    permission_classes = (IsAuthenticated, IsPatient)

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


class QuestionUnstarView(APIView):

    permission_classes = (IsAuthenticated, IsPatient)

    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        patient = Patient.objects.get(user=request.user)
        starred_question = get_object_or_404(StarredQuestion, question=question, patient=patient)
        starred_question.delete()

        # deduct stars of the question
        question.stars -= 1
        question.save()

        return Response({'id': int(pk), 'unstarred': True})


class SolveQuestionView(APIView):

    permission_classes = (IsAuthenticated, IsDoctor)

    def post(self, request, pk):
        question = Question.objects.get(id=pk)

        if question.solved:
            return Response({'error': "问题已被解决"},
                            status=status.HTTP_400_BAD_REQUEST)

        question.solved = True
        question.solver = request.user.doctor
        question.save()

        return Response({'success': True})


class AnswersListView(generics.ListAPIView):

    serializer_class = AnswerDisplaySerializer

    def get_queryset(self):
        return Answer.objects.filter(question__id=self.kwargs['pk'])


class NewAnswerView(generics.CreateAPIView):

    serializer_class = AnswerEditSerializer
    permission_classes = (IsAuthenticated, IsDoctor)

    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs['pk'])
        doctor = self.request.user.doctor
        answer = serializer.save(question=question, owner=doctor)
        doctor.patient_num += 1
        doctor.save()


class AnswersDetailView(generics.RetrieveUpdateAPIView):

    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

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
            comment = serializer.save(replier=self.request.user.doctor)
        except ObjectDoesNotExist:
            # this user is a patient
            comment = serializer.save(replier=self.request.user.patient)

        # if comment.reply_to is not None:
        #     push.send_push_to_user(
        #         message='您的评论有了新的回复：{}'.format(comment.body),
        #         user_id=comment.reply_to.replier.user.id
        #     )
