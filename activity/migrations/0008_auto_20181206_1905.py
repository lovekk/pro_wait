# Generated by Django 2.0 on 2018-12-06 19:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_activity_is_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitycomment',
            name='comment_datetime',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='评论时间'),
        ),
        migrations.AlterField(
            model_name='activitycomment',
            name='comment_date',
            field=models.DateField(auto_now_add=True, verbose_name='评论时间'),
        ),
    ]
