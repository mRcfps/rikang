# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-29 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_auto_20170726_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(default='小康', max_length=50, verbose_name='姓名'),
        ),
    ]
