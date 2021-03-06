# Generated by Django 2.0 on 2019-02-25 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_auto_20190108_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(default='', max_length=30, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='article',
            name='editor',
            field=models.CharField(default='', max_length=30, verbose_name='编辑人员'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='文章标题'),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='content',
            field=models.CharField(default='', max_length=300, verbose_name='评论内容'),
        ),
    ]
