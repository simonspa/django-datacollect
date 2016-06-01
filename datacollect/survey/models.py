from __future__ import unicode_literals

from django.db import models
from django_countries.fields import CountryField
from select_multiple_field.models import SelectMultipleField
from django.core.exceptions import ValidationError
from django.core.validators import int_list_validator, MinLengthValidator

def update_filename(instance, filename):
    return '{0}/{1}'.format(instance.person_id, filename)

class Record(models.Model):

    # Additional model valiation

    def clean(self):
        super(Record, self).clean()

        if self.date_govreply and not self.govreply_content:
            raise ValidationError('With a government reply date set, a reply content is required')
        if self.date_govaction and not self.govreply_action:
            raise ValidationError('With a government reply date set, a reply content is required')

    # Choices for select boxes

    GENDER_CHOICES = (
        (0, "Male"),
        (1, "Female"),
        (2, "Trans/inter*")
    )

    ISSUE_CHOICES = (
        ("?","N/A"),
        ("WR","Women's rights"),
        ("LGBTI","LGBTI issues"),
        ("IPR","Indigenous peoples' rights"),
        ("HRFE","Housing rights/forced evictions"),
        ("LNR","Land rights/nat' res'/environment"),
        ("LR","Labour rights"),
        ("IF","Internet freedom"),
        ("CRS","Children's rights"),
        ("HI","Health issues"),
        ("CR","Cultural rights"),
        ("RF","Religious freedom"),
        ("HRE","Human rights education"),
        ("MRR","Migrants'/refugees' rights"),
        ("MR","Minority rights (if not specified)"),
        ("AT","Anti-Torture"),
        ("PR","Prisoner's rights"),
        ("ED","Enforced disappearance"),
        ("H","Homocide"),
        ("AC","Anti-corruption"),
        ("PV","Police violence"),
        ("DV","Democratic/voting rights"),
    )
    
    ACTIVITIES_CHOICES = (
        ("?","N/A"),
        ("L","Lawyer/Judge"),
        ("CSA","Civil society activist"),
        ("TUA","Trade union activist"),
        ("S","Student"),
        ("J","Journalist/Editor/Writer"),
        ("MP","Medical professional"),
        ("T","Teacher/Professor"),
        ("CL","Community leader"),
        ("RA","Religious association"),
        ("PM","Politician/Party member"),
        ("HW","Humanitarian worker"),
        ("V","Victim/witness of HR violations"),
        ("I","Investigation against officials"),
        ("PC","Participation in conference"),
        ("PP","Participation in protest/rally"),
        ("OP","Ombudsperson")
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
        ("P","Prosecution"),
        ("UT","Unfair trial"),
        ("C","Conviction"),
        ("K","Killing"),
        ("KA","Killing attempt/Assault"),
        ("DI","Diappearance/Incommunicado"),
        ("PC","Held in poor conditions"),
        ("RT","Risk of torture"),
        ("TI","Torture/Ill-treatment"),
        ("T","Threats"),
        ("DC","Defamation campaign"),
        ("DP","Disciplinary proceedings"),
        ("S","Surveillance"),
        ("R","Office/home raided"),
        ("B","Barred from travelling"),
        ("AH","Administrative harassment")
    )

    PERPETRATOR_CHOICES = (
        ("?","N/A"),
        ("P","Police/security forces"),
        ("CS","Civil servant/administration/judiciary"),
        ("A","Army"),
        ("AO","Armed opposition"),
        ("B","Business/landholder"),
        ("M","Mob"),
        ("U","Unknown")
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
        ("ENVIR","ENVIR")
    )

    CONCERN_CHOICES = (
        ("CV","Concern over violation"),
        ("PM","Protection measures"),
        ("II","Independent investigation"),
        ("PI","Provide information"),
        ("PV","Concern: Pattern of violation")
    )

    GOV_REPLY_CHOICES = (
        ("reject","Violation rejected"),
        ("incomp","Reponsive but incomplete"),
        ("immat","Immaterial response"),
        ("react","Steps taken to address")
    )

    GOV_ACTION_CHOICES = (
        ("protect","Protection measures granted"),
        ("release","Individual released"),
        ("improve","Improved prison conditions"),
        ("investigate","Investigation opened"),
        ("prosecuted","Perpetrator suspended/prosecuted"),
        ("issued","Travel documents issued")
    )

    
    # Data model implementation

    person_id = models.CharField(
        max_length=10,
        verbose_name="Person ID",
        unique=True,
        validators=[int_list_validator(sep='-', message=None, code='invalid'),MinLengthValidator(10, message=None)],
        help_text="Form YYYY-CCC-P, where YYYY is the year of publication, CCC is the paragraph number given in the report, and P the person number within the communication"
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
        help_text="Select any number items with <i>Ctrl+Click</i>"
    )
    name = models.CharField(
        max_length=500,
        verbose_name="Name of HRD"
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES
    )
    follow_up_case = models.BooleanField(
        default = False
    )
    issue_area = SelectMultipleField(
        max_length=10,
        choices=ISSUE_CHOICES,
        max_choices=2,
        default="?",
        help_text="Select maximum 2 items with <i>Ctrl+Click</i>"
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
        max_length=15,
        choices=VIOLATIONS_CHOICES,
        max_choices=3,
        default="?",
        verbose_name="Violation(s)",
        help_text="Select maximum 3 items with <i>Ctrl+Click</i>"
    )
    perpetrator = SelectMultipleField(
        max_length=10,
        choices=PERPETRATOR_CHOICES,
        max_choices=2,
        default = "?",
        verbose_name="Alleged perpetrator",
        help_text="Select maximum 2 items with <i>Ctrl+Click</i>"
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
        verbose_name="Date of government action according to reply",
        help_text="Format YYY-MM-DD"
    )
    govreply_action = models.CharField(
        max_length=11,
        choices=GOV_ACTION_CHOICES,
        verbose_name="Government action taken according to reply",
        blank=True
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


    
