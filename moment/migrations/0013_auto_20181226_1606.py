# Generated by Django 2.0 on 2018-12-26 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moment', '0012_auto_20181225_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moment',
            name='publish_date',
            field=models.DateField(auto_now_add=True, verbose_name='发表日期'),
        ),
    ]
