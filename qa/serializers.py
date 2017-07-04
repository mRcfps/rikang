from rest_framework import serializers

from qa.models import Question, Answer, QuestionImage
from users.serializers import DoctorSerializer


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'title', 'department', 'body',
                  'answer_num', 'solved', 'stars', 'created')


class AnswerDisplaySerializer(serializers.ModelSerializer):

    author = DoctorSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'question', 'author', 'diagnosis', 'prescription',
                  'course', 'advice', 'picked', 'upvotes', 'created')
        read_only_fields = ('picked', 'upvotes', 'created')


class AnswerEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('question', 'author', 'diagnosis', 'prescription',
                  'course', 'advice')

class QuestionImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionImage
        fields = ('question', 'image')
