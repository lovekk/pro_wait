# Generated by Django 2.0 on 2018-12-20 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moment', '0010_replycomment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='publish_datetime',
            field=models.DateTimeField(auto_now_add=True, default='2018-12-20 23:23:23.11', verbose_name='添加时间'),
            preserve_default=False,
        ),
    ]