from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Doctor, Patient, Information, Income


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ('id', 'name', 'avatar', 'department', 'years', 'consult_price',
                  'order_num', 'title', 'hospital', 'ratings', 'patient_num')
        read_only_fields = ('id', 'order_num', 'ratings', 'patient_num')


class DoctorEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ('name', 'avatar', 'department', 'start', 'consult_price',
                  'title', 'hospital', 'doctor_license', 'id_card')


class PatientSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = Patient
        fields = ('id', 'avatar', 'phone', 'name', 'sex', 'age', 'medical_history')
        read_only_fields = ('id', 'phone')


class InformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Information
        exclude = ('id', 'doctor')


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ('total', 'gained', 'suspended')
