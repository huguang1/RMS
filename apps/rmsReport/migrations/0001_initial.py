# Generated by Django 2.1.8 on 2019-05-12 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rmsauth', '0003_auto_20190507_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('group_count', models.SmallIntegerField()),
                ('new_resume', models.IntegerField()),
                ('admit_count', models.SmallIntegerField()),
                ('entry_count', models.SmallIntegerField()),
                ('entry_percent', models.FloatField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rmsauth.Group')),
            ],
            options={
                'db_table': 'rms_target',
                'ordering': ['id'],
            },
        ),
    ]