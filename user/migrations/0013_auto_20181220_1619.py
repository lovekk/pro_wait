# Generated by Django 2.0 on 2018-12-20 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20181212_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='integral',
            field=models.IntegerField(default=0, verbose_name='积分'),
        ),
    ]
