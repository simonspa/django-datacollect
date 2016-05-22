from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Record(models.Model):
    name = models.CharField(max_length=500)
    branch = models.CharField(max_length=500)
    GENDER_CHOICES = (
      ("M", "Male"),
      ("F", "Female"),
      ("O", "Other"),
      ("?", "Unknown")
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="?"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
