# Generated by Django 2.0 on 2019-02-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0004_notice_is_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='editor',
            field=models.CharField(default='', max_length=30, verbose_name='编辑人员'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='公告标题'),
        ),
    ]
