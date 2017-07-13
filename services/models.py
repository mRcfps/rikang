import uuid
from django.db import models


class Consultation(models.Model):

    UNPAID = 'U'
    PAID = 'P'
    UNDERWAY = 'W'
    FINISHED = 'F'

    STATUS_CHOICES = (
        (UNPAID, '未支付'),
        (PAID, '已支付'),
        (UNDERWAY, '正在进行中'),
        (FINISHED, '已完成')
    )

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4().hex,
                          editable=False,
                          verbose_name='咨询单号')
    doctor = models.ForeignKey('users.doctor',
                               related_name='consultations',
                               verbose_name='医生')
    patient = models.ForeignKey('users.patient',
                                related_name='consulations',
                                verbose_name='患者')
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=1,
                              default=UNPAID,
                              verbose_name='状态')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '在线咨询'
        verbose_name_plural = verbose_name
