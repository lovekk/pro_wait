# Generated by Django 2.0 on 2018-12-05 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_comment',
            name='content',
            field=models.TextField(default='', max_length=100, verbose_name='评论内容'),
        ),
    ]
