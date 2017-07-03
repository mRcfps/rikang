# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-01 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_patient_starred_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='home.Hospital', verbose_name='所属医院'),
        ),
    ]