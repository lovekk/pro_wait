# Generated by Django 2.0 on 2018-12-28 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lose', '0006_lose_is_show'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lose',
            options={'verbose_name': '失物招领·发布', 'verbose_name_plural': '失物招领·发布'},
        ),
        migrations.AlterModelOptions(
            name='losecomment',
            options={'verbose_name': '失物招领·评论', 'verbose_name_plural': '失物招领·评论'},
        ),
        migrations.AlterModelOptions(
            name='loseimg',
            options={'verbose_name': '失物招领·图片', 'verbose_name_plural': '失物招领·图片'},
        ),
        migrations.AlterModelOptions(
            name='losereplycomment',
            options={'verbose_name': '失物招领·回复评论', 'verbose_name_plural': '失物招领·回复评论'},
        ),
    ]
