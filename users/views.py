from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

# import push

from users.models import Phone, Doctor, Patient, Information, Income
from users.serializers import (UserSerializer,
                               DoctorSerializer,
                               DoctorEditSerializer,
                               PatientSerializer,
                               InformationSerializer)
from users.permissions import RikangKeyPermission, IsDoctor, IsPatient, IsSMSVerified
from users.sms import send_sms_code
from qa.serializers import QuestionSerializer, StarredQuestionSerializer
from home.serializers import FavoritePostSerializer, FavoriteDoctorSerializer
from services.serializers import (ConsultationSerializer,
                                  ConsultationOrderSerializer)


class UserLoginView(APIView):

    serializer_class = AuthTokenSerializer
    authentication_classes = []
    permission_classes = (RikangKeyPermission,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'id': user.id,
            'token': token.key
        })


class UserRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = (RikangKeyPermission, IsSMSVerified)


class UserChangePasswordView(APIView):
    """Allow users to change their password with token auth."""

    def post(self, request):
        user = request.user
        try:
            old_password = request.data['old_password']
            new_password = request.data['new_password']
        except KeyError:
            return Response({'error': "表单格式错误"},
                            status=status.HTTP_400_BAD_REQUEST)

        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            return Response({'changed': True})
        else:
            return Response({'error': "旧密码错误"},
                            status=status.HTTP_403_FORBIDDEN)


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

    serializer_class = DoctorEditSerializer

    def perform_create(self, serializer):
        doctor = serializer.save(user=self.request.user)


class DoctorProfileView(generics.RetrieveUpdateAPIView):

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DoctorSerializer
        else:
            # the method is PUT
            return DoctorEditSerializer


class DoctorInfoView(generics.RetrieveUpdateAPIView):

    serializer_class = InformationSerializer

    def get_object(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Information.objects.get(doctor=doctor)


class DoctorOrdersView(generics.ListAPIView):

    serializer_class = ConsultationOrderSerializer
    pagination_class = None

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return doctor.orders.all()


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


# class NewCIDView(generics.CreateAPIView):

#     serializer_class = CIDSerializer


@staff_member_required
def admin_verify_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    context = {'doctor': doctor}

    return render(request, 'users/verify_doctor.html', context)


@staff_member_required
def admin_notify_verified_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.active = True
    doctor.save()
    # push.send_push_to_user(
    #     message="恭喜您通过日康的医生审核！欢迎成为日康平台的一员！",
    #     user_id=doctor.user.id
    # )

    return redirect('admin:users_doctor_changelist')


@staff_member_required
def admin_dispatch_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    doctor = income.doctor
    context = {'doctor': doctor, 'income': income}

    return render(request, 'users/dispatch_income.html', context)


@staff_member_required
def admin_confirm_dispatch(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    income.gained += income.suspended
    income.suspended = 0
    income.save()

    return redirect('admin:users_income_changelist')
