# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-21 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20170718_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='active',
            field=models.BooleanField(default=False, verbose_name='是否审核通过'),
        ),
    ]
