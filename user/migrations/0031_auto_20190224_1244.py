# Generated by Django 2.0 on 2019-02-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_integralgoods_integralorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='log_ip',
            field=models.CharField(default='', max_length=100, verbose_name='登录IP'),
        ),
        migrations.AlterField(
            model_name='user',
            name='reg_ip',
            field=models.CharField(default='', max_length=100, verbose_name='注册IP'),
        ),
    ]
