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

    RATING_CHOICES = (
        (1, _("Much worse")),
        (2, _("Somewhat worse")),
        (3, _("Not better, not worse / or alternating")),
        (4, _("Somewhat better")),
        (5, _("Much better")),
        (6, _("I don't know"))
    )
    ATTENTION_CHOICES = (
        (1, _("Definitely not")),
        (2, _("Rather not")),
        (3, _("Probably")),
        (4, _("For sure")),
        (6, _("I don't know"))
    )

    # Data model implementation
    case = models.OneToOneField(
        Record,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="followup"
    )
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name = _('Timestamp')
    )
    language = models.CharField(
        default = "en",
        max_length=7,
        choices=settings.LANGUAGES
    )
    incident_date_1 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYY-MM-DD")
    )
    incident_text_1 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )

    incident_date_2 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYY-MM-DD")
    )
    incident_text_2 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )

    incident_date_3 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYY-MM-DD")
    )
    incident_text_3 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )

    incident_date_4 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYY-MM-DD")
    )
    incident_text_4 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )
    incident_date_5 = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the incident"),
        help_text=_("Format YYY-MM-DD")
    )
    incident_text_5 = models.TextField(
        blank=True,
        verbose_name=_("Brief description of the incident"),
    )
    impact = models.TextField(
        blank=True,
        verbose_name=_("Details about impact"),
    )
    further_comments = models.TextField(
        blank=True,
        verbose_name=_("Further comments"),
        help_text=_("Observations that might be relevant but don't fit elsewhere")
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
        help_text=_("please note that by submitting your email address, your contact will be known by and can be connected to this case by the independent researcher carrying out the analysis. If you don't indicate your contact details, your submission will remain anonymous")
    )
    is_answered = models.BooleanField(
        default = False,
        verbose_name=_("Follow-up form answered")
    )
    is_processed = models.BooleanField(
        default = False,
        verbose_name=_("Follow-up processed")
    )
