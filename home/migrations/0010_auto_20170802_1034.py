# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-02 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_consultation_start'),
        ('home', '0009_hospital_doctor_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorcomment',
            name='order_no',
        ),
        migrations.AddField(
            model_name='doctorcomment',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.Order', verbose_name='评价订单'),
        ),
    ]
