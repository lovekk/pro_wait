# Generated by Django 2.0 on 2018-12-28 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20181206_2309'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '九点读书·文章', 'verbose_name_plural': '九点读书·文章'},
        ),
        migrations.AlterModelOptions(
            name='articlecomment',
            options={'verbose_name': '九点读书·评论', 'verbose_name_plural': '九点读书·评论'},
        ),
    ]