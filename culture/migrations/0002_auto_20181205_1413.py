# Generated by Django 2.0 on 2018-12-05 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culture', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='culture',
            name='introduction',
            field=models.TextField(default='', verbose_name='文化简介'),
        ),
        migrations.AlterField(
            model_name='culture_comment',
            name='content',
            field=models.TextField(default='', max_length=100, verbose_name='评论内容'),
        ),
    ]