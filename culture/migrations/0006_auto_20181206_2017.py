# Generated by Django 2.0 on 2018-12-06 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culture', '0005_auto_20181205_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='culturecomment',
            name='create_date',
            field=models.DateField(auto_now_add=True, default='2018-11-11', verbose_name='创建日期'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='culture',
            name='publish_date',
            field=models.DateField(auto_now_add=True, verbose_name='发表日期'),
        ),
    ]
