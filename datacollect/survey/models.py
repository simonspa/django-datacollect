from __future__ import unicode_literals

from django.db import models
from django_countries.fields import CountryField
from select_multiple_field.models import SelectMultipleField

# Choices for select boxes

GENDER_CHOICES = (
    (0, "Male"),
    (1, "Not Male")
)

ISSUE_CHOICES = (
    ("WR","Women's rights"),
    ("LGBTI","LGBTI issues"),
    ("IPR","Indigenous peoples' rights"),
    ("HRFE","Housing rights/Forced evictions"),
    ("LNR","Land rights/nat' res'/environment"),
    ("LR","Labour rights"),
    ("IF","Internet freedom"),
    ("CRS","Children's rights"),
    ("HI","Health issues"),
    ("CR","Cultural rights"),
    ("RF","Religious freedom"),
    ("HRE","Human rights education"),
    ("MRR","Migrants'/Refugees' rights"),
    ("MR","Minority rights (if not specified)"),
    ("AT","Anti-Torture"),
    ("PR","Prisoner's rights"),
    ("ED","Enforced disappearance"),
    ("H","Homocide"),
    ("AC","Anti-Corruption"),
    ("?","N/A")
)

ACTIVITIES_CHOICES = (
    ("L","Lawyer"),
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
    ("?","N/A")
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

VIOLATIONS_CHOICES = (
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
    ("AH","Administrative harassment"),
    ("?","N/A")
)

VIOLATION_FAMILY_CHOICES = (
    (0,"Only HDR"),
    (1,"against relative"),
    (2,"against both")
)

PERPETRATOR_CHOICES = (
    ("P","Police/Security forces"),
    ("A","Army"),
    ("AO","Armed opposition"),
    ("B","Business/landholder"),
    ("M","Mob"),
    ("U","Unknown"),
    ("?","N/A")
)

INTERVENTION_CHOICES = (
    ("UA","UA"),
    ("JUA","JUA"),
    ("AL","AL"),
    ("JAL","JAL"),
    ("PR","PR")
)

JOINT_CHOICES = (
    ("FREX","FREX"),
    ("TOR","TOR")
)

CONCERN_CHOICES = (
    ("PM","Protection measures"),
    ("II","Independent investigation"),
    ("PI","Provide information"),
    ("PV","Concern: Pattern of violation"),
    ("CV","Concern over violation")
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

class Record(models.Model):

    person_id = models.CharField(max_length=10)
    name = models.CharField(max_length=500)
    gender = models.IntegerField(
        choices=GENDER_CHOICES
    )
    issue_area = SelectMultipleField(
        max_length=10,
        choices=ISSUE_CHOICES,
        max_choices=2,
        default="?"
    )
    relevant_activities = SelectMultipleField(
        max_length=15,
        choices=ACTIVITIES_CHOICES,
        max_choices=3,
        default="?"
    )
    international_cooperation = models.IntegerField(
        choices=COOPERATION_CHOICES,
        default=0
    )
    follow_up_case = models.BooleanField(
        default = False
    )

    ##########################
    
    country = CountryField(blank_label='(select country)')
    location = models.CharField(
        max_length=1,
        choices=LOCATION_CHOICES,
        default = "?"
    )
    name_of_city_or_area = models.CharField(max_length=500,blank=True)
    violations = SelectMultipleField(
        max_length=15,
        choices=VIOLATIONS_CHOICES,
        max_choices=3,
        default="?"
    )
    violation_against_family_member = models.IntegerField(
        choices=VIOLATION_FAMILY_CHOICES,
        default=0
    )
    alleged_perpetrator = models.CharField(
        max_length=2,
        choices=PERPETRATOR_CHOICES,
        default = "?"
    )
    date_latest_incident = models.DateField(null=True, blank=True)

    ##########################
    
    date_intervention = models.DateField(null=True, blank=True)
    type_intervention = models.CharField(
        max_length=3,
        choices=INTERVENTION_CHOICES
    )
    joint_with = models.CharField(
        max_length=4,
        choices=JOINT_CHOICES,
        null = True,
        blank = True
    )
    concern_expressed = models.CharField(
        max_length=2,
        choices=CONCERN_CHOICES
    )

    ##########################

    date_government_reply = models.DateField(null=True, blank=True)
    government_reply_content = models.CharField(
        max_length=6,
        choices=GOV_REPLY_CHOICES
    )
    date_government_action = models.DateField(null=True, blank=True)
    government_reply_action = models.CharField(
        max_length=11,
        choices=GOV_ACTION_CHOICES
    )
    
    ##########################
    
    further_comments = models.TextField(blank=True)
