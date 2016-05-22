from django.contrib import admin
from survey.models import Record


class RecordAdmin(admin.ModelAdmin):
    list_display = ("name", "branch", "gender", "date_of_birth")
    list_filter = ("branch", "gender")
    search_fields = ("name",)

admin.site.register(Record, RecordAdmin)

