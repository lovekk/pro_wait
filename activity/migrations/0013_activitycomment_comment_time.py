# Generated by Django 2.0 on 2019-01-13 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0012_remove_activitycomment_comment_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitycomment',
            name='comment_time',
            field=models.TimeField(auto_now_add=True, default='11:11:11.11', verbose_name='创建时间'),
            preserve_default=False,
        ),
    ]
