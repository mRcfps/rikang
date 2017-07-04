from rest_framework import serializers

from home.models import Post, Hospital, DoctorComment
from users.serializers import PatientSerializer


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'photo', 'created')


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'photo', 'body', 'created')


class HospitalListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'location', 'photo', 'doctor_num', 'rank')


class HospitalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'location', 'photo', 'doctor_num',
                  'phone', 'description', 'rank')


class CommentDisplaySerializer(serializers.ModelSerializer):

    patient = PatientSerializer()

    class Meta:
        model = DoctorComment
        fields = ('patient', 'anonymous', 'ratings', 'created', 'body')


class NewCommentDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorComment
        fields = ('anonymous', 'ratings', 'body')
