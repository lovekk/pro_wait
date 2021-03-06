# Generated by Django 2.0 on 2019-01-23 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_auto_20190122_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daima', models.CharField(max_length=50, verbose_name='课程编码')),
                ('xueqi', models.CharField(max_length=50, verbose_name='学期')),
                ('name', models.CharField(max_length=50, verbose_name='课程名字')),
                ('number', models.CharField(max_length=20, verbose_name='分数')),
                ('is_pass', models.CharField(max_length=50, verbose_name='是否通过')),
                ('xuefen', models.CharField(max_length=50, verbose_name='学分')),
                ('leibie', models.CharField(max_length=50, verbose_name='课程类别')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='学校')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户·成绩',
                'verbose_name_plural': '用户·成绩',
                'db_table': 'dn_user_score',
            },
        ),
        migrations.CreateModel(
            name='Kb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yi1', models.CharField(max_length=100)),
                ('yi2', models.CharField(max_length=100)),
                ('yi3', models.CharField(max_length=100)),
                ('yi4', models.CharField(max_length=100)),
                ('yi5', models.CharField(max_length=100)),
                ('yi6', models.CharField(max_length=100)),
                ('yi7', models.CharField(max_length=100)),
                ('er1', models.CharField(max_length=100)),
                ('er2', models.CharField(max_length=100)),
                ('er3', models.CharField(max_length=100)),
                ('er4', models.CharField(max_length=100)),
                ('er5', models.CharField(max_length=100)),
                ('er6', models.CharField(max_length=100)),
                ('er7', models.CharField(max_length=100)),
                ('san1', models.CharField(max_length=100)),
                ('san2', models.CharField(max_length=100)),
                ('san3', models.CharField(max_length=100)),
                ('san4', models.CharField(max_length=100)),
                ('san5', models.CharField(max_length=100)),
                ('san6', models.CharField(max_length=100)),
                ('san7', models.CharField(max_length=100)),
                ('si1', models.CharField(max_length=100)),
                ('si2', models.CharField(max_length=100)),
                ('si3', models.CharField(max_length=100)),
                ('si4', models.CharField(max_length=100)),
                ('si5', models.CharField(max_length=100)),
                ('si6', models.CharField(max_length=100)),
                ('si7', models.CharField(max_length=100)),
                ('wu1', models.CharField(max_length=100)),
                ('wu2', models.CharField(max_length=100)),
                ('wu3', models.CharField(max_length=100)),
                ('wu4', models.CharField(max_length=100)),
                ('wu5', models.CharField(max_length=100)),
                ('wu6', models.CharField(max_length=100)),
                ('wu7', models.CharField(max_length=100)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.School', verbose_name='学校')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户·课表',
                'verbose_name_plural': '用户·课表',
                'db_table': 'dn_user_class',
            },
        ),
    ]
