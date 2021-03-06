# Generated by Django 2.0 on 2018-12-02 09:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='学校名称')),
                ('province', models.CharField(default='', max_length=20, verbose_name='学校省')),
                ('city', models.CharField(default='', max_length=20, verbose_name='学校市')),
            ],
            options={
                'verbose_name': '学校信息',
                'verbose_name_plural': '学校信息',
                'db_table': 'dn_school',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_num', models.CharField(default='', max_length=13, verbose_name='手机号')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('nick', models.CharField(default='', max_length=30, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='female', max_length=6)),
                ('head_image', models.ImageField(default='', upload_to='users/%Y/%m', verbose_name='用户头像')),
                ('head_qn_url', models.CharField(max_length=100, verbose_name='七牛头像地址')),
                ('account_num', models.CharField(max_length=20, verbose_name='等号')),
                ('my_sign', models.CharField(default='', max_length=128, verbose_name='个性签名')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('real_name', models.CharField(default='', max_length=30, verbose_name='真实姓名')),
                ('school_name', models.CharField(default='', max_length=50, verbose_name='学校')),
                ('college_name', models.CharField(default='', max_length=50, verbose_name='学院')),
                ('major', models.CharField(default='', max_length=50, verbose_name='专业')),
                ('token', models.CharField(max_length=100, verbose_name='身份令牌')),
                ('device_num', models.CharField(max_length=50, verbose_name='设备号')),
                ('create_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')),
                ('integral', models.CharField(max_length=30, verbose_name='积分')),
                ('is_delete', models.SmallIntegerField(choices=[(0, '正常'), (1, '已销户')], default=0, verbose_name='销户')),
                ('is_school_auth', models.SmallIntegerField(choices=[(0, '未认证'), (1, '已认证')], default=0, verbose_name='学生认证')),
                ('is_real_name_auth', models.SmallIntegerField(choices=[(0, '未认证'), (1, '已认证')], default=0, verbose_name='实名认证')),
                ('is_official_auth', models.SmallIntegerField(choices=[(0, '未认证'), (1, '已认证')], default=0, verbose_name='官方认证')),
                ('is_alipay_auth', models.SmallIntegerField(choices=[(0, '未认证'), (1, '已认证')], default=0, verbose_name='支付宝认证')),
                ('school_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='学校id')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 'dn_user',
            },
        ),
    ]
