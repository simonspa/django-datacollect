from __future__ import unicode_literals
import uuid

from django.db import models
from djgeojson.fields import PointField
from django_countries.fields import CountryField
from select_multiple_field.models import SelectMultipleField
from django.core.exceptions import ValidationError
from django.core.validators import int_list_validator, MinLengthValidator
from django.contrib.auth.models import User

from survey.models import Record

from datetime import datetime
from django.utils import dateformat

class FollowUp(models.Model):

    class Meta: 
        verbose_name = "HRD Case Follow-Up"

    def __unicode__(self):
        return "%s (%s)" % (self.case.person_id, self.case.name)
    
    # Additional model validation
    def clean(self):
        super(FollowUp, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        super(FollowUp, self).save(*args, **kwargs) # Call the "real" save() method.

    
    # Data model implementation
    case = models.OneToOneField(
        Record,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(
        null=True,
        blank=True
    )
    further_comments = models.TextField(
        blank=True,
        verbose_name="Further comments",
        help_text="Observations that might be relevant but don't fit elsewhere"
    )
    is_answered = models.BooleanField(
        default = False,
        verbose_name="Follow-up form answered"
    )
