# Generated by Django 2.0 on 2018-12-05 04:56

import datetime
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0006_auto_20181203_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50, verbose_name='公告标题')),
                ('content', tinymce.models.HTMLField(verbose_name='公告内容')),
                ('editor', models.CharField(default='', max_length=10, verbose_name='编辑人员')),
                ('publish_date', models.DateField(default=datetime.datetime.now, verbose_name='发表时间')),
                ('view_num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='学校')),
            ],
            options={
                'verbose_name': '校园公告',
                'verbose_name_plural': '校园公告',
                'db_table': 'dn_notice',
            },
        ),
    ]