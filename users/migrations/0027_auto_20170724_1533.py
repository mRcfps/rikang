# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-24 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20170722_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.CharField(default=0, max_length=50, verbose_name='医院'),
            preserve_default=False,
        ),
    ]
