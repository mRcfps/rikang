# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-11 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_doctorcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
    ]
