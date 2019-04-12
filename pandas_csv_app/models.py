from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class ColumnCheck(models.Model):
    name = models.CharField(max_length=255)
    null_values = models.BooleanField
    special_characters = models.BooleanField
    allowed_values = ArrayField(models.CharField(max_length=255), blank=True, default='')
