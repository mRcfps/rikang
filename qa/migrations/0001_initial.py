# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-27 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20170627_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(blank=True, max_length=100, verbose_name='疾病预测')),
                ('prescription', models.CharField(blank=True, max_length=50, verbose_name='药物选择')),
                ('course', models.CharField(blank=True, max_length=100, verbose_name='推荐疗程')),
                ('advice', models.CharField(blank=True, max_length=100, verbose_name='指导建议')),
                ('picked', models.BooleanField(default=False, verbose_name='被采纳')),
                ('upvotes', models.PositiveIntegerField(default=0, verbose_name='支持数')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='users.Doctor', verbose_name='作者')),
            ],
            options={
                'verbose_name': '回答',
                'verbose_name_plural': '回答',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('department', models.CharField(choices=[('妇科', (('GYN', '妇科'),)), ('儿科', (('PAE', '小儿科'), ('NEO', '新生儿科'))), ('内科', (('PNE', '呼吸内科'), ('CAR', '心血管内科'), ('NEU', '神经内科'), ('GAS', '消化内科'), ('NEP', '肾内科'), ('END', '内分泌与代谢科'), ('RHE', '风湿免疫科'), ('HAE', '血液病科'), ('INF', '感染科'))), ('皮肤性病科', (('DER', '皮肤科'), ('STD', '性病科'))), ('营养科', (('NUT', '营养科'),)), ('骨伤科', (('SPI', '脊柱科'), ('JOI', '关节科'), ('TRA', '创伤科'))), ('男科', (('AND', '男科'),)), ('外科', (('THO', '胸外科'), ('CSG', '心脏与血管外科'), ('NSG', '神经外科'), ('HEP', '肝胆外科'), ('BUR', '烧伤科'), ('REH', '康复科'), ('URO', '泌尿外科'), ('ANO', '肛肠科'), ('GSG', '普外科'), ('TAB', '甲状腺乳腺科'))), ('肿瘤及防治科', (('IMO', '肿瘤内科'), ('TUM', '肿瘤外科'), ('RAD', '介入与放疗中心'), ('TTU', '肿瘤中医科'))), ('中医科', (('TIM', '中医内科'), ('TSG', '中医外科'), ('TGY', '中医妇科'), ('TAN', '中医男科'), ('TPE', '中医儿科'))), ('口腔颌面科', (('OAM', '口腔颌面科'),)), ('耳鼻咽喉科', (('OTO', '耳科'), ('NAS', '鼻科'), ('THR', '咽喉科'))), ('眼科', (('OPH', '眼科'),)), ('整形美容科', (('PLA', '整形美容科'),)), ('精神心理科', (('PSY', '精神科'), ('PCH', '心理科'))), ('产科', (('PLA', '产科'),)), ('报告解读科', (('CLI', '检验科'), ('RDL', '放射科'), ('ESC', '内镜科'), ('PAT', '病理科'), ('ECG', '心电图科'), ('ULT', '超声科'), ('ANE', '麻醉科'), ('MEX', '体检中心'), ('PRE', '预防保健科')))], max_length=3, verbose_name='科室')),
                ('body', models.TextField(verbose_name='内容')),
                ('solved', models.BooleanField(default=False, verbose_name='已解决')),
                ('stars', models.IntegerField(default=0, verbose_name='关注人数')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='最近更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('patient', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.Patient', verbose_name='提问者')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='qa.Question', verbose_name='问题'),
        ),
    ]
