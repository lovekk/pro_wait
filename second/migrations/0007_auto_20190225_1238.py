# Generated by Django 2.0 on 2019-02-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second', '0006_secondreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='second',
            name='content',
            field=models.CharField(default='', max_length=500, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='secondcomment',
            name='content',
            field=models.CharField(default='', max_length=300, verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='secondreplycomment',
            name='content',
            field=models.CharField(default='', max_length=300, verbose_name='评论内容'),
        ),
    ]