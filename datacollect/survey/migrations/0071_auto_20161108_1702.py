# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-08 16:02
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0070_auto_20161107_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherrecord',
            name='joint_with',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('FrASSEM', 'FrASSEM'), ('FrEXPRESS', 'FrEXPRESS'), ('TORTURE', 'TORTURE'), ('WGAD', 'WGAD'), ('WGED', 'WGED'), ('SumEXECU', 'SumEXECU'), ('WOMEN', 'WOMEN'), ('FrRELIGION', 'FrRELIGION'), ('JUDGES', 'JUDGES'), ('INDIGENOUS', 'INDIGENOUS'), ('TERRORISM', 'TERRORISM'), ('BUSINESS', 'BUSINESS'), ('HEALTH', 'HEALTH'), ('ENVIR', 'ENVIR'), ('FOOD', 'FOOD'), ('CHILD', 'CHILD'), ('RACISM', 'RACISM'), ('HOUSING', 'HOUSING'), ('MINORITY', 'MINORITY'), ('EDUCATION', 'EDUCATION'), ('MIGRANTS', 'MIGRANTS'), ('WASTE', 'WASTE'), ('IDPs', 'IDPs'), ('WG_WOMEN', 'WG_WOMEN'), ('MERCENARIES', 'MERCENARIES'), ('TRUTH', 'TRUTH'), ('POVERTY', 'POVERTY'), ('CULTURE', 'CULTURE'), ('ELDERLY', 'ELDERLY'), ('SLAVERY', 'SLAVERY'), ('WATER', 'WATER'), ('AFRICAN', 'AFRICAN'), ('DISCAPA', 'DISCAPA'), ('SOLIDAR', 'SOLIDAR'), ('INTORDER', "INT'ORDER"), ('TRAFFIC', 'TRAFFIC'), ('specific', 'Country-specific')], help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=200),
        ),
        migrations.AlterField(
            model_name='record',
            name='joint_with',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('FrASSEM', 'FrASSEM'), ('FrEXPRESS', 'FrEXPRESS'), ('TORTURE', 'TORTURE'), ('WGAD', 'WGAD'), ('WGED', 'WGED'), ('SumEXECU', 'SumEXECU'), ('WOMEN', 'WOMEN'), ('FrRELIGION', 'FrRELIGION'), ('JUDGES', 'JUDGES'), ('INDIGENOUS', 'INDIGENOUS'), ('TERRORISM', 'TERRORISM'), ('BUSINESS', 'BUSINESS'), ('HEALTH', 'HEALTH'), ('ENVIR', 'ENVIR'), ('FOOD', 'FOOD'), ('CHILD', 'CHILD'), ('RACISM', 'RACISM'), ('HOUSING', 'HOUSING'), ('MINORITY', 'MINORITY'), ('EDUCATION', 'EDUCATION'), ('MIGRANTS', 'MIGRANTS'), ('WASTE', 'WASTE'), ('IDPs', 'IDPs'), ('WG_WOMEN', 'WG_WOMEN'), ('MERCENARIES', 'MERCENARIES'), ('TRUTH', 'TRUTH'), ('POVERTY', 'POVERTY'), ('CULTURE', 'CULTURE'), ('ELDERLY', 'ELDERLY'), ('SLAVERY', 'SLAVERY'), ('WATER', 'WATER'), ('AFRICAN', 'AFRICAN'), ('DISCAPA', 'DISCAPA'), ('SOLIDAR', 'SOLIDAR'), ('INTORDER', "INT'ORDER"), ('TRAFFIC', 'TRAFFIC'), ('specific', 'Country-specific')], help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=200),
        ),
        migrations.AlterField(
            model_name='record',
            name='relevant_activities',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('CSA', 'Civil society activist'), ('TUA', 'Trade union activist'), ('RA', 'Religious association'), ('PM', 'Politician/Party member'), ('CL', 'Community leader'), ('L', 'Lawyer/Judge/Attorney'), ('J', 'Journalist/Editor'), ('CA', 'Cyberactivist'), ('A', 'Artist/Writer'), ('S', 'Student'), ('T', 'Teacher/Professor/Scientist'), ('MP', 'Medical professional'), ('HW', 'Humanitarian worker'), ('V', 'Victim/witness of HR violations'), ('OP', 'Ombudsperson/Procuraduria/NHRI'), ('GAS', 'Government/Army/Security forces'), ('I', 'Investigation against officials'), ('PC', 'Participation in conference/meeting'), ('PP', 'Participation in public protest/rally')], default='?', help_text='Select maximum 3 items with <i>Ctrl+Click</i>', max_choices=3, max_length=15),
        ),
    ]
