# Generated by Django 2.0 on 2019-01-09 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culture', '0007_auto_20181228_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='culture',
            name='comment_num',
            field=models.IntegerField(default=0, verbose_name='评论数'),
        ),
    ]