from django.db import models

import departments
from users.models import Doctor, Patient


class Question(models.Model):

    title = models.CharField(max_length=100, verbose_name='标题')
    department = models.CharField(
        choices=departments.DEPARTMENT_CHOICES,
        max_length=3,
        verbose_name='科室'
    )
    questioner = models.ForeignKey(Patient, null=True, verbose_name='提问者')
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

    def author_name(self):
        return self.author.name

    def author_info(self):
        hospital = None if self.author.hospital is None else self.author.hospital.name
        return hospital + self.author.get_title_display()
