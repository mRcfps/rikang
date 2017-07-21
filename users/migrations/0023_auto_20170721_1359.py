# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-21 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_doctor_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ('patient_num', 'ratings'), 'verbose_name': '医生', 'verbose_name_plural': '医生'},
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='years',
        ),
        migrations.AddField(
            model_name='doctor',
            name='start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='开始从医年份'),
            preserve_default=False,
        ),
    ]