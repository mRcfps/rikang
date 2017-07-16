import random

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from users.models import Phone, Doctor, Patient, Information
from users.serializers import (UserSerializer,
                               DoctorSerializer,
                               PatientSerializer,
                               InformationSerializer)
from users.permissions import RikangKeyPermission, IsDoctor, IsPatient, IsSMSVerified
from users.sms import send_sms_code
from qa.serializers import QuestionSerializer, StarredQuestionSerializer
from home.serializers import FavoritePostSerializer, FavoriteDoctorSerializer
from services.serializers import ConsultationOrderSerializer


class UserLoginView(APIView):

    serializer_class = AuthTokenSerializer
    authentication_classes = []
    permission_classes = (RikangKeyPermission,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class UserRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = (RikangKeyPermission, IsSMSVerified)


class UserChangePasswordView(generics.UpdateAPIView):
    """Allow users to change their password with token auth."""

    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)


class RequestSmsCodeView(APIView):

    authentication_classes = []
    permission_classes = (RikangKeyPermission,)

    def post(self, request):
        phone, created = Phone.objects.get_or_create(number=request.data['phone'])
        result = send_sms_code(phone.number, phone.code)

        if result == status.HTTP_200_OK:
            return Response({'success': True})
        else:
            # Sms code was not sent successfully for some reason
            return Response({'error': "发送短信失败"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


class VerifySmsCodeView(APIView):

    authentication_classes = []
    permission_classes = (RikangKeyPermission,)

    def post(self, request):
        phone = get_object_or_404(Phone, number=request.data['phone'])
        if phone.code == int(request.data['code']):
            # SMS verification passed
            phone.verified = True
            phone.save()
            return Response({'verified': True})
        else:
            return Response({'error': "验证码不正确"},
                            status=status.HTTP_400_BAD_REQUEST)


class DoctorInitView(generics.CreateAPIView):

    serializer_class = DoctorSerializer

    def perform_create(self, serializer):
        doctor = serializer.save(user=self.request.user)

        # Create info model for this doctor
        Information.objects.create(doctor=doctor)


class DoctorProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsDoctor)

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


class DoctorInfoView(generics.RetrieveUpdateAPIView):

    serializer_class = InformationSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsDoctor)

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
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.questions.all()


class PatientStarredQuestionsView(generics.ListAPIView):

    serializer_class = StarredQuestionSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.starred_questions.all()


class PatientFavDoctorsView(generics.ListAPIView):

    serializer_class = FavoriteDoctorSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.favorite_doctors.all()


class PatientFavPostsView(generics.ListAPIView):

    serializer_class = FavoritePostSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.favorite_posts.all()


class PatientServicesView(generics.ListAPIView):

    serializer_class = ConsultationOrderSerializer
    permission_classes = (IsAuthenticated, RikangKeyPermission, IsPatient)
    pagination_class = None

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return patient.orders.all()
