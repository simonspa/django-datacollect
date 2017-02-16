from django import forms
from django.utils import timezone
from django.http import Http404
from django.core.urlresolvers import reverse

from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from questionnaire.models import FollowUp
from questionnaire.forms import FollowUpForm


class FollowUpUpdate(UpdateView):
    model = FollowUp
    form_class = FollowUpForm
    template_name_suffix = '_form'

    def get_object(self, **kwargs):
        # get the uuid out of the url group and find the corresponding object
        obj = FollowUp.objects.filter(unique_id=self.kwargs.get('uuid')).first()
        if obj.is_answered:
            raise Http404("Page not foundt")
        else:
            return obj

    def get_success_url(self):
        return reverse('submit-success', kwargs={'person_id': self.object.case.person_id})


class FormSuccessView(TemplateView):
    template_name = 'questionnaire/success.html'
    context_object_name = 'case'
    
    def get_context_data(self, **kwargs):
        context = super(FormSuccessView, self).get_context_data(**kwargs)
        return context
