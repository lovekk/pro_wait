# Generated by Django 2.0 on 2018-12-27 23:13

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_follow_is_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutWe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50, verbose_name='关于我们标题')),
                ('content', tinymce.models.HTMLField(verbose_name='关于我们内容')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '关于我们',
                'verbose_name_plural': '关于我们',
                'db_table': 'dn_user_about',
            },
        ),
        migrations.CreateModel(
            name='AboutWeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(default='', max_length=120, verbose_name='评论内容')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='评论日期')),
                ('create_time', models.TimeField(auto_now_add=True, verbose_name='评论日期')),
                ('about_we', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.AboutWe', verbose_name='关于我们')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '关于我们评论',
                'verbose_name_plural': '关于我们评论',
                'db_table': 'dn_user_about_comment',
            },
        ),
        migrations.CreateModel(
            name='RecoveryPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_num', models.CharField(default='', max_length=11, verbose_name='登录账户')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='学校')),
            ],
            options={
                'verbose_name': '回收人员',
                'verbose_name_plural': '回收人员',
                'db_table': 'dn_user_recovery_worker',
            },
        ),
    ]
