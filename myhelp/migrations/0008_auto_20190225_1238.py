# Generated by Django 2.0 on 2019-02-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myhelp', '0007_auto_20190218_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpreplycomment',
            name='content',
            field=models.CharField(default='', max_length=300, verbose_name='评论内容'),
        ),
    ]