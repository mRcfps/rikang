import random
from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
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


class ActiveDoctorManager(models.Manager):
    """
    Model manager that returns only verified doctors
    (`active` field is `True`).
    """
    def get_queryset(self):
        queryset = super(ActiveDoctorManager, self).get_queryset()
        return queryset.filter(active=True)


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
    hospital = models.CharField(max_length=50, verbose_name='医院')
    department = models.CharField(choices=departments.DEPARTMENT_CHOICES,
                                  max_length=3,
                                  verbose_name='科室')
    start = models.DateField(verbose_name='开始从医日期')
    consult_price = models.DecimalField(default=0,
                                        max_digits=10,
                                        decimal_places=2,
                                        verbose_name='咨询价格')
    title = models.CharField(choices=TITLE_CHOICES, max_length=1, verbose_name='职称')
    ratings = models.DecimalField(default=5.0,
                                  max_digits=2,
                                  decimal_places=1,
                                  validators=[MinValueValidator(0), MaxValueValidator(5)],
                                  verbose_name='评分')
    patient_num = models.PositiveIntegerField(default=0, verbose_name='已帮助患者')
    active = models.BooleanField(default=False, verbose_name='是否审核通过')
    created = models.DateField(auto_now_add=True, verbose_name='注册时间')
    doctor_license = models.ImageField(null=True,
                                       blank=True,
                                       upload_to='licenses/',
                                       verbose_name='医生执照')
    id_card = models.ImageField(null=True, blank=True, upload_to='idcards/', verbose_name='持证自拍')

    # model managers
    objects = models.Manager()
    active_doctors = ActiveDoctorManager()

    class Meta:
        ordering = ('patient_num', 'ratings')
        verbose_name = '医生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def order_num(self):
        return self.consultations.count()

    @property
    def years(self):
        return datetime.now().year - self.start.year


class Information(models.Model):

    doctor = models.OneToOneField(Doctor, verbose_name='医生')
    specialty = models.TextField(blank=True, verbose_name='专长')
    background = models.TextField(blank=True, verbose_name='教育背景')
    achievements = models.TextField(blank=True, verbose_name='学术研究成果及获奖情况')
    motto = models.TextField(blank=True, verbose_name='医生寄语')

    class Meta:
        verbose_name = "医生详细资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.doctor.name + "的详细资料"


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
    name = models.CharField(default='小康', max_length=50, verbose_name='姓名')
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


@receiver(post_save, sender=Doctor)
def create_new_info(sender, **kwargs):
    doctor = kwargs.get('instance')
    Information.objects.create(doctor=doctor)
