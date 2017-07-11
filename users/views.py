from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, parsers, status

from users.models import Doctor, Patient, Information
from users.serializers import (UserSerializer,
                               DoctorSerializer,
                               PatientSerializer,
                               InformationSerializer)
from qa.serializers import QuestionSerializer, StarredQuestionSerializer
from home.serializers import FavoritePostSerializer, FavoriteDoctorSerializer


class UserLoginView(APIView):

    serializer_class = AuthTokenSerializer
    authentication_classes = set()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class UserRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = set()
    permission_classes = (AllowAny,)


class UserChangePasswordView(generics.UpdateAPIView):
    """Allow users to change their password with token auth."""

    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)


class DoctorInitView(generics.CreateAPIView):

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def perform_create(self, serializer):
        doctor = serializer.save(user=self.request.user)

        # Create info model for this doctor
        Information.objects.create(doctor=doctor)


class DoctorProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = DoctorSerializer

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


class DoctorInfoView(generics.RetrieveUpdateAPIView):

    serializer_class = InformationSerializer

    def get_object(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Information.objects.get(doctor=doctor)


class PatientProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = PatientSerializer

    def get_object(self):
        profile, created = Patient.objects.get_or_create(user=self.request.user)
        return profile


class PatientQuestionsView(generics.ListAPIView):

    serializer_class = QuestionSerializer
    pagination_class = None

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.questions.all()


class PatientStarredQuestionsView(generics.ListAPIView):

    serializer_class = StarredQuestionSerializer
    pagination_class = None

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.starred_questions.all()


class PatientFavDoctorsView(generics.ListAPIView):

    serializer_class = FavoriteDoctorSerializer
    pagination_class = None

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.favorite_doctors.all()


class PatientFavPostsView(generics.ListAPIView):

    serializer_class = FavoritePostSerializer

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.favorite_posts.all()
