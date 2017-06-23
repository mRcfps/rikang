from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, parsers, status

from users.models import Doctor, Patient, Information
from users.serializers import (UserSerializer,
                               DoctorSerializer,
                               PatientSerializer,
                               InformationSerializer)


class UserLoginView(APIView):

    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class UserRegistrationView(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DoctorInitView(generics.CreateAPIView):

    queryset = Doctor.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = DoctorSerializer

    def perform_create(self, serializer):
        doctor = serializer.save(user=self.request.user)

        # Create info model for this doctor
        Information.objects.create(doctor=doctor)


class DoctorProfileView(generics.RetrieveUpdateAPIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = DoctorSerializer

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


class DoctorInfoView(generics.RetrieveUpdateAPIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = InformationSerializer

    def get_object(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Information.objects.get(doctor=doctor)


class PatientProfileView(generics.RetrieveUpdateAPIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = PatientSerializer

    def get_object(self):
        profile = Patient.objects.get_or_create(user=self.request.user)
        return profile
