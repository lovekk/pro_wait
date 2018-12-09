# Generated by Django 2.0 on 2018-12-05 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20181205_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='device_num',
            field=models.CharField(default='', max_length=100, verbose_name='设备号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='integral',
            field=models.CharField(default='1', max_length=30, verbose_name='积分'),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(default='', max_length=100, verbose_name='身份令牌'),
        ),
    ]