# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20160526_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='govreply_action',
            field=models.CharField(blank=True, choices=[('protect', 'Protection measures granted'), ('release', 'Individual released'), ('improve', 'Improved prison conditions'), ('investigate', 'Investigation opened'), ('prosecuted', 'Perpetrator suspended/prosecuted'), ('issued', 'Travel documents issued')], max_length=11, verbose_name='Government action taken according to reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='issue_area',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('WR', "Women's rights"), ('LGBTI', 'LGBTI issues'), ('IPR', "Indigenous peoples' rights"), ('HRFE', 'Housing rights/Forced evictions'), ('LNR', "Land rights/nat' res'/environment"), ('LR', 'Labour rights'), ('IF', 'Internet freedom'), ('CRS', "Children's rights"), ('HI', 'Health issues'), ('CR', 'Cultural rights'), ('RF', 'Religious freedom'), ('HRE', 'Human rights education'), ('MRR', "Migrants'/Refugees' rights"), ('MR', 'Minority rights (if not specified)'), ('AT', 'Anti-Torture'), ('PR', "Prisoner's rights"), ('ED', 'Enforced disappearance'), ('H', 'Homocide'), ('AC', 'Anti-Corruption')], default='?', help_text='Select maximum 2 items with <i>Ctrl+Click</i>', max_choices=2, max_length=10),
        ),
        migrations.AlterField(
            model_name='record',
            name='perpetrator',
            field=models.CharField(choices=[('?', 'N/A'), ('P', 'Police/security forces'), ('CS', 'Civil servant/administration'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('U', 'Unknown')], default='?', max_length=2, verbose_name='Alleged perpetrator'),
        ),
        migrations.AlterField(
            model_name='record',
            name='relevant_activities',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('L', 'Lawyer'), ('CSA', 'Civil society activist'), ('TUA', 'Trade union activist'), ('S', 'Student'), ('J', 'Journalist/Editor/Writer'), ('MP', 'Medical professional'), ('T', 'Teacher/Professor'), ('CL', 'Community leader'), ('RA', 'Religious association'), ('PM', 'Politician/Party member'), ('HW', 'Humanitarian worker'), ('V', 'Victim/witness of HR violations'), ('I', 'Investigation against officials'), ('PC', 'Participation in conference'), ('PP', 'Participation in protest/rally')], default='?', help_text='Select maximum 3 items with <i>Ctrl+Click</i>', max_choices=3, max_length=15),
        ),
        migrations.AlterField(
            model_name='record',
            name='type_intervention',
            field=models.CharField(choices=[('?', 'N/A'), ('UA', 'UA'), ('JUA', 'JUA'), ('AL', 'AL'), ('JAL', 'JAL'), ('PR', 'PR')], max_length=3, verbose_name='Type of intervention'),
        ),
        migrations.AlterField(
            model_name='record',
            name='violations',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('AD', 'Arrest/Detention'), ('P', 'Prosecution'), ('UT', 'Unfair trial'), ('C', 'Conviction'), ('K', 'Killing'), ('KA', 'Killing attempt/Assault'), ('DI', 'Diappearance/Incommunicado'), ('PC', 'Held in poor conditions'), ('RT', 'Risk of torture'), ('TI', 'Torture/Ill-treatment'), ('T', 'Threats'), ('DC', 'Defamation campaign'), ('DP', 'Disciplinary proceedings'), ('S', 'Surveillance'), ('R', 'Office/home raided'), ('B', 'Barred from travelling'), ('AH', 'Administrative harassment')], default='?', help_text='Select maximum 3 items with <i>Ctrl+Click</i>', max_choices=3, max_length=15, verbose_name='Violation(s)'),
        ),
    ]
