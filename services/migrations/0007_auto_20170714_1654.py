# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-14 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20170714_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='summary_type',
            field=models.CharField(choices=[('summary.daily.available', '每日总结'), ('summary.weekly.available', '每周总结'), ('summary.monthly.available', '每月总结')], max_length=20, verbose_name='总结类型'),
        ),
    ]