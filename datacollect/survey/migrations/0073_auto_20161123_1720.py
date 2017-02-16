# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-23 16:20
from __future__ import unicode_literals

from django.db import migrations
from django.db.utils import IntegrityError

def update_person_id(apps, schema_editor):
    Record = apps.get_model('survey', 'Record')

    for object in Record.objects.all():
        # Update the person ID to feature three P digits:
        id = object.person_id.split("-")
        # Find the next available person ID
        while 1:
            try:
                id[-1] = str(int(id[-1])).zfill(3)
                object.person_id = '-'.join(id)
                object.save()
                break
            except IntegrityError:
                pass

class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0072_auto_20161123_1715'),
    ]

    operations = [
        migrations.RunPython(update_person_id),
    ]