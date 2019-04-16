from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class ColumnCheck(models.Model):
    name = models.CharField(max_length=255)
    null_values = models.BooleanField(default=False)
    special_characters = models.BooleanField(default=False)
    allowed_values = ArrayField(models.CharField(max_length=255, blank=True), default=list)
    min = models.FloatField(null=True, blank=True, default=None)
    max = models.FloatField(null=True, blank=True, default=None)
    min_allowed = models.FloatField(null=True, blank=True, default=None)
    max_allowed = models.FloatField(null=True, blank=True, default=None)
    min_date = models.DateField(null=True, blank=True, default=None)
    max_date = models.DateField(null=True, blank=True, default=None)
    min_allowed_date = models.DateField(null=True, blank=True, default=None)
    max_allowed_date = models.DateField(null=True, blank=True, default=None)
