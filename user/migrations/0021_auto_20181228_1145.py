# Generated by Django 2.0 on 2018-12-28 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_recoveryperson_is_use'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recoveryperson',
            options={'verbose_name': '工作回收人员', 'verbose_name_plural': '工作回收人员'},
        ),
    ]
