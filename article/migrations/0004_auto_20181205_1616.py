# Generated by Django 2.0 on 2018-12-05 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20181205_1616'),
        ('article', '0003_article_list_img'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Article_comment',
            new_name='ArticleComment',
        ),
    ]
