# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-28 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20170628_0912'),
        ('users', '0002_auto_20170627_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='starred_questions',
            field=models.ManyToManyField(to='qa.Question'),
        ),
    ]
