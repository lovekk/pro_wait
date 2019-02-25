# Generated by Django 2.0 on 2019-02-24 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_auto_20190224_1244'),
        ('moment', '0014_auto_20181228_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Push',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('push_content', models.CharField(default='', max_length=300, verbose_name='评论内容')),
                ('comment_date', models.DateField(auto_now_add=True, verbose_name='评论日期')),
                ('comment_time', models.TimeField(auto_now_add=True, verbose_name='评论时间')),
                ('push_type', models.SmallIntegerField(choices=[(0, '说说发现'), (1, '帮助help'), (2, '二手市场'), (3, '失物招领')], default=0, verbose_name='推送类别')),
                ('publish_id', models.IntegerField(default=0, verbose_name='发布内容的id')),
                ('publisher_id', models.IntegerField(default=0, verbose_name='发布者的id')),
                ('commentator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='评论者')),
            ],
            options={
                'verbose_name': '发现·消息推送',
                'verbose_name_plural': '发现·消息推送',
                'db_table': 'dn_moment_push',
            },
        ),
    ]
