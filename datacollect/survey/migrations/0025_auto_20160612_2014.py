# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 18:14
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0024_auto_20160612_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='relevant_activities',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('CSA', 'Civil society activist'), ('TUA', 'Trade union activist'), ('RA', 'Religious association'), ('PM', 'Politician/Party member'), ('CL', 'Community leader'), ('L', 'Lawyer/Judge/Attorney'), ('J', 'Journalist/Editor'), ('A', 'Artist/Writer'), ('S', 'Student'), ('T', 'Teacher/Professor'), ('MP', 'Medical professional'), ('HW', 'Humanitarian worker'), ('V', 'Victim/witness of HR violations'), ('OP', 'Ombudsperson'), ('I', 'Investigation against officials'), ('PC', 'Participation in conference/meeting'), ('PP', 'Participation in public protest/rally')], default='?', help_text='Select maximum 3 items with <i>Ctrl+Click</i>', max_choices=3, max_length=15),
        ),
    ]
