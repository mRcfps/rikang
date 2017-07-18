import random
from functools import partial

from django.db import models
from django.contrib.auth.models import User

import departments
from home.models import Hospital, Post


def random_code():
        return random.randrange(1001, 9999)


class Phone(models.Model):

    number = models.CharField(max_length=11, verbose_name='手机号码')
    verified = models.BooleanField(default=False, verbose_name='是否通过验证')
    code = models.IntegerField(default=random_code, verbose_name='验证码')
    created = models.DateField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '手机号码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.number


class Doctor(models.Model):

    # Titles of doctors
    RESIDENT = 'R'
    ATTENDING = 'A'
    DEPUTY_CHIEF = 'D'
    CHIEF = 'C'

    TITLE_CHOICES = (
        (RESIDENT, '住院医师'),
        (ATTENDING, '主治医师'),
        (DEPUTY_CHIEF, '副主任医师'),
        (CHIEF, '主任医师'),
    )

    user = models.OneToOneField(User, verbose_name='手机号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    hospital = models.ForeignKey(Hospital,
                                 related_name='doctors',
                                 null=True,
                                 verbose_name='所属医院')
    department = models.CharField(choices=departments.DEPARTMENT_CHOICES,
                                  max_length=3,
                                  verbose_name='科室')
    years = models.PositiveIntegerField(verbose_name='从医时间')
    consult_price = models.DecimalField(default=0,
                                        max_digits=10,
                                        decimal_places=2,
                                        verbose_name='咨询价格')
    title = models.CharField(choices=TITLE_CHOICES, max_length=1, verbose_name='职称')
    ratings = models.PositiveIntegerField(default=5, verbose_name='评分')
    patient_num = models.PositiveIntegerField(default=0, verbose_name='已帮助患者')
    created = models.DateField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        ordering = ('patient_num', 'ratings', 'years')
        verbose_name = '医生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def order_num(self):
        return self.consultations.count()


class Information(models.Model):

    doctor = models.OneToOneField(Doctor)
    specialty = models.TextField(blank=True, verbose_name='专长')
    background = models.TextField(blank=True, verbose_name='教育背景')
    achievements = models.TextField(blank=True, verbose_name='学术研究成果及获奖情况')
    motto = models.TextField(blank=True, verbose_name='医生寄语')


class Patient(models.Model):

    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'

    SEX_CHOICES = (
        (MALE, '男'),
        (FEMALE, '女'),
        (UNKNOWN, '未选择'),
    )

    user = models.OneToOneField(User, verbose_name='手机号')
    name = models.CharField(default='unnamed', max_length=50, verbose_name='姓名')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=UNKNOWN, verbose_name='性别')
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name='年龄')
    medical_history = models.TextField(blank=True, null=True, verbose_name='疾病历史')
    created = models.DateField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '患者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class StarredQuestion(models.Model):

    patient = models.ForeignKey(Patient, related_name='starred_questions', verbose_name='患者')
    question = models.ForeignKey('qa.question', verbose_name='问题')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        ordering = ('-created',)
        unique_together = ('patient', 'question')


class FavoritePost(models.Model):

    patient = models.ForeignKey(Patient, related_name='favorite_posts', verbose_name='患者')
    post = models.ForeignKey('home.post', verbose_name='文章')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        ordering = ('-created',)
        unique_together = ('patient', 'post')


class FavoriteDoctor(models.Model):

    patient = models.ForeignKey(Patient, related_name='favorite_doctors', verbose_name='患者')
    doctor = models.ForeignKey(Doctor, verbose_name='医生')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        ordering = ('-created',)
        unique_together = ('patient', 'doctor')
