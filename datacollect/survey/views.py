from django.shortcuts import render
from django.views.generic import TemplateView
from survey.models import Record

# Create your views here.

def get_counts_by_gender(qs):
    counts = {}
    counts["male"] = qs.filter(gender=0).count()
    counts["other"] = qs.filter(gender=1).count()
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

        # Count issues in categories (multiple choices possible)
        issue_head = ""
        issue_body = ""
        for x in Record.ISSUE_CHOICES:
            issue_head += "<th>" + x[1] + "</th>"

            tmp_count = 0
            for record in records:
                for item in getattr(record,'issue_area'):
                    tmp_count += (1 if item == x[0] else 0)
            issue_body += "<td>" + str(tmp_count) + "</td>"

        
        return locals()

