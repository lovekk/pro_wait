# Generated by Django 2.0 on 2018-12-09 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0010_auto_20181205_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Second',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=300, verbose_name='内容')),
                ('price', models.IntegerField(default=0, verbose_name='价格')),
                ('view_num', models.IntegerField(default=0, verbose_name='浏览量')),
                ('good_num', models.IntegerField(default=0, verbose_name='点赞数')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('create_time', models.TimeField(auto_now_add=True, verbose_name='时间')),
                ('is_first', models.SmallIntegerField(choices=[(0, '未置顶'), (1, '置顶')], default=0, verbose_name='置顶')),
                ('is_type', models.SmallIntegerField(choices=[(0, '全新'), (1, '九新'), (2, '半新')], default=1, verbose_name='新型')),
                ('is_sale', models.SmallIntegerField(choices=[(0, '未售出'), (1, '已出')], default=0, verbose_name='出售')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='发布者')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='学校')),
            ],
            options={
                'verbose_name': '校园二手发布',
                'verbose_name_plural': '校园二手发布',
                'db_table': 'dn_second',
            },
        ),
        migrations.CreateModel(
            name='SecondImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qiniu_img', models.CharField(default='', max_length=100, verbose_name='七牛地址')),
                ('local_img', models.ImageField(default='', upload_to='lose/%Y/%m/%d', verbose_name='本地地址')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='日期时间')),
                ('second', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='second.Second', verbose_name='校园二手')),
            ],
            options={
                'verbose_name': '校园二手图片',
                'verbose_name_plural': '校园二手图片',
                'db_table': 'dn_second_img',
            },
        ),
    ]
