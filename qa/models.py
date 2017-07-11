from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import departments
from users.models import Doctor, Patient


class Question(models.Model):

    title = models.CharField(max_length=100, verbose_name='标题')
    department = models.CharField(
        choices=departments.DEPARTMENT_CHOICES,
        max_length=3,
        verbose_name='科室'
    )
    questioner = models.ForeignKey(Patient, related_name='questions', null=True, verbose_name='提问者')
    body = models.TextField(verbose_name='内容')
    solved = models.BooleanField(default=False, verbose_name='已解决')
    stars = models.IntegerField(default=0, verbose_name='关注人数')
    updated = models.DateTimeField(auto_now=True, verbose_name='最近更新时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def answer_num(self):
        return self.answers.count()


class QuestionImage(models.Model):

    question = models.ForeignKey(Question, related_name='images')
    image = models.ImageField(upload_to='questions/', verbose_name='照片')


class Answer(models.Model):

    question = models.ForeignKey(Question,
                                 related_name='answers',
                                 verbose_name='问题')
    author = models.ForeignKey(Doctor,
                               related_name='answers',
                               verbose_name='作者')
    diagnosis = models.CharField(blank=True, max_length=100, verbose_name='疾病预测')
    prescription = models.CharField(blank=True, max_length=50, verbose_name='药物选择')
    course = models.CharField(blank=True, max_length=100, verbose_name='推荐疗程')
    advice = models.CharField(blank=True, max_length=100, verbose_name='指导建议')
    picked = models.BooleanField(default=False, verbose_name='被采纳')
    upvotes = models.PositiveIntegerField(default=0, verbose_name='支持数')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '回答'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}的回答'.format(self.author.name)


class AnswerComment(models.Model):

    answer = models.ForeignKey(Answer, related_name='comments', verbose_name='回答')
    replier_type = models.ForeignKey(ContentType, null=True, blank=True, verbose_name='回答者身份')
    replier_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='回答者编号')
    replier = GenericForeignKey('replier_type', 'replier_id')
    reply_to = models.ForeignKey('self',
                                 null=True,
                                 blank=True,
                                 related_name='replies',
                                 verbose_name='回复评论')
    body = models.TextField(verbose_name='评论内容')
    upvotes = models.PositiveIntegerField(default=0, verbose_name='获赞数')
    created = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = '回答评论'
        verbose_name_plural = verbose_name
