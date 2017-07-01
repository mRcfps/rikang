from rest_framework import serializers

from qa.models import Question, Answer, QuestionImage


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'title', 'department', 'body',
                  'answer_num', 'solved', 'stars', 'created')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'question', 'author', 'author_name',
                  'author_info', 'diagnosis', 'prescription',
                  'course', 'advice', 'picked', 'upvotes', 'created')


class QuestionImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionImage
        fields = ('question', 'image')
