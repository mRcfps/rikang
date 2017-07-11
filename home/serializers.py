from rest_framework import serializers

from home.models import Post, Hospital, DoctorComment
from qa.models import Answer
from users.serializers import PatientSerializer
from users.models import FavoritePost, FavoriteDoctor


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'photo', 'created')


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'photo', 'body', 'created')


class FavoritePostSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='post.id')
    title = serializers.CharField(source='post.title')
    photo = serializers.SerializerMethodField()
    created = serializers.DateField(source='post.created')

    class Meta:
        model = FavoritePost
        fields = ('id', 'title', 'photo', 'created')

    def get_photo(self, fav_post):
        request = self.context.get('request')
        try:
            photo = fav_post.post.photo.url
            return request.build_absolute_uri(photo)
        except ValueError:
            # this post has no photo
            return None


class HospitalListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'location', 'photo', 'doctor_num', 'rank')


class HospitalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'location', 'photo', 'doctor_num',
                  'phone', 'description', 'rank')


class FavoriteDoctorSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='doctor.id')
    name = serializers.CharField(source='doctor.name')
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteDoctor
        fields = ('id', 'name', 'avatar')

    def get_doctor_avatar(self, fav_doctor):
        request = self.context.get('request')
        try:
            doctor_avatar = fav_doctor.doctor.avatar.url
            return request.build_absolute_uri(doctor_avatar)
        except ValueError:
            # this doctor has no avatar
            return None


class DoctorAnswerSerializer(serializers.ModelSerializer):

    question_title = serializers.CharField(source='question.title')

    class Meta:
        model = Answer
        fields = ('id', 'question_title', 'question', 'diagnosis',
                  'prescription', 'course', 'advice', 'picked', 'upvotes')


class CommentDisplaySerializer(serializers.ModelSerializer):

    patient = PatientSerializer()

    class Meta:
        model = DoctorComment
        fields = ('id', 'patient', 'anonymous', 'ratings', 'created', 'body')


class NewCommentDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorComment
        fields = ('anonymous', 'ratings', 'body')
