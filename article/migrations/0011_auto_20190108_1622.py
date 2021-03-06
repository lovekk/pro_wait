# Generated by Django 2.0 on 2019-01-08 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20190108_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_all_school',
            field=models.SmallIntegerField(choices=[(0, '不同步'), (1, '同步全国')], default=0, verbose_name='同步全国'),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_original',
            field=models.SmallIntegerField(choices=[(0, '不是原创'), (1, '原创')], default=0, verbose_name='原创'),
        ),
    ]
