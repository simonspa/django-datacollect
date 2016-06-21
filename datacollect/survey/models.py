from __future__ import unicode_literals

from django.db import models
from djgeojson.fields import PointField
from django_countries.fields import CountryField
from select_multiple_field.models import SelectMultipleField
from django.core.exceptions import ValidationError
from django.core.validators import int_list_validator, MinLengthValidator
from django.contrib.auth.models import User

import json
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

        # Fill geolocation:
        self.get_coordinates()
        

    def save(self, *args, **kwargs):
        self.clean()
        super(Record, self).save(*args, **kwargs) # Call the "real" save() method.


    # Choices for select boxes

    GENDER_CHOICES = (
        (0, "Male"),
        (1, "Female"),
        (2, "Trans/inter*")
    )

    ISSUE_CHOICES = (
        ("?","N/A"),
        ("WR","Women's rights"),
        ("CRS","Children's rights"),
        ("IPR","Indigenous peoples' rights"),
        ("LGBTI","LGBTI issues"),
        ("MRR","Migrants'/refugees' rights"),
        ("LR","Labour rights"),
        ("POV","Poverty"),
        ("RTF","Right to food"),
        ("HI","Health issues"),
        ("HRFE","Housing rights/forced evictions"),
        ("LNR","Land rights/environment"),
        ("CR","Cultural rights"),
        ("RF","Religious freedom"),
        ("PR","Prisoner's rights"),
        ("AT","Torture"),
        ("ED","Enforced disappearance"),
        ("H","Homocide"),
        ("PV","Police violence"),
        ("AC","Corruption"),
        ("DV","Democratic/voting rights"),
        ("IF","Internet freedom"),
        ("HRE","Human rights education"),
        ("TJ","Transitional justice")
    )
    
    ACTIVITIES_CHOICES = (
        ("?","N/A"),
        ("CSA","Civil society activist"),
        ("TUA","Trade union activist"),
        ("RA","Religious association"),
        ("PM","Politician/Party member"),
        ("CL","Community leader"),
        ("L","Lawyer/Judge/Attorney"),
        ("J","Journalist/Editor"),
        ("A","Artist/Writer"),
        ("S","Student"),
        ("T","Teacher/Professor"),
        ("MP","Medical professional"),
        ("HW","Humanitarian worker"),
        ("V","Victim/witness of HR violations"),
        ("OP","Ombudsperson"),
        ("I","Investigation against officials"),
        ("PC","Participation in conference/meeting"),
        ("PP","Participation in public protest/rally"),
    )

    COOPERATION_CHOICES = (
        (0, "Not mentioned"),
        (1, "UN"),
        (2, "INGO")
    )

    LOCATION_CHOICES = (
        ("C","Capital"),
        ("T","City/Town"),
        ("R","Rural area"),
        ("?","Unknown")
    )

    VIOLATION_FAMILY_CHOICES = (
        (0,"Only HRD"),
        (1,"against relative"),
        (2,"against both")
    )

    VIOLATIONS_CHOICES = (
        ("?","N/A"),
        ("AD","Arrest/Detention"),
        ("IC"," + Incommunicado"),
        ("PC"," + Held in poor conditions"),
        ("RT"," + Risk of torture"),
        ("TI","Torture/Ill-treatment"),
        ("ED","Enforced disappearance"),
        ("KA","Physical attack"),
        ("KK"," + Killing attempt"),
        ("K","  + Killing"),
        ("DI","Kidnapping"),
        ("P","Prosecution"),
        ("UT"," + Unfair trial"),
        ("C"," + Conviction"),
        ("T","Threats"),
        ("S","Surveillance"),
        ("R","Office/home raided"),
        ("DC","Defamation campaign"),
        ("DP","Disciplinary proceedings"),
        ("B","Travel restrictions"),
        ("AH","Administrative harassment"),
        ("FI","Failure to intervene/protect")
    )

    PERPETRATOR_CHOICES = (
        ("U","Unknown"),
        ("P","Police/security forces"),
        ("CS","Public official/administration/judiciary"),
        ("A","Army"),
        ("AO","Armed opposition"),
        ("B","Business/landholder"),
        ("M","Mob")
    )

    INTERVENTION_CHOICES = (
        ("?","N/A"),
        ("UA","UA"),
        ("JUA","JUA"),
        ("AL","AL"),
        ("JAL","JAL"),
        ("PR","PR")
    )

    JOINT_CHOICES = (
        ("FrASSEM","FrASSEM"),
        ("FrEXPRESS","FrEXPRESS"),
        ("TORTURE","TORTURE"),
        ("WGAD","WGAD"),
        ("WGED","WGED"),
        ("SumEXECU","SumEXECU"),
        ("WOMEN","WOMEN"),
        ("FrRELIGION","FrRELIGION"),
        ("JUDGES","JUDGES"),
        ("INDIGENOUS","INDIGENOUS"),
        ("TERRORISM","TERRORISM"),
        ("BUSINESS","BUSINESS"),
        ("HEALTH","HEALTH"),
        ("ENVIR","ENVIR"),
        ("FOOD","FOOD")
    )

    CONCERN_CHOICES = (
        ("CV","Concern over violation"),
        ("PV","Concern: Pattern of violation"),
        ("PM","Demand: Protection measures"),
        ("II","Demand: Independent investigation"),
        ("PI","Demand: Provide information"),
        ("RD","Demand: Release detainee")
    )

    GOV_REPLY_CHOICES = (
        ("reject","Violation rejected"),
        ("incomp","Reponsive but incomplete"),
        ("immat","Immaterial response"),
        ("react","Steps taken to address"),
        ("transl","In translation")
    )

    GOV_ACTION_CHOICES = (
        ("protect","Protection measures granted"),
        ("release","Individual released early"),
        ("improve","Improved prison conditions"),
        ("investigate","Investigation opened"),
        ("prosecuted","Perpetrator suspended/prosecuted"),
        ("issued","Travel documents issued")
    )

    
    # Data model implementation

    person_id = models.CharField(
        max_length=12,
        verbose_name="Person ID",
        unique=True,
        validators=[int_list_validator(sep='-', message=None, code='invalid'),MinLengthValidator(12, message=None)],
        help_text="Form YYYY-CCCC-PP, where YYYY is the year of publication, CCCC is the paragraph number given in the report, and PP the person number within the communication"
    )
    ohchr_case = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="OHCHR case no."
    )
    country = CountryField(blank_label='(select country)')
    date_intervention = models.DateField(
        verbose_name="Date of the intervention",
        help_text="Format YYY-MM-DD"
    )
    type_intervention = models.CharField(
        max_length=3,
        choices=INTERVENTION_CHOICES,
        verbose_name="Type of intervention"
    )
    joint_with = SelectMultipleField(
        max_length=200,
        choices=JOINT_CHOICES,
        blank = True,
        help_text="Select multiple items with <i>Ctrl+Click</i>"
    )
    name = models.CharField(
        max_length=500,
        verbose_name="Name of HRD"
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES
    )
    follow_up_case = models.BooleanField(
        default = False,
        verbose_name="Follow-up on UN case"
    )
    regional_case = models.BooleanField(
        default = False,
        verbose_name="Regional mechanism case"
    )
    issue_area = SelectMultipleField(
        max_length=10,
        choices=ISSUE_CHOICES,
        max_choices=3,
        default="?",
        help_text="Select maximum 3 items with <i>Ctrl+Click</i>"
    )
    relevant_activities = SelectMultipleField(
        max_length=15,
        choices=ACTIVITIES_CHOICES,
        max_choices=3,
        default="?",
        help_text="Select maximum 3 items with <i>Ctrl+Click</i>"
    )
    further_info = models.TextField(
        blank=True,
        verbose_name="Further information",
        help_text="Name of NGO or party, title of conference, object of investigation etc."
    )
    international_cooperation = models.IntegerField(
        choices=COOPERATION_CHOICES,
        default=0
    )
    location = models.CharField(
        max_length=1,
        choices=LOCATION_CHOICES,
        default = "?"
    )
    name_area = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Name of City / Area"
    )
    violation_family = models.IntegerField(
        choices=VIOLATION_FAMILY_CHOICES,
        default=0,
        verbose_name="Violation against HRD or family member?"
    )
    violations = SelectMultipleField(
        max_length=50,
        choices=VIOLATIONS_CHOICES,
        default="?",
        verbose_name="Violation(s)",
        help_text="Select multiple items with <i>Ctrl+Click</i>"
    )
    perpetrator = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        default = "U",
        verbose_name="Alleged perpetrator",
        help_text="Select multiple items with <i>Ctrl+Click</i>"
    )
    violations2 = SelectMultipleField(
        max_length=50,
        choices=VIOLATIONS_CHOICES,
        verbose_name="Violation(s) #2",
        help_text="Select multiple items with <i>Ctrl+Click</i>",
        blank=True
    )
    perpetrator2 = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        verbose_name="Alleged perpetrator #2",
        help_text="Select multiple items with <i>Ctrl+Click</i>",
        blank=True
    )
    violations3 = SelectMultipleField(
        max_length=50,
        choices=VIOLATIONS_CHOICES,
        verbose_name="Violation(s) #3",
        help_text="Select multiple items with <i>Ctrl+Click</i>",
        blank=True
    )
    perpetrator3 = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        verbose_name="Alleged perpetrator #3",
        help_text="Select multiple items with <i>Ctrl+Click</i>",
        blank=True
    )
    date_incident = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of the latest incident",
        help_text="Format YYY-MM-DD"
    )
    concern_expressed = models.CharField(
        max_length=2,
        choices=CONCERN_CHOICES,
        verbose_name="Concern/demand expressed in intervention",
        blank=True
    )

    ##########################

    date_govreply = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of government reply",
        help_text='Format YYY-MM-DD, leave empty for "No response"'
    )
    govreply_content = models.CharField(
        max_length=6,
        choices=GOV_REPLY_CHOICES,
        verbose_name="Content of government reply",
        help_text="According to rating criteria by Piccone (2012)",
        blank=True
    )
    date_govaction = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of action according to reply",
        help_text="Format YYY-MM-DD"
    )
    govreply_action = models.CharField(
        max_length=11,
        choices=GOV_ACTION_CHOICES,
        verbose_name="Action taken according to reply",
        blank=True
    )
    
    ##########################
    
    further_comments = models.TextField(
        blank=True,
        verbose_name="Further comments",
        help_text="Observations that might be relevant but don't fit elsewhere"
    )

    feedback = models.TextField(
        blank=True,
        verbose_name="Feedback",
        help_text="Direct feedback on the coding of this particular case"
    )

    upload = models.FileField(
        upload_to=update_filename,
        null=True,
        blank=True
    )

    analyst = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name="Analyst",
        help_text="User responsible for this record"
    )
    
    coords = PointField(
        blank=True,
        null=True,
        editable=False
    )

    
    def get_coordinates(self):
        geolocator = Nominatim()
        geoname = "%s %s"%(self.country.name,self.name_area)
        loc = geolocator.geocode(geoname)
        try:
            self.coords = {
                "type": "Point",
                "coordinates": [
                    float(loc.longitude),
                    float(loc.latitude)
                ]
            }
            print "Located record %s (%s)" % (self.person_id, self.name) + " in: " + loc.address
        except AttributeError:
            print "Could locate record %s (%s)" % (self.person_id, self.name) + " with: " + geoname
        
    def as_geojson_dict(self):
        """
        Method to return each feature in the DB as a geojson object.
        """
        if self.coords is not None:
            as_dict = {
                "type": "Feature",
                "geometry": self.coords,
                "properties": {
                    "date": dateformat.format(self.date_intervention, 'F j, Y'),
                    "type": self.type_intervention
                }
            }
        else:
            as_dict = {}
        return as_dict

    
class OtherRecord(models.Model):

    class Meta: 
        verbose_name = "NGO Record"

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
        verbose_name="Case ID",
        unique=True,
        validators=[int_list_validator(sep='-', message=None, code='invalid'),MinLengthValidator(9, message=None)],
        help_text="Form YYYY-CCCC, where YYYY is the year of publication and CCCC the paragraph number given in the report"
    )
    ohchr_case = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="OHCHR case no."
    )
    country = CountryField(blank_label='(select country)')
    date_intervention = models.DateField(
        verbose_name="Date of the intervention",
        help_text="Format YYY-MM-DD"
    )
    type_intervention = models.CharField(
        max_length=3,
        choices=Record.INTERVENTION_CHOICES,
        verbose_name="Type of intervention"
    )
    joint_with = SelectMultipleField(
        max_length=200,
        choices=Record.JOINT_CHOICES,
        blank = True,
        help_text="Select multiple items with <i>Ctrl+Click</i>"
    )
    name = models.CharField(
        max_length=500,
        verbose_name="Name of NGO"
    )
    follow_up_case = models.BooleanField(
        default = False,
        verbose_name="Follow-up on UN case"
    )
    regional_case = models.BooleanField(
        default = False,
        verbose_name="Regional mechanism case"
    )
    
    ##########################
    
    further_comments = models.TextField(
        blank=True,
        verbose_name="Further comments",
        help_text="Observations that might be relevant but don't fit elsewhere"
    )

    upload = models.FileField(
        upload_to=update_filename,
        null=True,
        blank=True
    )

    analyst = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name="Analyst",
        help_text="User responsible for this record"
    )
