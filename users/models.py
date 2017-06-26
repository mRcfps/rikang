from django.db import models
from django.contrib.auth.models import User

import departments
from home.models import Hospital


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
                                 verbose_name='所属医院')
    department = models.CharField(choices=departments.DEPARTMENT_CHOICES,
                                  max_length=3,
                                  verbose_name='科室')
    years = models.PositiveIntegerField(verbose_name='从医时间')
    title = models.CharField(choices=TITLE_CHOICES, max_length=1, verbose_name='职称')
    ratings = models.PositiveIntegerField(default=5, verbose_name='评分')
    patient_num = models.PositiveIntegerField(default=0, verbose_name='已帮助患者')
    created = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '医生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def hospital_name(self):
        return self.hospital.name


class Information(models.Model):

    doctor = models.OneToOneField(Doctor)
    specialty = models.TextField(blank=True, verbose_name='专长')
    background = models.TextField(blank=True, verbose_name='教育背景')
    achievements = models.TextField(blank=True, verbose_name='学术研究成果及获奖情况')
    motto = models.TextField(blank=True, verbose_name='医生寄语')


class Patient(models.Model):

    user = models.OneToOneField(User, verbose_name='手机号')
    name = models.CharField(default='unnamed', max_length=50, verbose_name='姓名')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    favorite_doctors = models.ManyToManyField(Doctor, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '患者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
