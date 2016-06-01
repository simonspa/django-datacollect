from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from survey.models import Record
from django.forms import ModelForm, Textarea
from django.db.utils import IntegrityError

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=survey.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    # Write out the column names, read from first item
    writer.writerow([smart_str(field.name) for field in queryset[0]._meta.fields])

    # Loop over requested records and write out data
    for obj in queryset:
        writer.writerow([smart_str(getattr(obj,field.name)) for field in obj._meta.fields])
        
    return response
export_csv.short_description = u"Export CSV"

def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.name = u"%s (duplicate)" % object.name

        id = object.person_id.split("-")
        # Find the next available person ID
        while 1:
            try:
                if(int(id[-1]) < 99):
                    id[-1] = str(int(id[-1])+1).zfill(2)
                else:
                    id[-2] = str(int(id[-2])+1).zfill(3)
                    id[-1] = str(1)
                object.person_id = '-'.join(id)
                object.save()
                break
            except IntegrityError:
                pass
duplicate_event.short_description = u"Duplicate"


class RecordAdmin(admin.ModelAdmin):
    list_display = ("person_id","name", "country", "type_intervention", "date_intervention", "further_comments")
    list_filter = ("gender", "type_intervention","country")
    search_fields = ("name",)
    actions = [export_csv,duplicate_event] #, export_xls, export_xlsx]
    fieldsets = (
        (None, {
            'fields': ('person_id', 'ohchr_case')
        }),
        ('Case information', {
            'fields': ('country', 'date_intervention', 'type_intervention', 'joint_with', 'name', 'follow_up_case')
        }),
        ('HRD identity', {
            #'description': 'ex',
            'fields': ('gender', 'issue_area', 'relevant_activities', 'further_info', 'international_cooperation')
            }),
        ('Incident information', {
            'fields': ('location', 'name_area', 'violation_family', 'violations', 'perpetrator', 'date_incident', 'concern_expressed'),
        }),
        ('Government reply', {
            #'classes': ('collapse',),
            'fields': ('date_govreply', 'govreply_content', 'govreply_action', 'date_govaction'),
        }),
        ('Additional information', {
            #'classes': ('collapse',),
            'fields': ('further_comments',),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 2,
                   'cols': 50,
                   'style': 'height: 2em;'})},
    }

admin.site.register(Record, RecordAdmin)

