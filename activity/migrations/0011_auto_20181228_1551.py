# Generated by Django 2.0 on 2018-12-28 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_auto_20181206_1955'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitycomment',
            options={'verbose_name': '校园活动·评论', 'verbose_name_plural': '校园活动·评论'},
        ),
        migrations.AddField(
            model_name='activitycomment',
            name='is_show',
            field=models.SmallIntegerField(choices=[(0, '显示'), (1, '已删除')], default=0, verbose_name='是否显示'),
        ),
    ]
