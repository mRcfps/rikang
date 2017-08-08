from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from services import events


class Order(models.Model):

    # Order status
    UNPAID = 'U'
    PAID = 'P'
    UNDERWAY = 'W'
    REFUND = 'R'
    FINISHED = 'F'

    STATUS_CHOICES = (
        (UNPAID, '未支付'),
        (PAID, '已支付'),
        (UNDERWAY, '正在进行中'),
        (REFUND, '已退款'),
        (FINISHED, '已完成'),
    )

    order_no = models.UUIDField(editable=False,
                                verbose_name='订单编号')
    owner = models.ForeignKey('users.patient', related_name='orders', verbose_name='顾客')
    provider = models.ForeignKey('users.doctor', related_name='orders', verbose_name='服务提供者')
    cost = models.DecimalField(max_digits=5, decimal_places=2, editable=False, verbose_name='费用')
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=1,
                              default=UNPAID,
                              editable=False,
                              verbose_name='订单状态')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='创建时间')
    limit = models.Q(app_label='services', model='consultation')
    service_type = models.ForeignKey(ContentType,
                                     limit_choices_to=limit,
                                     on_delete=models.CASCADE,
                                     verbose_name='服务类型')
    service_object = GenericForeignKey('service_type', 'order_no')

    class Meta:
        ordering = ('-created',)
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '订单{}'.format(self.order_no)


class Consultation(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, verbose_name='咨询编号')
    doctor = models.ForeignKey('users.doctor',
                               related_name='consultations',
                               verbose_name='医生')
    patient = models.ForeignKey('users.patient',
                                related_name='consulations',
                                verbose_name='患者')
    start = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = '在线咨询'
        verbose_name_plural = verbose_name


class Comment(models.Model):

    patient = models.ForeignKey('users.Patient', related_name='comments', verbose_name='患者')
    doctor = models.ForeignKey('users.Doctor', related_name='comments', verbose_name='医生')
    order = models.OneToOneField('services.order', null=True, blank=True, verbose_name='订单')
    anonymous = models.BooleanField(default=False, verbose_name='匿名回答')
    ratings = models.PositiveIntegerField(validators=[MaxValueValidator(5)], verbose_name='评分')
    created = models.DateField(auto_now_add=True, verbose_name='创建时间')
    body = models.TextField(verbose_name='评论内容')

    class Meta:
        verbose_name = '订单评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}对{}医生的评价'.format(self.patient.name, self.doctor.name)


class Summary(models.Model):

    TYPE_CHOICES = (
        (events.DAILY_SUMMARY, "每日总结"),
        (events.WEEKLY_SUMMARY, "每周总结"),
        (events.MONTHLY_SUMMARY, "每月总结"),
    )

    summary_type = models.CharField(choices=TYPE_CHOICES, max_length=30, verbose_name="总结类型")
    charges_amount = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         verbose_name='交易金额（元）')
    charges_count = models.PositiveIntegerField(verbose_name='交易量（笔）')
    summary_from = models.DateTimeField(verbose_name='统计起始时间')
    summary_to = models.DateTimeField(verbose_name='统计终止时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = "交易总结"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} ~ {} {}".format(self.summary_from, self.summary_to, self.summary_type)
