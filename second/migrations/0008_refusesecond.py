# Generated by Django 2.0 on 2019-03-19 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_auto_20190224_1244'),
        ('second', '0007_auto_20190225_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefuseSecond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_datetime', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('second', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='second.Second', verbose_name='二手id')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '校园二手·屏蔽',
                'verbose_name_plural': '校园二手·屏蔽',
                'db_table': 'dn_second_refuse',
            },
        ),
    ]
