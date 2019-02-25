# Generated by Django 2.0 on 2019-02-21 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0029_auto_20190218_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegralGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10, verbose_name='商品名称')),
                ('price', models.IntegerField(default='100', verbose_name='商品价格')),
                ('desc', models.CharField(default='', max_length=200, verbose_name='商品描述')),
                ('image', models.ImageField(default='', upload_to='user_shop/%Y/%m/%d', verbose_name='商品图片')),
            ],
            options={
                'verbose_name': '用户·积分商城',
                'verbose_name_plural': '用户·积分商城',
                'db_table': 'dn_user_shop',
            },
        ),
        migrations.CreateModel(
            name='IntegralOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_num', models.CharField(default='', max_length=15, verbose_name='手机号')),
                ('address', models.CharField(default='', max_length=50, verbose_name='收货地址')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='订单时间')),
                ('change_date', models.DateField(auto_now=True, verbose_name='修改时间')),
                ('status', models.SmallIntegerField(choices=[(0, '未发货'), (1, '已经发货')], default=0, verbose_name='是否发货')),
                ('which_school', models.CharField(default='', max_length=30, verbose_name='学校')),
                ('good', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.IntegralGoods', verbose_name='商品')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='收货人')),
            ],
            options={
                'verbose_name': '用户·积分订单',
                'verbose_name_plural': '用户·积分订单',
                'db_table': 'dn_user_shop_order',
            },
        ),
    ]
