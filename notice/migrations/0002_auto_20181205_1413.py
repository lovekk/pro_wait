# Generated by Django 2.0 on 2018-12-05 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(default='', max_length=60, verbose_name='公告标题'),
        ),
    ]