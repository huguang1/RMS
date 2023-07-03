# Generated by Django 2.1.8 on 2019-05-03 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rmsManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='urgencyjobdemand',
            name='hr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='对接人'),
        ),
        migrations.AddField(
            model_name='urgencyjobdemand',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rmsManager.Job', verbose_name='岗位'),
        ),
        migrations.AddField(
            model_name='jobdemand',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rmsManager.Company'),
        ),
        migrations.AddField(
            model_name='jobdemand',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rmsManager.Job', verbose_name='岗位'),
        ),
        migrations.AddField(
            model_name='company',
            name='hr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
