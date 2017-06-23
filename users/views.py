from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, parsers, status

from users.models import Information
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

    authentication_classes = (TokenAuthentication,)
    serializer_class = DoctorSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # Create info model for this doctor
        Information.objects.create(doctor=self.request.user)


class DoctorProfileView(generics.RetrieveAPIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = DoctorSerializer


class DoctorInfoView(generics.RetrieveUpdateAPIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = InformationSerializer


class PatientProfileView(generics.RetrieveAPIView):

    authentication_classes = (TokenAuthentication,)
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
