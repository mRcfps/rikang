# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-18 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0012_auto_20170718_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercomment',
            name='replier_id',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='评论者编号'),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='replier_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='评论者身份'),
        ),
    ]
