# Generated by Django 2.0 on 2018-12-14 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moment', '0008_auto_20181213_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_img', models.CharField(default='', max_length=100, verbose_name='七牛云地址')),
                ('local_img', models.ImageField(default='', upload_to='moment_comment_img/%Y/%m/%d', verbose_name='本地地址')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '发现·评论·图片',
                'verbose_name_plural': '发现·评论·图片',
                'db_table': 'dn_moment_comment_image',
            },
        ),
        migrations.CreateModel(
            name='CommentVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_video', models.CharField(default='', max_length=100, verbose_name='七牛云地址')),
                ('local_video', models.FileField(default='', upload_to='moment_comment_video/%Y/%m/%d', verbose_name='本地地址')),
                ('qiniu_video_img', models.CharField(default='', max_length=100, verbose_name='七牛云视频缩略图')),
                ('local_video_img', models.ImageField(default='', upload_to='moment_video/%Y/%m/%d', verbose_name='本地视频缩略图')),
                ('video_size', models.CharField(default='', max_length=20, verbose_name='视频大小')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '发现·评论·视频',
                'verbose_name_plural': '发现·评论·视频',
                'db_table': 'dn_moment_comment_video',
            },
        ),
        migrations.CreateModel(
            name='CommentVoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_voice', models.CharField(default='', max_length=100, verbose_name='七牛云地址')),
                ('local_voice', models.FileField(default='', upload_to='moment_comment_voice/%Y/%m/%d', verbose_name='本地地址')),
                ('voice_time', models.CharField(default='', max_length=20, verbose_name='音频时长')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '发现·评论·语音',
                'verbose_name_plural': '发现·评论·语音',
                'db_table': 'dn_moment_comment_voice',
            },
        ),
        migrations.RemoveField(
            model_name='comment',
            name='local_img',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='local_voice',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='qiniu_img',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='qiniu_voice',
        ),
        migrations.AddField(
            model_name='comment',
            name='is_show',
            field=models.SmallIntegerField(choices=[(0, '未删除'), (1, '已经删除')], default=0, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='comment',
            name='replay_num',
            field=models.IntegerField(default=0, verbose_name='评论回复数量'),
        ),
        migrations.AddField(
            model_name='moment',
            name='is_global',
            field=models.SmallIntegerField(choices=[(0, '未删除'), (1, '已经删除')], default=1, verbose_name='是否同步全国'),
        ),
        migrations.AlterField(
            model_name='image',
            name='local_img',
            field=models.ImageField(default='', upload_to='moment_img/%Y/%m/%d', verbose_name='本地地址'),
        ),
        migrations.AlterField(
            model_name='moment',
            name='is_show',
            field=models.SmallIntegerField(choices=[(0, '未删除'), (1, '已经删除')], default=0, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='video',
            name='moment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='发现id'),
        ),
        migrations.AlterModelTable(
            name='commentgood',
            table='dn_moment_comment_good',
        ),
        migrations.AddField(
            model_name='commentvoice',
            name='comment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Comment', verbose_name='评论id'),
        ),
        migrations.AddField(
            model_name='commentvideo',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Comment', verbose_name='评论id'),
        ),
        migrations.AddField(
            model_name='commentimage',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Comment', verbose_name='评论id'),
        ),
    ]
