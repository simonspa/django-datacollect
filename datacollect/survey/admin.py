from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from survey.models import Record, OtherRecord, AIRecord
from questionnaire.models import FollowUp
from django.forms import ModelForm, Textarea
from django.db.utils import IntegrityError
from django.utils.encoding import force_bytes
from reversion.admin import VersionAdmin
from django.db import transaction

import random

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

class RelationListFilter(admin.SimpleListFilter):
    title = 'Selected for follow-up'
    parameter_name = 'has_followup'

    def lookups(self, request, model_admin):
        return (
            ('y', 'Yes'),
            ('n', 'No'),
        )

    def queryset(self, request, queryset):

        followup_y = [rec.person_id for rec in Record.objects.all() if rec.has_related_object()]
        if self.value() == 'y':
            return queryset.filter(person_id__in=followup_y)

        if self.value() == 'n':
            return queryset.exclude(person_id__in=followup_y)

class RecordAdmin(VersionAdmin):
    exclude = ("analyst",)
    list_display = ("person_id","name", "country", "type_intervention", "date_intervention", "further_comments","feedback","analyst","is_final")
    list_filter = ("is_final","gender","violation_family","business_case","type_intervention","analyst","country")
    search_fields = ("name","person_id")
    actions = [export_csv,duplicate_event,set_final,'generate_followups'] #, export_xls, export_xlsx]
    fieldsets = (
        (None, {
            'fields': (('person_id', 'ohchr_case'),)
        }),
        ('Case information', {
            'fields': ('country', 'date_intervention', 'type_intervention', 'joint_with', 'name', ('follow_up_case','regional_case'), 'earlier_coms')
        }),
        ('HRD identity', {
            #'description': 'ex',
            'fields': ('gender', 'issue_area', ('relevant_activities', 'further_info', 'foreign_national'), 'affiliation', 'international_cooperation')
            }),
        ('Incident information', {
            'fields': (('location', 'name_area'), ('violation_family','violation_family_who'), ('violations', 'perpetrator')),
        }),
        ('Further violations', {
            #'classes': ('collapse',),
            'fields': (('violations2','perpetrator2'), ('violations3','perpetrator3'), ('violations4','perpetrator4')),
        }),
        (None, {
            'fields': (('date_incident','date_incident_unspecific'),'is_released'),
        }),
        ('Government reply', {
            #'classes': ('collapse',),
            'fields': (('date_govreply','date_govreply_further'), 'govreply_content', 'govreply_action', 'date_govaction'),
        }),
        ('Additional information', {
            #'classes': ('collapse',),
            'fields': (('business_case','business_company'),('sources_number','sources_type'),('complaint_sent','complaint_received'),'further_comments','feedback','is_final'),
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

    def generate_followups(self, request, queryset):
        insert_list = []
        commlist = {}

        # Prepare:
        for obj in queryset:
            # take first nine chars of the personID and increment on new cases
            commlist[obj.person_id[:9]] = commlist.get(obj.person_id[:9], 0) + 1

        cases_selected = 0
        while (cases_selected < 100):
            # do we have options left?
            if not commlist:
                break;
        
            case, persons = random.choice(list(commlist.items()))
            #remove from commlist to avoid duplicated:
            del commlist[case]
        
            # If more than 10 persons in this case: drop
            if persons > 10:
                print "Discarding " + str(case) + ": too big (" + str(persons) + " persons)"
                continue;

            # If a follow-up already exists: drop:
            followups = FollowUp.objects.filter(case__person_id__startswith=case)
            if followups.count() > 0:
                print "Discarding " + str(case) + ": exists (" + str(followups) + ")"
                continue;

            cases_selected += 1
            print "Selecting " + str(case)
            # Get all HRD records fro this case:
            records = Record.objects.filter(person_id__startswith=case)
            for r in records:
                print "   adding " + str(r)
                insert_list.append(FollowUp(case=r))

        FollowUp.objects.bulk_create(insert_list)
        self.message_user(request, "Created new follow-up questionnaires for %s cases with %s individual persons." % (cases_selected, len(insert_list)))
    generate_followups.short_description = u"Generate 100 new follow-up questionnaires"

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


class AIRecordAdmin(VersionAdmin):
    exclude = ("analyst",)
    list_display = ("person_id", "name", "country", "date_submission", "analyst","is_final")
    list_filter = ("is_final","analyst","country")
    search_fields = ("name","person_id")
    actions = [duplicate_event,set_final]
    fieldsets = (
        (None, {
            'fields': ('person_id', 'ai_reference','pub_reference',)
        }),
        ('Complaint information', {
            'fields': ('country', 'date_submission', 'joint_with', 'name', 'case_summary')
        }),
        ('Further action(s)', {
            'fields': ('fa_title', 'fa_date', 'fa_summary')
            }),
        ('Further action(s)', {
            'classes': ('collapse',),
            'fields': ('fa_title2', 'fa_date2', 'fa_summary2','fa_title3', 'fa_date3', 'fa_summary3','fa_title4', 'fa_date4', 'fa_summary4',)
        }),
        ('Additional information', {
            #'classes': ('collapse',),
            'fields': ('further_comments','is_final'),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 5,
                   'cols': 50,
                   'style': 'height: 8em;'})},
    }

    # Automatically store the analyst user
    def save_model(self, request, obj, form, change):
        if not change:
            obj.analyst = request.user
        obj.save()


admin.site.register(Record, RecordAdmin)
admin.site.register(OtherRecord, OtherRecordAdmin)
admin.site.register(AIRecord, AIRecordAdmin)

