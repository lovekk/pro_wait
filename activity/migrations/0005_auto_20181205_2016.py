# Generated by Django 2.0 on 2018-12-05 12:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_activity_is_first'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='创立时间'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='introduction',
            field=models.TextField(default='', verbose_name='活动简介'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='publish_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='发表日期'),
        ),
        migrations.AlterField(
            model_name='activitycomment',
            name='content',
            field=models.CharField(default='', max_length=100, verbose_name='评论内容'),
        ),
    ]
