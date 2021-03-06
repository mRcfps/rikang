from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import departments
from users.models import Doctor, Patient
from qa.search import ESQuestion


class Question(models.Model):

    title = models.CharField(max_length=100, verbose_name='标题')
    department = models.CharField(
        choices=departments.DEPARTMENT_CHOICES,
        max_length=3,
        verbose_name='科室'
    )
    owner = models.ForeignKey(Patient,
                              related_name='questions',
                              null=True,
                              verbose_name='提问者')
    solver = models.ForeignKey(Doctor, null=True, blank=True, verbose_name='回答医生')
    body = models.TextField(verbose_name='内容')
    solved = models.BooleanField(default=False, verbose_name='已解决')
    stars = models.IntegerField(default=0, verbose_name='关注人数')
    updated = models.DateTimeField(auto_now=True, verbose_name='最近更新时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('stars', 'answers', '-updated')
        verbose_name = '问题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    @property
    def answer_num(self):
        return self.answers.count()

    def indexing(self):
        esq = ESQuestion(
            meta={'id': self.pk},
            title=self.title,
            department=self.department,
            body=self.body,
            solved=self.solved,
            stars=self.stars,
            answer_num=self.answer_num,
            created=self.created
        )
        esq.save(index='rikang_qa')
        return esq.to_dict(include_meta=True)


class QuestionImage(models.Model):

    question = models.ForeignKey(Question, related_name='images')
    image = models.ImageField(upload_to='questions/', verbose_name='照片')


class Answer(models.Model):

    question = models.ForeignKey(Question,
                                 related_name='answers',
                                 verbose_name='问题')
    owner = models.ForeignKey(Doctor,
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
        ordering = ('picked', 'upvotes', '-created')
        verbose_name = '回答'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}的回答'.format(self.owner.name)

    @property
    def comment_num(self):
        return self.comments.count()


class AnswerComment(models.Model):

    answer = models.ForeignKey(Answer, related_name='comments', verbose_name='回答')
    limit = models.Q(app_label='users', model='doctor') | models.Q(app_label='users', model='patient')
    replier_type = models.ForeignKey(ContentType,
                                     limit_choices_to=limit,
                                     null=True,
                                     blank=True,
                                     verbose_name='评论者身份')
    replier_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='评论者编号')
    replier = GenericForeignKey('replier_type', 'replier_id')
    reply_to = models.ForeignKey('self',
                                 null=True,
                                 blank=True,
                                 related_name='replies',
                                 verbose_name='回复评论')
    body = models.TextField(verbose_name='评论内容')
    upvotes = models.PositiveIntegerField(default=0, verbose_name='获赞数')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = '回答评论'
        verbose_name_plural = verbose_name


@receiver(post_save, sender=Question)
def index_question(sender, instance, **kwargs):
    instance.indexing()
