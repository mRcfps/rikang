# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-18 10:38
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20170717_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='code',
            field=models.IntegerField(default=users.models.random_code, verbose_name='验证码'),
        ),
    ]
