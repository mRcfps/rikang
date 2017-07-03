# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-01 20:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_auto_20170701_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='questions/', verbose_name='照片')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='qa.Question')),
            ],
        ),
    ]