# Generated by Django 2.0 on 2018-12-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20181205_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='head_image',
            field=models.ImageField(default='', upload_to='user/%Y/%m/%d', verbose_name='用户头像'),
        ),
    ]