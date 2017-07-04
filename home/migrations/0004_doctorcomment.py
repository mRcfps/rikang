# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-03 14:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170701_1440'),
        ('home', '0003_auto_20170627_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous', models.BooleanField(default=False, verbose_name='匿名回答')),
                ('ratings', models.PositiveIntegerField(verbose_name='评分')),
                ('created', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('body', models.TextField(verbose_name='评论内容')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.Doctor', verbose_name='全部评价')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.Patient', verbose_name='全部评价')),
            ],
            options={
                'verbose_name_plural': '医生评论',
                'verbose_name': '医生评论',
            },
        ),
    ]