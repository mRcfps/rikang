from django.db import models
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
    cost = models.DecimalField(max_digits=5, decimal_places=2, editable=False, verbose_name='费用')
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=1,
                              default=UNPAID,
                              editable=False,
                              verbose_name='订单状态')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='创建时间')
    service_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     verbose_name='服务类型')
    service_object = GenericForeignKey('service_type', 'order_no')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class Consultation(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, verbose_name='咨询编号')
    doctor = models.ForeignKey('users.doctor',
                               related_name='consultations',
                               verbose_name='医生')
    patient = models.ForeignKey('users.patient',
                                related_name='consulations',
                                verbose_name='患者')

    class Meta:
        verbose_name = '在线咨询'
        verbose_name_plural = verbose_name


class Summary(models.Model):

    TYPE_CHOICES = (
        (events.DAILY_SUMMARY, "每日总结"),
        (events.WEEKLY_SUMMARY, "每周总结"),
        (events.MONTHLY_SUMMARY, "每月总结"),
    )

    summary_type = models.CharField(choices=TYPE_CHOICES, max_length=20, verbose_name="总结类型")
    charges_amount = models.DecimalField(max_digits=5,
                                         decimal_places=2,
                                         verbose_name='交易金额（元）')
    charges_count = models.PositiveIntegerField(verbose_name='交易量（笔）')
    summary_from = models.DateTimeField(verbose_name='统计起始时间')
    summary_to = models.DateTimeField(verbose_name='统计终止时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
