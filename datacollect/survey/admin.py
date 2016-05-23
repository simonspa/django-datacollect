from django.contrib import admin
from django.http import HttpResponse
from survey.models import Record

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

class RecordAdmin(admin.ModelAdmin):
    list_display = ("person_id","name", "date_latest_incident", "date_intervention")
    list_filter = ("gender", "type_intervention")
    search_fields = ("name",)
    actions = [export_csv] #, export_xls, export_xlsx]

admin.site.register(Record, RecordAdmin)

