# Generated by Django 2.0 on 2018-12-02 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20181202_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='is_show',
            field=models.BooleanField(default=False, verbose_name='是否入驻'),
        ),
    ]
