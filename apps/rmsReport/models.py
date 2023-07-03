from django.db import models

# Create your models here.
from apps.rmsauth.models import Group


class Target(models.Model):
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    date = models.DateTimeField()
    group_count = models.SmallIntegerField()
    new_resume = models.IntegerField()
    admit_count = models.SmallIntegerField()
    entry_count = models.SmallIntegerField()
    entry_percent = models.CharField(max_length=32)

    class Meta:
        db_table = 'rms_target'
        ordering = ['id']
