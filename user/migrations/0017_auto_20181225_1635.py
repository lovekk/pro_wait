# Generated by Django 2.0 on 2018-12-25 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_auto_20181223_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='functionmodule',
            name='module_name',
            field=models.CharField(default='', max_length=30, verbose_name='模块名称'),
        ),
    ]
