# Generated by Django 2.0 on 2018-12-12 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20181212_1827'),
        ('moment', '0005_auto_20181211_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moment.Moment', verbose_name='发现id')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '发现·举报',
                'verbose_name_plural': '发现·举报',
                'db_table': 'dn_moment_report',
            },
        ),
    ]
