from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from questionnaire.models import FollowUp
from survey.models import Record
from django.forms import ModelForm, Textarea
from django.db.utils import IntegrityError
from django.utils.encoding import force_bytes
from reversion.admin import VersionAdmin
from django.db import transaction

def invalidate_form(modeladmin, request, queryset):
    queryset.update(is_answered=True)
invalidate_form.short_description = u"Mark selected Follow-Up form as invalid"

class FollowUpAdmin(VersionAdmin):
    list_display = ("person_id","name","country","date_intervention","unique_id","language","timestamp","is_answered",)
    list_filter = ("is_answered","language",)
    actions = [invalidate_form]

    def person_id(self, x):
        return x.case.person_id
    person_id.short_description = 'Person ID'

    def name(self, x):
        return x.case.name
    name.short_description = 'Name of HRD'

    def country(self, x):
        return x.case.country
    country.short_description = 'Country'

    def date_intervention(self, x):
        return x.case.date_intervention
    date_intervention.short_description = 'Date of the intervention'

admin.site.register(FollowUp, FollowUpAdmin)

