# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-11 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20170711_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='medical_history',
            field=models.TextField(blank=True, null=True, verbose_name='疾病历史'),
        ),
    ]