# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-08 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20170808_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='开始时间'),
        ),
    ]
