from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

import push

from users.models import Doctor, Information, Patient, FavoritePost, FavoriteDoctor
from users.serializers import DoctorSerializer, InformationSerializer
from home.models import Post, Hospital, DoctorComment
from home.serializers import (PostListSerializer,
                              PostDetailSerializer,
                              HospitalListSerializer,
                              HospitalDetailSerializer,
                              DoctorAnswerSerializer,
                              CommentDisplaySerializer,
                              NewCommentDisplaySerializer)


class PostListView(generics.ListAPIView):
    """GET a collection of posts."""

    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(generics.RetrieveAPIView):
    """GET a single post by id."""

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostFavView(generics.RetrieveAPIView):
    """GET this endpoint and the user will have desired post added
    to his/her favorite_posts."""

    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)
        post = Post.objects.get(id=self.kwargs['pk'])
        fav_post, created = FavoritePost.objects.get_or_create(patient=patient, post=post)

        return Response({'id': self.kwargs['pk'], 'success': True})


class PostUnfavView(generics.RetrieveAPIView):
    """GET this endpoint and the given post will be removed from favorite posts."""

    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)
        post = Post.objects.get(id=self.kwargs['pk'])
        fav_post = get_object_or_404(FavoritePost, patient=patient, post=post)
        fav_post.delete()

        return Response({'id': self.kwargs['pk'], 'success': True})


class HospitalListView(generics.ListAPIView):
    """GET a collection of hospitals."""

    queryset = Hospital.objects.all()
    serializer_class = HospitalListSerializer


class HospitalDetailView(generics.RetrieveAPIView):
    """GET a single hospital by id."""

    queryset = Hospital.objects.all()
    serializer_class = HospitalDetailSerializer


class HospitalDoctorsView(generics.ListAPIView):
    """GET all doctors of a hospital by given id."""

    serializer_class = DoctorSerializer

    def get_queryset(self):
        hospital = Hospital.objects.get(id=self.kwargs['pk'])
        return hospital.doctors.all()


class DoctorListView(generics.ListAPIView):
    """GET a collection of doctors."""

    serializer_class = DoctorSerializer

    def get_queryset(self):
        dep = self.request.query_params.get('dep', None)
        order = self.request.query_params.get('order', None)
        results = Doctor.active_doctors.all()

        if dep is not None:
            # filter against given department
            results = results.filter(department=dep)

        if order is not None:
            results = results.order_by(order)

        return results


class DoctorDetailView(generics.RetrieveAPIView):
    """GET a single doctor by id."""

    queryset = Doctor.active_doctors.all()
    serializer_class = DoctorSerializer


class DoctorInfoView(generics.RetrieveAPIView):
    """GET a doctor's information."""

    queryset = Information.objects.all()
    serializer_class = InformationSerializer


class DoctorFavView(APIView):
    """GET this endpoint and the user will have desired doctor added
    to his/her favorite_doctors."""

    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)
        doctor = get_object_or_404(Doctor, id=self.kwargs['pk'], active=True)
        fav_doctor, created = FavoriteDoctor.objects.get_or_create(patient=patient,
                                                                   doctor=doctor)

        return Response({'id': self.kwargs['pk'], 'success': True})


class DoctorUnfavView(APIView):
    """
    GET this endpoint and the given doctor will be removed from
    favorite doctors.
    """

    def get(self, request, *args, **kwargs):
        patient = Patient.objects.get(user=request.user)
        doctor = get_object_or_404(Doctor, id=self.kwargs['pk'], active=True)
        fav_doctor = get_object_or_404(FavoriteDoctor, patient=patient, doctor=doctor)
        fav_doctor.delete()

        return Response({'id': self.kwargs['pk'], 'success': True})


class DoctorAnswersView(generics.ListAPIView):

    serializer_class = DoctorAnswerSerializer

    def get_queryset(self):
        doctor = get_object_or_404(Doctor, id=self.kwargs['pk'], active=True)
        return doctor.answers.all()


class DoctorCommentsView(generics.ListAPIView):

    serializer_class = CommentDisplaySerializer

    def get_queryset(self):
        doctor = get_object_or_404(Doctor, id=self.kwargs['pk'], active=True)
        return DoctorComment.objects.filter(doctor=doctor)


class DoctorNewCommentView(generics.CreateAPIView):

    queryset = DoctorComment.objects.all()
    serializer_class = NewCommentDisplaySerializer

    def perform_create(self, serializer):
        doctor = get_object_or_404(Doctor, id=self.kwargs['pk'], active=True)
        serializer.save(patient=self.request.user.patient, doctor=doctor)

        # calculate new rating for this doctor
        new_rating = serializer.validated_data['ratings']
        comment_num = doctor.comments.count()
        doctor.ratings = (doctor.ratings * (comment_num - 1) + new_rating) / comment_num
        doctor.save()

        push.send_push_to_user(
            message="有位用户刚刚对您做出了评价。",
            user_id=doctor.user.id
        )
