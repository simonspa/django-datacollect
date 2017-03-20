# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-20 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0009_auto_20170320_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='followup',
            name='attention',
            field=models.IntegerField(choices=[(1, 'Definitely not'), (2, 'Rather not'), (3, 'Probably'), (4, 'For sure'), (6, "I don't know")], default=6, null=True),
        ),
        migrations.AddField(
            model_name='followup',
            name='rating',
            field=models.IntegerField(choices=[(1, 'Much worse'), (2, 'Somewhat worse'), (3, 'Not better, not worse / or alternating'), (4, 'Somewhat better'), (5, 'Much better'), (6, "I don't know")], default=6, null=True),
        ),
    ]
