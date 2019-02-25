# Generated by Django 2.0 on 2019-02-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recovery', '0003_auto_20181228_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appoint',
            name='address',
            field=models.CharField(default='', max_length=100, verbose_name='预约地址'),
        ),
        migrations.AlterField(
            model_name='appoint',
            name='phone_num',
            field=models.CharField(default='', max_length=50, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='appoint',
            name='thing_type',
            field=models.CharField(default='', max_length=100, verbose_name='物品类别'),
        ),
        migrations.AlterField(
            model_name='appoint',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='重量小数'),
        ),
        migrations.AlterField(
            model_name='price',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='物品名称'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=6, verbose_name='物品价格'),
        ),
        migrations.AlterField(
            model_name='price',
            name='unit',
            field=models.CharField(default='', max_length=20, verbose_name='物品单位'),
        ),
    ]
