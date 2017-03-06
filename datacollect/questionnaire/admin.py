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

class FollowUpAdmin(VersionAdmin):
    readonly_fields = ['case']
    list_display = ("person_id","name","country","date_intervention","unique_id","language","timestamp","is_answered",)
    fieldsets = (
        ('Case information', {
            'fields': ('case',)
        }),
        ('Questionnaire', {
            'fields': ("language","timestamp","is_answered",)
    }))
    list_filter = ("is_answered","language",)
    actions = ['mark_as_answered', 'export_urls']
    
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

    def mark_as_answered(self, request, queryset):
        queryset.update(is_answered=True)
    mark_as_answered.short_description = u"Mark selected follow-up form as answered"

    def export_urls(self, request, queryset):
        import csv
        from django.utils.encoding import smart_str
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=survey.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        # Write out the column names, read from first item
        writer.writerow(['case.person_id', 'unique_id','url'])

        # Loop over requested records and write out data
        for obj in queryset:
            writer.writerow([obj.case.person_id, obj.unique_id, request.META['HTTP_HOST'] + "/submit/" + str(obj.unique_id)])
        
        return response
    export_urls.short_description = u"Export URLs"

admin.site.register(FollowUp, FollowUpAdmin)

