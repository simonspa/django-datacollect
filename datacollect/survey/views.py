from django.shortcuts import render
from django.views.generic import TemplateView
from survey.models import Record

# Create your views here.

def get_counts_by_gender(qs):
    counts = {}
    counts["male"] = qs.filter(gender="M").count()
    counts["female"] = qs.filter(gender="F").count()
    counts["other"] = qs.filter(gender="O").count()
    counts["unknown"] = qs.filter(gender="?").count()
    return counts

class RecordAnalysis(TemplateView):
    # The HTML template we're going to use, found in the /templates directory
    template_name = "record_analysis.html"

    def get_context_data(self, **kwargs):
        # Quick notation to access all records
        records = Record.objects.all()

        # Total counts of cases, all priority levels
        total_count = records.all().count()
        total_by_gender = get_counts_by_gender(records)

        return locals()

