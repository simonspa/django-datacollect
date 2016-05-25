from django.shortcuts import render
from django.views.generic import FormView
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
    template_name = "analysis.html"

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

        # Produce matrix of Gov reply vs concern
        matrix_head = "<th></th>"
        for x in Record.GOV_REPLY_CHOICES:
            matrix_head += "<th>" + x[1] + "</th>"

        matrix_body = ""
        for y in Record.CONCERN_CHOICES:
            matrix_body += "<tr><th>" + y[1] + "</th>"
            
            for x in Record.GOV_REPLY_CHOICES:
                tmp_count = 0
                for record in records:
                    tmp_count += (1 if x[0] == getattr(record,'govreply_content') and
                                  y[0] == getattr(record,'concern_expressed') else 0)
                matrix_body += "<td>" + str(tmp_count) + "</td>"
            matrix_body += "</tr>"
        
        return locals()

class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        #messages.info(self.request, 'hello http://example.com')
        return context

class MiscView(TemplateView):
    template_name = 'demo/misc.html'
