# Generated by Django 2.0 on 2018-12-28 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recovery', '0002_auto_20181228_1145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appoint',
            options={'verbose_name': '回收·预约', 'verbose_name_plural': '回收·预约'},
        ),
        migrations.AlterModelOptions(
            name='bag',
            options={'verbose_name': '回收·袋子编号', 'verbose_name_plural': '回收·袋子编号'},
        ),
        migrations.AlterModelOptions(
            name='introduction',
            options={'verbose_name': '回收·环保知识介绍', 'verbose_name_plural': '回收·环保知识介绍'},
        ),
        migrations.AlterModelOptions(
            name='myrank',
            options={'verbose_name': '回收·排名榜', 'verbose_name_plural': '回收·排名榜'},
        ),
        migrations.AlterModelOptions(
            name='price',
            options={'verbose_name': '回收·物品价格', 'verbose_name_plural': '回收·物品价格'},
        ),
        migrations.AlterModelOptions(
            name='tips',
            options={'verbose_name': '回收·学校提示', 'verbose_name_plural': '回收·学校提示'},
        ),
    ]
