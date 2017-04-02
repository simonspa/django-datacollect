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
    list_per_page = 500
    list_display = ("person_id","name","affiliation","ohchr_case","country","date_intervention","unique_id","language","timestamp","is_answered","is_processed")
    list_editable = ("language",)
    fieldsets = (
        ('Case information', {
            'fields': ('case',)
        }),
        ('Questionnaire', {
            'fields': ("familiarity","rating",
                       "incident_date_1","incident_text_1",)
        }),
        ('Further incidents', {
            'classes': ('collapse',),
            'fields': ("incident_date_2","incident_text_2",
                       "incident_date_3","incident_text_3",
                       "incident_date_4","incident_text_4",
                       "incident_date_5","incident_text_5",
            )
        }),
        (None, {
            'fields': ("attention",
                       "intervention",
                       "impact",
                       "further_comments",)
        }),
        ('Voluntary contact information', {
            'fields': ("want_informed",
                       "contact_again",
                       "email_address",
                       )
        }),
        ('Metadata', {
            'fields': ("language","timestamp","is_answered","is_processed","internal_comments")
        })
    )
    list_filter = ("is_processed","is_answered","language")
    actions = ['mark_as_answered', 'mark_as_processed', 'mark_as_unprocessed', 'export_urls']
    
    def person_id(self, x):
        return x.case.person_id
    person_id.short_description = 'Person ID'

    def name(self, x):
        return x.case.name
    name.short_description = 'Name of HRD'

    def ohchr_case(self, x):
        return x.case.ohchr_case
    ohchr_case.short_description = 'OHCHR case no.'

    def affiliation(self, x):
        return x.case.affiliation
    affiliation.short_description = 'Affiliation'

    def country(self, x):
        return x.case.country.alpha3
    country.short_description = 'Country'

    def date_intervention(self, x):
        return x.case.date_intervention
    date_intervention.short_description = 'Date of the intervention'

    def mark_as_answered(self, request, queryset):
        queryset.update(is_answered=True)
    mark_as_answered.short_description = u"Mark selected follow-up forms as answered"

    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)
    mark_as_processed.short_description = u"Mark selected follow-up forms as processed"

    def mark_as_unprocessed(self, request, queryset):
        queryset.update(is_processed=False)
    mark_as_unprocessed.short_description = u"Mark selected follow-up forms as unprocessed"

    def export_urls(self, request, queryset):
        import csv
        from django.utils.encoding import smart_str
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=survey.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        # Write out the column names, read from first item
        writer.writerow(['case.person_id', 'case.name', 'case.ohchr_case', 'case.country', 'case.date_intervention', 'case.date_incident', 'unique_id','url', 'is_processed'])

        # Loop over requested records and write out data
        for obj in queryset:
            writer.writerow([obj.case.person_id, obj.case.name.encode('utf8'), obj.case.ohchr_case, obj.case.country.alpha3, obj.case.date_intervention, obj.case.date_incident, obj.unique_id, request.META['HTTP_HOST'] + "/submit/" + str(obj.unique_id), obj.is_processed])
        
        return response
    export_urls.short_description = u"Export URLs"

admin.site.register(FollowUp, FollowUpAdmin)

