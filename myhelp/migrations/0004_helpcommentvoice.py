# Generated by Django 2.0 on 2018-12-26 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myhelp', '0003_auto_20181226_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpCommentVoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_voice', models.CharField(default='', max_length=100, verbose_name='七牛云地址')),
                ('local_voice', models.FileField(default='', upload_to='myhelp_comment_voice/%Y/%m/%d', verbose_name='本地地址')),
                ('voice_time', models.CharField(default='', max_length=20, verbose_name='音频时长')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('comment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='myhelp.HelpComment', verbose_name='评论id')),
            ],
            options={
                'verbose_name': '发现·评论·语音',
                'verbose_name_plural': '发现·评论·语音',
                'db_table': 'dn_help_comment_voice',
            },
        ),
    ]
