# Generated by Django 2.0 on 2018-12-10 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0011_auto_20181210_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=100, verbose_name='评论内容')),
                ('qiniu_img', models.CharField(default='', max_length=100, verbose_name='评论图片七牛云')),
                ('local_img', models.ImageField(default='', upload_to='moment/%Y/%m/%d', verbose_name='评论图片本地')),
                ('qiniu_voice', models.CharField(default='', max_length=100, verbose_name='评论语音七牛云')),
                ('local_voice', models.FileField(default='', upload_to='moment_voice/%Y/%m/%d', verbose_name='评论语音本地')),
                ('comment_date', models.DateField(auto_now_add=True, verbose_name='评论日期')),
                ('comment_time', models.TimeField(auto_now_add=True, verbose_name='评论时间')),
                ('good_num', models.IntegerField(default=0, verbose_name='点赞数量')),
            ],
            options={
                'verbose_name': '发现·评论',
                'verbose_name_plural': '发现·评论',
                'db_table': 'dn_moment_comment',
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crate_datetime', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
            ],
            options={
                'verbose_name': '发现·点赞',
                'verbose_name_plural': '发现·点赞',
                'db_table': 'dn_moment_good',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_img', models.CharField(default='', max_length=100, verbose_name='七牛云地址')),
                ('local_img', models.ImageField(default='', upload_to='moment/%Y/%m/%d', verbose_name='本地地址')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '发现·图片',
                'verbose_name_plural': '发现·图片',
                'db_table': 'dn_moment_image',
            },
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=500, verbose_name='动态内容')),
                ('publish_date', models.DateField(auto_now_add=True, verbose_name='发表时间')),
                ('publish_time', models.TimeField(auto_now_add=True, verbose_name='发表时间')),
                ('tag', models.CharField(default='', max_length=30, verbose_name='标签')),
                ('good_num', models.IntegerField(default=0, verbose_name='点赞数量')),
                ('comment_num', models.IntegerField(default=0, verbose_name='评论数量')),
                ('view_num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('relay_num', models.IntegerField(default=0, verbose_name='转发量')),
                ('report_num', models.IntegerField(default=0, verbose_name='举报数')),
                ('is_first', models.SmallIntegerField(choices=[(0, '未置顶'), (1, '置顶')], default=0, verbose_name='置顶')),
                ('is_show', models.SmallIntegerField(choices=[(0, '未置顶'), (1, '置顶')], default=0, verbose_name='是否删除')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='学校')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '发现·动态内容',
                'verbose_name_plural': '发现·动态内容',
                'db_table': 'dn_moment',
            },
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=100, verbose_name='评论内容')),
                ('comment_date', models.DateField(auto_now_add=True, verbose_name='回复评论日期')),
                ('comment_time', models.TimeField(auto_now_add=True, verbose_name='回复评论时间')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Comment', verbose_name='评论')),
                ('moment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='发现')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '发现·回复评论',
                'verbose_name_plural': '发现·回复评论',
                'db_table': 'dn_moment_comment_reply',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='标签名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '发现·标签',
                'verbose_name_plural': '发现·标签',
                'db_table': 'dn_moment_tag',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_video', models.CharField(default='', max_length=100, verbose_name='七牛云地址')),
                ('local_video', models.FileField(default='', upload_to='moment_video/%Y/%m/%d', verbose_name='本地地址')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('moment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='发现id')),
            ],
            options={
                'verbose_name': '发现·视频',
                'verbose_name_plural': '发现·视频',
                'db_table': 'dn_moment_video',
            },
        ),
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_voice', models.CharField(default='', max_length=100, verbose_name='七牛云地址')),
                ('local_voice', models.FileField(default='', upload_to='moment_voice/%Y/%m/%d', verbose_name='本地地址')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('moment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='发现id')),
            ],
            options={
                'verbose_name': '发现·语音',
                'verbose_name_plural': '发现·语音',
                'db_table': 'dn_moment_voice',
            },
        ),
        migrations.AddField(
            model_name='image',
            name='moment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='发现id'),
        ),
        migrations.AddField(
            model_name='good',
            name='find',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='关联发现id'),
        ),
        migrations.AddField(
            model_name='good',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='关联用户id'),
        ),
        migrations.AddField(
            model_name='comment',
            name='moment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='发现'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户'),
        ),
    ]
