from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Doctor, Information, Patient
from users.serializers import DoctorSerializer, InformationSerializer
from home.models import Post, Hospital
from home.serializers import (PostListSerializer,
                              PostDetailSerializer,
                              HospitalListSerializer,
                              HospitalDetailSerializer)


class PostListView(generics.ListAPIView):
    """GET a collection of posts."""

    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(generics.RetrieveAPIView):
    """GET a single post by id."""

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class HospitalListView(generics.ListAPIView):
    """GET a collection of hospitals."""

    queryset = Hospital.objects.all()
    serializer_class = HospitalListSerializer


class HospitalDetailView(generics.RetrieveAPIView):
    """GET a single hospital by id."""

    queryset = Hospital.objects.all()
    serializer_class = HospitalDetailSerializer


class DoctorListView(generics.ListAPIView):
    """GET a collection of doctors。"""

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorDetailView(generics.RetrieveAPIView):
    """GET a single doctor by id."""

    queryset = Doctor.objects.all()
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
        doctor = Doctor.objects.get(id=self.kwargs['pk'])
        patient.favorite_doctors.add(doctor)
        patient.save()

        return Response({'success': True})
