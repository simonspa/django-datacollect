from django.contrib import admin
from survey.models import Record


class RecordAdmin(admin.ModelAdmin):
    list_display = ("person_id","name", "date_latest_incident", "date_intervention")
    list_filter = ("gender", "type_intervention")
    search_fields = ("name",)

admin.site.register(Record, RecordAdmin)

