from __future__ import unicode_literals
import uuid

from django.db import models
from djgeojson.fields import PointField
from django_countries.fields import CountryField
from select_multiple_field.models import SelectMultipleField
from django.core.exceptions import ValidationError
from django.core.validators import int_list_validator, MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from survey.models import Record

from datetime import datetime
from django.utils import dateformat

class FollowUp(models.Model):

    class Meta: 
        verbose_name = _("HRD Case Follow-Up")

    def __unicode__(self):
        return "%s (%s)" % (self.case.person_id, self.case.name)
    
    # Additional model validation
    def clean(self):
        super(FollowUp, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        super(FollowUp, self).save(*args, **kwargs) # Call the "real" save() method.

    FAMILIARITY_CHOICES = (
        (1, _("I am very familiar with the case.")),
        (2, _("I have information but it might be incomplete.")),
        (3, _("I only have little information.")),
        (4, _("I don't have any information.")),
    )
    RATING_CHOICES = (
        (1, _("Much better")),
        (2, _("Somewhat better")),
        (3, _("Situation stayed the same overall")),
        (4, _("Somewhat worse")),
        (5, _("Much worse")),
        (6, _("I don't know"))
    )
    ATTENTION_CHOICES = (
        (1, _("For sure")),
        (2, _("Probably")),
        (3, _("Rather not")),
        (4, _("Definitely not")),
        (6, _("I don't know"))
    )

    # Data model implementation
    case = models.OneToOneField(
        Record,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="followup",
        verbose_name = _('Case')
    )
    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name = _('Unique ID')
    )
    timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name = _('Timestamp')
    )
    language = models.CharField(
        default = "en",
        max_length=7,
        choices=settings.LANGUAGES,
        verbose_name = _('Language')
    )
    familiarity = models.IntegerField(
        choices=FAMILIARITY_CHOICES,
        default=4,
        null=True,
        verbose_name = _('Level of familiarity')
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=6,
        null=True,
        verbose_name = _('Rating')
    )
    incident_date_1 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYYY-MM-DD")
    )
    incident_text_1 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )

    incident_date_2 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYYY-MM-DD")
    )
    incident_text_2 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )

    incident_date_3 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYYY-MM-DD")
    )
    incident_text_3 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )

    incident_date_4 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYYY-MM-DD")
    )
    incident_text_4 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )
    incident_date_5 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYYY-MM-DD")
    )
    incident_text_5 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )
    attention = models.IntegerField(
        choices=ATTENTION_CHOICES,
        default=6,
        null=True,
        verbose_name = _('Attention impact')
    )
    impact = models.TextField(
        blank=True,
        verbose_name=_("Details about impact"),
    )
    further_comments = models.TextField(
        blank=True,
        verbose_name=_("Further comments"),
    )
    want_informed = models.BooleanField(
        default = False,
        blank=True,
        verbose_name=_("I want to be informed about the outcome of this study")
    )
    contact_again = models.BooleanField(
        default = False,
        blank=True,
        verbose_name=_("You can contact me again if you have further questions about this case")
    )
    email_address = models.EmailField(
        default=None,
        blank=True,
        null=True,
        verbose_name=_("Email address"),
    )
    is_answered = models.BooleanField(
        default = False,
        verbose_name=_("Follow-up form answered")
    )
    is_processed = models.BooleanField(
        default = False,
        verbose_name=_("Follow-up processed")
    )
    internal_comments = models.TextField(
        blank=True,
        verbose_name=_("Internal comments"),
    )
