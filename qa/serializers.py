from rest_framework import serializers

from qa.models import Question, Answer, QuestionImage, AnswerComment
from users.serializers import DoctorSerializer
from users.models import StarredQuestion


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'title', 'department', 'body',
                  'answer_num', 'solved', 'stars', 'created')


class StarredQuestionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='question.id')
    title = serializers.CharField(source='question.title')
    answer_num = serializers.IntegerField(source='question.answer_num')
    created = serializers.DateField(source='question.created')

    class Meta:
        model = StarredQuestion
        fields = ('id', 'title', 'answer_num', 'created')


class AnswerDisplaySerializer(serializers.ModelSerializer):

    owner = DoctorSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'question', 'owner', 'diagnosis', 'prescription',
                  'course', 'advice', 'picked', 'upvotes', 'comment_num', 'created')
        read_only_fields = ('picked', 'upvotes', 'comment_num', 'created')


class AnswerEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('question', 'owner', 'diagnosis', 'prescription',
                  'course', 'advice')

class QuestionImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionImage
        fields = ('question', 'image')


class AnswerCommentDisplaySerializer(serializers.ModelSerializer):

    replier_name = serializers.CharField(source='replier.name')
    replier_avatar = serializers.SerializerMethodField()

    class Meta:
        model = AnswerComment
        fields = ('id', 'replier_name', 'replier_avatar',
                  'reply_to', 'body', 'upvotes', 'created')

    def get_replier_avatar(self, comment):
        request = self.context.get('request')
        try:
            replier_avatar = comment.replier.avatar.url
            return request.build_absolute_uri(replier_avatar)
        except ValueError:
            # this user has no avatar
            return None


class NewAnswerCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerComment
        fields = ('answer', 'reply_to', 'body')
