# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-17 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20170716_2133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phone',
            options={'verbose_name': '手机号码', 'verbose_name_plural': '手机号码'},
        ),
        migrations.AlterField(
            model_name='phone',
            name='code',
            field=models.IntegerField(default=3640, verbose_name='验证码'),
        ),
    ]