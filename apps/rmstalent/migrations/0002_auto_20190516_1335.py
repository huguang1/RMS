# Generated by Django 2.1.8 on 2019-05-16 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rmstalent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talent',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '待面试'), (2, '待入职'), (3, '办理签证'), (4, '待分配'), (5, '到岗'), (6, '跳票'), (7, '已放弃'), (8, '离职')]),
        ),
    ]