# Generated by Django 2.0 on 2018-12-06 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20181205_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish_datetime',
            field=models.DateTimeField(auto_now_add=True, default='2018-11-11 11:11:11', verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='create_date',
            field=models.DateField(auto_now_add=True, default='2018-11-11', verbose_name='创建日期'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='发表日期'),
        ),
    ]
