# Generated by Django 2.1.8 on 2019-05-07 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rmsManager', '0003_auto_20190506_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='hr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companys', to=settings.AUTH_USER_MODEL),
        ),
    ]