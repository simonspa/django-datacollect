from __future__ import unicode_literals

from django.db import models
from djgeojson.fields import PointField
from django_countries.fields import CountryField
from select_multiple_field.models import SelectMultipleField
from django.core.exceptions import ValidationError
from django.core.validators import int_list_validator, MinLengthValidator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import json
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim
from datetime import datetime
from django.utils import dateformat

def update_filename(instance, filename):
    return '{0}/{1}'.format(instance.person_id, filename)

class Record(models.Model):

    class Meta: 
        verbose_name = "HRD Record"

    def __unicode__(self):
        return "%s (%s)" % (self.person_id, self.name)
    
    # Additional model valiation

    def clean(self):
        super(Record, self).clean()

        if self.date_govreply and not self.govreply_content:
            raise ValidationError('With a government reply date set, a reply content is required')
        if self.date_govaction and not self.govreply_action:
            raise ValidationError('With a government reply date set, a reply content is required')
        if self.type_intervention == 'JUA' or self.type_intervention == 'JAL':
            if not self.joint_with or (len(self.joint_with) == 1 and not self.joint_with[0]):
                raise ValidationError('Select joint intervention type, required for JUA and JAL.')

        # Communication dates: check for sensible time order
        if self.date_govreply and self.date_intervention and self.date_govreply < self.date_intervention:
            raise ValidationError('Date of government reply has to be past the date of intervention.')
        if self.date_intervention and self.date_incident and self.date_intervention < self.date_incident:
            raise ValidationError('Date of intervention has to be past the date of the incident.')
        if self.date_govreply and self.date_incident and self.date_govreply < self.date_incident:
            raise ValidationError('Date of government reply has to be past the date of the incident.')

        
        # Violations: Auto-add top-level entries when sub-cat is selected
        if not "AD" in self.violations:
            if any(True for x in self.violations if x in ["IC","PC","RT"]):
                self.violations.append("AD")
        if not "KA" in self.violations:
            if any(True for x in self.violations if x in ["KK","K"]):
                self.violations.append("KA")
        if not "P" in self.violations:
            if any(True for x in self.violations if x in ["UT","C"]):
                self.violations.append("P")

        if not "AD" in self.violations2:
            if any(True for x in self.violations2 if x in ["IC","PC","RT"]):
                self.violations2.append("AD")
        if not "KA" in self.violations2:
            if any(True for x in self.violations2 if x in ["KK","K"]):
                self.violations2.append("KA")
        if not "P" in self.violations2:
            if any(True for x in self.violations2 if x in ["UT","C"]):
                self.violations2.append("P")

        if not "AD" in self.violations3:
            if any(True for x in self.violations3 if x in ["IC","PC","RT"]):
                self.violations3.append("AD")
        if not "KA" in self.violations3:
            if any(True for x in self.violations3 if x in ["KK","K"]):
                self.violations3.append("KA")
        if not "P" in self.violations3:
            if any(True for x in self.violations3 if x in ["UT","C"]):
                self.violations3.append("P")

        if not "AD" in self.violations4:
            if any(True for x in self.violations4 if x in ["IC","PC","RT"]):
                self.violations4.append("AD")
        if not "KA" in self.violations4:
            if any(True for x in self.violations4 if x in ["KK","K"]):
                self.violations4.append("KA")
        if not "P" in self.violations4:
            if any(True for x in self.violations4 if x in ["UT","C"]):
                self.violations4.append("P")

        # Fill geolocation:
        self.get_coordinates()
        

    def save(self, *args, **kwargs):
        self.clean()
        super(Record, self).save(*args, **kwargs) # Call the "real" save() method.


    # Choices for select boxes

    GENDER_CHOICES = (
        (0, _("Male")),
        (1, _("Female")),
        (2, _("Trans/inter*")),
        (3, _("Gender unclear"))
    )

    ISSUE_CHOICES = (
        ("?",_("N/A")),
        ("WR",_("Women's rights")),
        ("CRS",_("Children's rights")),
        ("IPR",_("Indigenous peoples' rights")),
        ("LGBTI",_("LGBTI issues")),
        ("MRR",_("Migrants'/refugees'/IDP's rights")),
        ("MR",_("Ethnic minorities' rights")),
        ("LR",_("Labour rights")),
        ("POV",_("Poverty/social welfare")),
        ("RTF",_("Right to food/water")),
        ("HI",_("Health issues")),
        ("RE",_("Right to education")),
        ("HRFE",_("Housing rights/forced evictions")),
        ("LNR",_("Land rights/environment")),
        ("CR",_("Cultural rights")),
        ("RF",_("Religious freedom")),
        ("PR",_("Prisoner's rights")),
        ("AT",_("Torture")),
        ("DP",_("Death penalty")),
        ("ED",_("Enforced disappearance")),
        ("H",_("Homocide")),
        ("PV",_("Police/military violence")),
        ("NSV",_("Non-state violence")),
        ("AC",_("Corruption")),
        ("DV",_("Democratic/voting rights")),
        ("JI",_("Judicial independence")),
        ("IF",_("Internet freedom")),
        ("HRE",_("Human rights education")),
        ("TJ",_("Transitional justice")),
        ("PA",_("Peace activism")),
        ("AR",_("Anti-racism")),
        ("RP",_("Right to privacy")),
    )
    
    ACTIVITIES_CHOICES = (
        ("?",_("N/A")),
        ("CSA",_("Civil society activist")),
        ("TUA",_("Trade union activist")),
        ("RA",_("Religious association")),
        ("PM",_("Politician/Party member")),
        ("CL",_("Community leader")),
        ("L",_("Lawyer/Judge/Attorney")),
        ("J",_("Journalist/Editor")),
        ("CA",_("Cyberactivist")),
        ("A",_("Artist/Writer")),
        ("S",_("Student")),
        ("T",_("Teacher/Professor/Scientist")),
        ("MP",_("Medical professional")),
        ("HW",_("Humanitarian worker")),
        ("V",_("Victim/witness of HR violations")),
        ("OP",_("Ombudsperson/Procuraduria/NHRI")),
        ("UN",_("UN official")),
        ("GAS",_("Government/Army/Security forces")),
        ("I",_("Investigation against officials")),
        ("PC",_("Participation in conference/meeting")),
        ("PP",_("Participation in public protest/rally")),
    )

    COOPERATION_CHOICES = (
        (0,_("Not mentioned")),
        (1,_("UN")),
        (2,_("INGO/other IO")),
    )

    LOCATION_CHOICES = (
        ("C",_("Capital")),
        ("T",_("City/Town")),
        ("R",_("Rural area")),
        ("A",_("Abroad")),
        ("?",_("Unknown"))
    )

    VIOLATION_FAMILY_CHOICES = (
        (0,_("Only HRD")),
        (1,_("against relative")),
        (2,_("against both")),
    )

    VIOLATIONS_CHOICES = (
        ("?",_("N/A")),
        ("AD",_("Arrest/Detention")),
        ("IC",_("Incommunicado")),
        ("PC",_("Held in poor conditions")),
        ("RT",_("Risk of torture")),
        ("TI",_("Torture/Ill-treatment")),
        ("ED",_("Enforced disappearance")),
        ("KA",_("Physical attack")),
        ("KK",_("Killing attempt")),
        ("K",_("Killing")),
        ("DI",_("Kidnapping")),
        ("P",_("Trial")),
        ("UT",_("Unfair trial")),
        ("C",_("Conviction")),
        ("T",_("Threats")),
        ("S",_("Surveillance")),
        ("R",_("Office/home raided")),
        ("PD",_("Property stolen/confiscated/destroyed")),
        ("DC",_("Defamation campaign")),
        ("DP",_("Disciplinary proceedings")),
        ("B",_("Travel restrictions")),
        ("A",_("Access denied")),
        ("VD",_("Expulsion/Visa denied")),
        ("AH",_("Administrative harassment")),
        ("FI",_("Failure to intervene/protect")),
        ("CR",_("Citizenship revoked")),
    )

    PERPETRATOR_CHOICES = (
        ("U",_("Unknown")),
        ("P",_("Police/security forces")),
        ("CS",_("Public official/administration/judiciary")),
        ("A",_("Army")),
        ("AO",_("Armed opposition")),
        ("B",_("Business/landholder")),
        ("M",_("Mob")),
        ("PM",_("Paramilitary group")),
        ("PP",_("Private person")),
        ("RA",_("Religious authority")),
    )

    INTERVENTION_CHOICES = (
        ("?",_("N/A")),
        ("UA",_("UA")),
        ("JUA",_("JUA")),
        ("AL",_("AL")),
        ("JAL",_("JAL")),
        ("PR",_("PR")),
    )

    JOINT_CHOICES = (
        ("FrASSEM",_("FrASSEM")),
        ("FrEXPRESS",_("FrEXPRESS")),
        ("TORTURE",_("TORTURE")),
        ("WGAD",_("WGAD")),
        ("WGED",_("WGED")),
        ("SumEXECU",_("SumEXECU")),
        ("WOMEN",_("WOMEN")),
        ("FrRELIGION",_("FrRELIGION")),
        ("JUDGES",_("JUDGES")),
        ("INDIGENOUS",_("INDIGENOUS")),
        ("TERRORISM",_("TERRORISM")),
        ("BUSINESS",_("BUSINESS")),
        ("HEALTH",_("HEALTH")),
        ("ENVIR",_("ENVIR")),
        ("FOOD",_("FOOD")),
        ("CHILD",_("CHILD")),
        ("RACISM",_("RACISM")),
        ("HOUSING",_("HOUSING")),
        ("MINORITY",_("MINORITY")),
        ("EDUCATION",_("EDUCATION")),
        ("MIGRANTS",_("MIGRANTS")),
        ("WASTE",_("WASTE")),
        ("IDPs",_("IDPs")),
        ("WG_WOMEN",_("WG_WOMEN")),
        ("MERCENARIES",_("MERCENARIES")),
        ("TRUTH",_("TRUTH")),
        ("POVERTY",_("POVERTY")),
        ("CULTURE",_("CULTURE")),
        ("ELDERLY",_("ELDERLY")),
        ("SLAVERY",_("SLAVERY")),
        ("WATER",_("WATER")),
        ("AFRICAN",_("AFRICAN")),
        ("DISCAPA",_("DISCAPA")),
        ("SOLIDAR",_("SOLIDAR")),
        ("INTORDER",_("INT'ORDER")),
        ("TRAFFIC",_("TRAFFIC")),
        ("PRIVACY",_("PRIVACY")),
        ("DEBT",_("DEBT")),
        ("SOGI",_("SOGI")),
        ("specific",_("Country-specific")),
    )

    CONCERN_CHOICES = (
        ("CV",_("Concern over violation")),
        ("PV",_("Concern: Pattern of violation")),
        ("PM",_("Demand: Protection measures")),
        ("II",_("Demand: Independent investigation")),
        ("PI",_("Demand: Provide information")),
        ("RD",_("Demand: Release detainee")),
    )

    GOV_REPLY_CHOICES = (
        ("reject",_("Violation rejected")),
        ("incomp",_("Reponsive but incomplete")),
        ("immat",_("Immaterial response")),
        ("react",_("Steps taken to address")),
        ("transl",_("In translation")),
        ("na",_("File not available")),
    )

    GOV_ACTION_CHOICES = (
        ("protect",_("Protection measures granted")),
        ("release",_("Individual released early")),
        ("notrial",_("Individual released without trial")),
        ("improve",_("Improved prison conditions")),
        ("investigate",_("Investigation opened")),
        ("prosecuted",_("Perpetrator suspended/prosecuted")),
        ("issued",_("Travel documents issued")),
        ("other",_("Other")),
    )

    SOURCES_CHOICES = (
        ("NGO",_("INGO")),
        ("RNGO",_("RNGO")),
        ("LNGO",_("LNGO")),
        ("GOV",_("GOV")),
        ("IO",_("IO")),
        ("IND",_("Indiv.")),
    )
    
    # Data model implementation

    person_id = models.CharField(
        max_length=13,
        verbose_name=_("Person ID"),
        unique=True,
        validators=[int_list_validator(sep='-', message=None, code='invalid'),MinLengthValidator(13, message=None)],
        help_text=_("Form YYYY-CCCC-PPP, where YYYY is the year of publication, CCCC is the paragraph number given in the report, and PPP the person number within the communication")
    )
    ohchr_case = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("OHCHR case no.")
    )
    country = CountryField(
        blank_label=_('(select country)'),
        verbose_name=_("Country")
    )
    date_intervention = models.DateField(
        verbose_name=_("Date of the intervention"),
        help_text=_("Format YYYY-MM-DD"),
        blank=True,
        null=True
    )
    type_intervention = models.CharField(
        max_length=3,
        choices=INTERVENTION_CHOICES,
        verbose_name=_("Type of intervention")
    )
    joint_with = SelectMultipleField(
        max_length=200,
        choices=JOINT_CHOICES,
        blank = True,
        verbose_name=_("Joint with"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>")
    )
    name = models.CharField(
        max_length=500,
        verbose_name=_("Name of HRD")
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES,
        verbose_name=_("Gender")
    )
    follow_up_case = models.BooleanField(
        default = False,
        verbose_name=_("Follow-up on UN case")
    )
    follow_ups = models.ManyToManyField(
        'self',
        default = None,
        blank = True,
        verbose_name="Follow-up Person IDs"
    )
    earlier_coms = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_("Date(s) of earlier coms")
    )
    regional_case = models.BooleanField(
        default = False,
        verbose_name=_("Regional mechanism case")
    )
    issue_area = SelectMultipleField(
        max_length=20,
        choices=ISSUE_CHOICES,
        max_choices=3,
        default="?",
        verbose_name=_("Issue area"),
        help_text=_("Select maximum 3 items with <i>Ctrl+Click</i>")
    )
    relevant_activities = SelectMultipleField(
        max_length=15,
        choices=ACTIVITIES_CHOICES,
        max_choices=3,
        default="?",
        verbose_name=_("Relevant activities"),
        help_text=_("Select maximum 3 items with <i>Ctrl+Click</i>")
    )
    affiliation = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_("Affiliation")
    )
    further_info = models.TextField(
        blank=True,
        verbose_name=_("Further information"),
        help_text=_("Name of NGO or party, title of conference, object of investigation etc.")
    )
    foreign_national = models.BooleanField(
        default=False,
        verbose_name=_("Foreign national")
    )
    international_cooperation = models.IntegerField(
        choices=COOPERATION_CHOICES,
        default=0,
        verbose_name=_("International cooperation")
    )
    location = models.CharField(
        max_length=1,
        choices=LOCATION_CHOICES,
        default = "?",
        verbose_name=_("Location")
    )
    name_area = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Name of City / Area")
    )
    violation_family = models.IntegerField(
        choices=VIOLATION_FAMILY_CHOICES,
        default=0,
        verbose_name=_("Violation against HRD or family member?")
    )
    violation_family_who = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Concerned family member")
    )
    violations = SelectMultipleField(
        max_length=50,
        choices=VIOLATIONS_CHOICES,
        default="?",
        verbose_name=_("Violation(s)"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>")
    )
    perpetrator = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        default = "U",
        verbose_name=_("Alleged perpetrator"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>")
    )
    violations2 = SelectMultipleField(
        max_length=50,
        choices=VIOLATIONS_CHOICES,
        verbose_name=_("Violation(s) #2"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        blank=True
    )
    perpetrator2 = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        verbose_name=_("Alleged perpetrator #2"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        blank=True
    )
    violations3 = SelectMultipleField(
        max_length=50,
        choices=VIOLATIONS_CHOICES,
        verbose_name=_("Violation(s) #3"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        blank=True
    )
    perpetrator3 = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        verbose_name=_("Alleged perpetrator #3"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        blank=True
    )
    violations4 = SelectMultipleField(
        max_length=50,
        choices=VIOLATIONS_CHOICES,
        verbose_name=_("Violation(s) #4"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        blank=True
    )
    perpetrator4 = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        verbose_name=_("Alleged perpetrator #4"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        blank=True
    )
    date_incident = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of the latest incident"),
        help_text=_("Format YYYY-MM-DD")
    )
    date_incident_unspecific = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("If unspecific")
    )
    concern_expressed = models.CharField(
        max_length=2,
        choices=CONCERN_CHOICES,
        verbose_name=_("Concern/demand expressed in intervention"),
        blank=True
    )
    is_released = models.BooleanField(
        default = False,
        verbose_name=_("If arrested: released?")
    )
    
    ##########################

    date_govreply = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of government reply"),
        help_text=_('Format YYYY-MM-DD, leave empty for "No response"')
    )
    date_govreply_further = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Date(s) of further replies")
    )
    govreply_content = models.CharField(
        max_length=6,
        choices=GOV_REPLY_CHOICES,
        verbose_name=_("Content of government reply"),
        help_text=_("According to rating criteria by Piccone (2012)"),
        blank=True
    )
    date_govaction = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date of action according to reply"),
        help_text=_("Format YYYY-MM-DD")
    )
    govreply_action = models.CharField(
        max_length=11,
        choices=GOV_ACTION_CHOICES,
        verbose_name=_("Action taken according to reply"),
        blank=True
    )
    
    ##########################
    
    further_comments = models.TextField(
        blank=True,
        verbose_name=_("Further comments"),
        help_text=_("Observations that might be relevant but don't fit elsewhere")
    )

    feedback = models.TextField(
        blank=True,
        verbose_name=_("Feedback"),
        help_text=_("Direct feedback on the coding of this particular case")
    )

    upload = models.FileField(
        upload_to=update_filename,
        null=True,
        blank=True,
        verbose_name=_("Uploads")
    )

    analyst = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name=_("Analyst"),
        help_text=_("User responsible for this record")
    )

    is_final = models.BooleanField(
        default = False,
        verbose_name=_("Final")
    )
    
    business_case = models.BooleanField(
        default = False,
        verbose_name=_("Business-related case")
    )

    business_company = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_("Name of company")
    )

    sources_number = models.CharField(
        blank=True,
        max_length=50,
        verbose_name=_("Number of sources")
    )

    sources_type = SelectMultipleField(
        max_length=50,
        choices=SOURCES_CHOICES,
        verbose_name=_("Type of sources"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        blank=True
    )

    complaint_sent = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Complaint sent on"),
        help_text=_("Format YYYY-MM-DD")
    )

    complaint_received = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Complaint received on"),
        help_text=_("Format YYYY-MM-DD")
    )

    coords = PointField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("Coordinates")
    )

    def has_related_object(self):
        return hasattr(self, 'followup')

    def get_geoname(self):
        return "%s"%(self.country.name) if not self.name_area or self.location == 'A' else "%s, %s"%(self.name_area,self.country.name)
    
    def get_coordinates(self):
        geolocator = Nominatim()
        try:
            loc = geolocator.geocode(self.get_geoname())
            tmp = PointField()
            tmp = {
                "type": "Point",
                "coordinates": [
                    float(loc.longitude),
                    float(loc.latitude)
                ]
            }

            #if tmp != self.coords:
                #print "Updated record %s: %s -> %s" % (self.person_id, "none" if not self.coords else self.coords['coordinates'], tmp['coordinates'])

            self.coords = tmp
            #print "Located record %s (%s)" % (self.person_id, unicode(self.name)) + " with: " + unicode(self.get_geoname()) + " " + str(loc.longitude) + " " + str(loc.latitude)
        except AttributeError:
            #print "Could not locate record %s (%s)" % (self.person_id, unicode(self.name)) + " with: " + unicode(self.get_geoname())
            pass
        except GeocoderServiceError:
            #print "Geocoder service error on record %s (%s)" % (self.person_id, unicode(self.name))
            pass
        
    def as_geojson_dict(self):
        """
        Method to return each feature in the DB as a geojson object.
        """
        if self.coords is not None:
            place = self.get_geoname()
            as_dict = {
                "type": "Feature",
                "geometry": self.coords,
                "properties": {
                    "date": dateformat.format(self.date_intervention, 'F j, Y') if self.date_intervention else "unknown",
                    "type": self.type_intervention,
                    "location": place,
                    "id": self.id
                }
            }
        else:
            as_dict = {}
        return as_dict

    
class OtherRecord(models.Model):

    CASE_CHOICES = (
        (0, _("NGO/Trade union/...")),
        (1, _("NHRI")),
        (2, _("Statement by official")),
        (3, _("Law/bill")),
        (4, _("Mass violation/pattern")),
        (5, _("Anonymous cases")),
        (6, _("PR on individual")),
        (7, _("Country visit by SR")),
        (8, _("Event/Commemoration"))
    )

    class Meta: 
        verbose_name = _("NGO Record")

    def __unicode__(self):
        return "%s (%s)" % (self.case_id, self.name)
    
    # Additional model valiation

    def clean(self):
        super(OtherRecord, self).clean()

        if self.type_intervention == 'JUA' or self.type_intervention == 'JAL':
            if not self.joint_with or (len(self.joint_with) == 1 and not self.joint_with[0]):
                raise ValidationError('Select joint intervention type, required for JUA and JAL.')

    case_id = models.CharField(
        max_length=9,
        verbose_name=_("Case ID"),
        unique=True,
        validators=[int_list_validator(sep='-', message=None, code='invalid'),MinLengthValidator(9, message=None)],
        help_text=_("Form YYYY-CCCC, where YYYY is the year of publication and CCCC the paragraph number given in the report")
    )
    ohchr_case = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("OHCHR case no.")
    )
    country = CountryField(
        blank_label=_('(select country)'),
        verbose_name=_("Country")
    )
    date_intervention = models.DateField(
        verbose_name=_("Date of the intervention"),
        help_text=_("Format YYYY-MM-DD")
    )
    type_intervention = models.CharField(
        max_length=3,
        choices=Record.INTERVENTION_CHOICES,
        verbose_name=_("Type of intervention")
    )
    joint_with = SelectMultipleField(
        max_length=200,
        choices=Record.JOINT_CHOICES,
        blank = True,
        verbose_name=_("Joint with"),
        help_text=_("Select multiple items with <i>Ctrl+Click</i>")
    )
    name = models.CharField(
        max_length=500,
        verbose_name=_("Subject of communication")
    )
    case_type = models.IntegerField(
        choices=CASE_CHOICES,
        verbose_name=_("Type of case"),
        default=0
    )
    follow_up_case = models.BooleanField(
        default = False,
        verbose_name=_("Follow-up on UN case")
    )
    regional_case = models.BooleanField(
        default = False,
        verbose_name=_("Regional mechanism case")
    )
    
    ##########################
    
    further_comments = models.TextField(
        blank=True,
        verbose_name=_("Further comments"),
        help_text=_("Observations that might be relevant but don't fit elsewhere")
    )

    upload = models.FileField(
        upload_to=update_filename,
        null=True,
        blank=True,
        verbose_name=_("Uploads")
    )

    analyst = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name=_("Analyst"),
        help_text=_("User responsible for this record")
    )

    business_case = models.BooleanField(
        default = False,
        verbose_name=_("Business-related case")
    )

    business_company = models.CharField(
        blank=True,
        max_length=500,
        verbose_name=_("Name of company")
    )




class AIRecord(models.Model):

    class Meta: 
        verbose_name = _("AI Record")

    def __unicode__(self):
        return "%s (%s)" % (self.person_id, self.name)
    
    # Additional model valiation

    def clean(self):
        super(AIRecord, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        super(AIRecord, self).save(*args, **kwargs) # Call the "real" save() method.
    
    # Data model implementation

    person_id = models.CharField(
        max_length=16,
        verbose_name=_("Person ID"),
        unique=True,
        validators=[MinLengthValidator(16, message=None)],
        default = "AI-",
        help_text=_("Form AI-YYYY-RRRR-PPP, where YYYY is the year of publication, RRRR is the reference, and PPP the person number within the communication")
    )
    ai_reference = models.CharField(
        max_length=25,
        verbose_name=_("AI Internal Reference")
    )
    pub_reference = models.CharField(
        max_length=25,
        blank=True,
        verbose_name=_("Public ID")
    )
    country = CountryField(blank_label='(select country)')
    date_submission = models.DateField(
        verbose_name=_("Date of the submission"),
        help_text=_("Format YYYY-MM-DD")
    )
    joint_with = SelectMultipleField(
        max_length=200,
        choices=Record.JOINT_CHOICES,
        blank = True,
        help_text=_("Select multiple items with <i>Ctrl+Click</i>"),
        verbose_name=_("Additional mandates")
    )
    name = models.CharField(
        max_length=500,
        verbose_name=_("Name of HRD")
    )   
    case_summary = models.TextField(
        blank=True,
        verbose_name=_("Case Summary"),
        help_text=""
    )

    fa_title = models.TextField(
        blank=True,
        verbose_name=_("FA Title"),
        help_text=""
    )

    fa_date = models.DateField(
        verbose_name=_("Date of FA"),
        help_text=_("Format YYYY-MM-DD"),
        blank=True,
        null=True
    )

    fa_summary = models.TextField(
        blank=True,
        verbose_name=_("Summary of FA"),
        help_text=""
    )

    fa_title2 = models.TextField(
        blank=True,
        verbose_name=_("FA Title (2)"),
        help_text=""
    )

    fa_date2 = models.DateField(
        verbose_name=_("Date of FA (2)"),
        help_text=_("Format YYYY-MM-DD"),
        blank=True,
        null=True
    )

    fa_summary2 = models.TextField(
        blank=True,
        verbose_name=_("Summary of FA (2)"),
        help_text=""
    )

    fa_title3 = models.TextField(
        blank=True,
        verbose_name=_("FA Title (3)"),
        help_text=""
    )

    fa_date3 = models.DateField(
        verbose_name=_("Date of FA (3)"),
        help_text=_("Format YYYY-MM-DD"),
        blank=True,
        null=True
    )

    fa_summary3 = models.TextField(
        blank=True,
        verbose_name=_("Summary of FA (3)"),
        help_text=""
    )

    fa_title4 = models.TextField(
        blank=True,
        verbose_name=_("FA Title (4)"),
        help_text=""
    )

    fa_date4 = models.DateField(
        verbose_name=_("Date of FA (4)"),
        help_text=_("Format YYYY-MM-DD"),
        blank=True,
        null=True
    )

    fa_summary4 = models.TextField(
        blank=True,
        verbose_name=_("Summary of FA (4)"),
        help_text=""
    )
    
    further_comments = models.TextField(
        blank=True,
        verbose_name=_("Further comments"),
        help_text=_("Observations that might be relevant but don't fit elsewhere")
    )

    analyst = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name=_("Analyst"),
        help_text=_("User responsible for this record")
    )

    is_final = models.BooleanField(
        default = False,
        verbose_name=_("Final")
    )
    
