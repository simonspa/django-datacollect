from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from survey.models import Record, OtherRecord
from django.forms import ModelForm, Textarea
from django.db.utils import IntegrityError
from django.utils.encoding import force_bytes
from reversion.admin import VersionAdmin
from django.db import transaction

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
        writer.writerow(["\"" + force_bytes(getattr(obj,field.name)) + "\"" for field in obj._meta.fields])
        
    return response
export_csv.short_description = u"Export CSV"

def set_final(modeladmin, request, queryset):
    queryset.update(is_final=True)
set_final.short_description = u"Mark selected HRD Records as final"

def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.name = u"%s (duplicate)" % object.name
        
        id = object.person_id.split("-")
        # Find the next available person ID
        while 1:
            try:
                if(int(id[-1]) < 999):
                    id[-1] = str(int(id[-1])+1).zfill(3)
                else:
                    id[-2] = str(int(id[-2])+1).zfill(4)
                    id[-1] = str(1).zfill(3)
                object.person_id = '-'.join(id)
                with transaction.atomic():
                    object.save()
                break
            except IntegrityError:
                pass
duplicate_event.short_description = u"Duplicate"

def duplicate_other_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.name = u"%s (duplicate)" % object.name
        
        id = object.case_id.split("-")
        # Find the next available case ID
        while 1:
            try:
                id[-1] = str(int(id[-1])+1).zfill(4)
                object.case_id = '-'.join(id)
                with transaction.atomic():
                    object.save()
                break
            except IntegrityError:
                pass
duplicate_other_event.short_description = u"Duplicate"


class RecordAdmin(VersionAdmin):
    exclude = ("analyst",)
    list_display = ("person_id","name", "country", "type_intervention", "date_intervention", "further_comments","feedback","analyst","is_final")
    list_filter = ("is_final","gender","business_case","type_intervention","analyst","country")
    search_fields = ("name","person_id")
    actions = [export_csv,duplicate_event,set_final] #, export_xls, export_xlsx]
    fieldsets = (
        (None, {
            'fields': (('person_id', 'ohchr_case'),)
        }),
        ('Case information', {
            'fields': ('country', 'date_intervention', 'type_intervention', 'joint_with', 'name', ('follow_up_case','regional_case'), 'earlier_coms')
        }),
        ('HRD identity', {
            #'description': 'ex',
            'fields': ('gender', 'issue_area', ('relevant_activities', 'further_info', 'foreign_national'), 'international_cooperation')
            }),
        ('Incident information', {
            'fields': (('location', 'name_area'), 'violation_family', ('violations', 'perpetrator')),
        }),
        ('Further violations', {
            #'classes': ('collapse',),
            'fields': (('violations2','perpetrator2'), ('violations3','perpetrator3')),
        }),
        (None, {
            'fields': ('date_incident',),
        }),
        ('Government reply', {
            #'classes': ('collapse',),
            'fields': ('date_govreply', 'govreply_content', 'govreply_action', 'date_govaction'),
        }),
        ('Additional information', {
            #'classes': ('collapse',),
            'fields': (('business_case','business_company'),'further_comments','feedback','is_final'),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 2,
                   'cols': 50,
                   'style': 'height: 2em;'})},
    }

    # Automatically store the analyst user
    def save_model(self, request, obj, form, change):
        if not change:
            obj.analyst = request.user
        obj.save()


class OtherRecordAdmin(VersionAdmin):
    exclude = ("analyst",)
    list_display = ("case_id","name", "case_type", "country", "type_intervention", "date_intervention", "further_comments","analyst")
    list_filter = ("type_intervention","analyst","case_type","country")
    search_fields = ("name","case_id")
    actions = [export_csv,duplicate_other_event]
    fieldsets = (
        (None, {
            'fields': (('case_id', 'ohchr_case'),)
        }),
        ('Case information', {
            'fields': ('country', 'date_intervention', 'type_intervention', 'joint_with', 'name', "case_type", ('follow_up_case','regional_case'))
        }),
        ('Additional information', {
            #'classes': ('collapse',),
            'fields': (('business_case','business_company'),'further_comments',),
        }),
    )

    
    # Automatically store the analyst user
    def save_model(self, request, obj, form, change):
        if not change:
            obj.analyst = request.user
        obj.save()


admin.site.register(Record, RecordAdmin)
admin.site.register(OtherRecord, OtherRecordAdmin)

