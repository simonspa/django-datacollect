from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic import TemplateView
from survey.models import Record, OtherRecord
import json
from django.http import HttpResponse
from collections import OrderedDict
import operator
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def get_counts_by_gender(qs):
    counts = {}
    counts["male"] = qs.filter(gender=0).count()
    counts["female"] = qs.filter(gender=1).count()
    counts["trans"] = qs.filter(gender=2).count()
    return counts

class RecordAnalysis(LoginRequiredMixin,TemplateView):
    # The HTML template we're going to use, found in the /templates directory
    template_name = "analysis.html"

    login_url = '/login/'
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

        # List of communications for all reports since 2001:
        reportlist = [1,4198,1]
        reportsum = sum(reportlist)
        progress = 100.*total_comm/reportsum
        
        # Count issues in categories (multiple choices possible)
        issues = {x[0]: 0 for x in Record.ISSUE_CHOICES}
        issues_titles = dict(Record.ISSUE_CHOICES)
        
        activities = {x[0]: 0 for x in Record.ACTIVITIES_CHOICES}
        activities_titles = dict(Record.ACTIVITIES_CHOICES)

        matrix_violations = OrderedDict([(y[0], OrderedDict([(x[0], 0) for x in Record.PERPETRATOR_CHOICES])) for y in Record.VIOLATIONS_CHOICES])
        matrix_violations_titles_x = dict(Record.PERPETRATOR_CHOICES)
        matrix_violations_titles_y = dict(Record.VIOLATIONS_CHOICES)

        matrix_activities = OrderedDict([(y[0], OrderedDict([(x[0], 0) for x in Record.ACTIVITIES_CHOICES])) for y in Record.VIOLATIONS_CHOICES])
        matrix_activities_titles_x = dict(Record.ACTIVITIES_CHOICES)
        matrix_activities_titles_y = dict(Record.VIOLATIONS_CHOICES)

        matrix_perpetrator = OrderedDict([(y[0], OrderedDict([(x[0], 0) for x in Record.GOV_REPLY_CHOICES])) for y in Record.PERPETRATOR_CHOICES])
        matrix_perpetrator_titles_x = dict(Record.GOV_REPLY_CHOICES)
        matrix_perpetrator_titles_y = dict(Record.PERPETRATOR_CHOICES)

        
        for record in records:
            for item in getattr(record,'issue_area'):
                issues[item] += 1
            for item in getattr(record,'relevant_activities'):
                activities[item] += 1
            for viol in getattr(record,'violations'):
                for perp in getattr(record,'perpetrator'):
                    matrix_violations[viol][perp] += 1
                for act in getattr(record,'relevant_activities'):
                    matrix_activities[viol][act] += 1
            for perp in getattr(record,'perpetrator'):
                gov = getattr(record,'govreply_content')
                if(gov):
                    matrix_perpetrator[perp][gov] += 1

        issues_sorted = sorted(issues.items(), key=operator.itemgetter(1), reverse=True)
        activities_sorted = sorted(activities.items(), key=operator.itemgetter(1), reverse=True)
        
        return locals()


class HomePageView(TemplateView):
    template_name = 'jsp/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

class RecordsMap(LoginRequiredMixin,TemplateView):
    """
    A map we use to display cases in a Leaflet-based template.
    In the HTML template, we pull the cases_son views.
    """
    template_name = 'map.html'
    login_url = '/login/'

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
