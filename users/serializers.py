from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Doctor, Patient, Information


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
        fields = ('id', 'name', 'avatar', 'department', 'years',
                  'title', 'hospital_name', 'ratings', 'patient_num')


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ('id', 'name', 'avatar')


class InformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Information
        fields = '__all__'
