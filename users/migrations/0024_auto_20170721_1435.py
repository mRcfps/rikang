# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-21 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20170721_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='information',
            options={'verbose_name': '医生详细资料', 'verbose_name_plural': '医生详细资料'},
        ),
    ]