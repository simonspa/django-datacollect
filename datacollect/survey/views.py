from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import TemplateView
from survey.models import Record, OtherRecord
import json
from django.http import HttpResponse


# Create your views here.

def get_counts_by_gender(qs):
    counts = {}
    counts["male"] = qs.filter(gender=0).count()
    counts["female"] = qs.filter(gender=1).count()
    counts["trans"] = qs.filter(gender=2).count()
    return counts

class RecordAnalysis(TemplateView):
    # The HTML template we're going to use, found in the /templates directory
    template_name = "analysis.html"

    def get_context_data(self, **kwargs):
        # Quick notation to access all records
        records = Record.objects.all()
        ngorecords = OtherRecord.objects.all()
        
        # Total counts of cases, all priority levels
        hrd_total_count = records.all().count()
        ngo_total_count = ngorecords.all().count()
        total_count = hrd_total_count + ngo_total_count
        total_by_gender = get_counts_by_gender(records)

        # Total count of communications (stripping person identifier from personID)
        commlist = []
        for record in records:
            # take first eight chars of the personID
            commlist.append(record.person_id[:9])
        # set removes duplicates, len counts length:
        hrd_comm = len(set(commlist))

        # Total count of communications (here we have one comm per database record)
        ngo_comm = len(ngorecords)
        total_comm = hrd_comm + ngo_comm

        # Count issues in categories (multiple choices possible)
        issue_body = ""
        for x in Record.ISSUE_CHOICES:
            issue_body += "<tr><th>" + x[1] + "</th>"

            tmp_count = 0
            for record in records:
                for item in getattr(record,'issue_area'):
                    tmp_count += (1 if item == x[0] else 0)
            issue_body += "<td>" + str(tmp_count) + "</td></tr>"

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

        # Produce matrix of violations vs perpetrators
        matrix2_head = "<th></th>"
        for x in Record.PERPETRATOR_CHOICES:
            matrix2_head += "<th>" + x[1] + "</th>"

        matrix2_body = ""
        for y in Record.VIOLATIONS_CHOICES:
            matrix2_body += "<tr><th>" + y[1] + "</th>"
            
            for x in Record.PERPETRATOR_CHOICES:
                tmp_count = 0
                for record in records:
                    for item in getattr(record,'violations'):
                        for item2 in getattr(record,'perpetrator'):
                            tmp_count += (1 if item == y[0] and item2 == x[0] else 0)
                col = ""
                if tmp_count > 20: col = "red"
                elif tmp_count > 10: col = "orange"
                elif tmp_count > 5: col = "yellow"
                matrix2_body += '<td class="' + col + '">' + str(tmp_count) + "</td>"
            matrix2_body += "</tr>"

        return locals()

class HomePageView(TemplateView):
    template_name = 'jsp/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

class RecordsMap(TemplateView):
    """
    A map we use to display cases in a Leaflet-based template.
    In the HTML template, we pull the cases_son views.
    """
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super(RecordsMap, self).get_context_data(**kwargs)
        return context
 
def cases_json(request):
    """
    Pull all cases.
    """
    records = Record.objects.exclude(coords=None)

    records = list(records)
    features = [record.as_geojson_dict() for record in records]

    objects = {
        'type': "FeatureCollection",
        'features': features
    }

    response = json.dumps(objects)
    return HttpResponse(response, content_type='text/json')
