# Generated by Django 2.0 on 2018-12-05 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culture', '0003_auto_20181205_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='culturecomment',
            name='content',
            field=models.CharField(default='', max_length=100, verbose_name='评论内容'),
        ),
    ]
