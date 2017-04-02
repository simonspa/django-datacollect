from django import forms
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from questionnaire.models import FollowUp
from questionnaire.forms import *

from django.utils import translation

class FollowUpUpdate(UpdateView):
    model = FollowUp
    form_class = FollowUpForm
    template_name_suffix = '_form'

    lang_form_class = LanguageForm

    def get_context_data(self, **kwargs):
        context = super(FollowUpUpdate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.lang_form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Handle proper submit form:
        if 'save' in request.POST:
            return super(FollowUpUpdate, self).post(request, **kwargs)
        # Handle language change:
        else:
            if 'language' in request.POST:
                translation.activate(request.POST['language'])
                self.request.session[translation.LANGUAGE_SESSION_KEY] = request.POST['language']
            url = reverse('submit-form', args=(self.object.unique_id,))
            return HttpResponseRedirect(url)

    def get_object(self, **kwargs):
        # get the uuid out of the url group and find the corresponding object
        obj = FollowUp.objects.filter(unique_id=self.kwargs.get('uuid')).first()
        if not obj or obj.is_answered:
            raise Http404("Page not found")
        else:
            if translation.LANGUAGE_SESSION_KEY not in self.request.session:
                translation.activate(obj.language)
                self.request.session[translation.LANGUAGE_SESSION_KEY] = obj.language
            return obj

    def get_success_url(self):
        return reverse('submit-success')


class FormSuccessView(TemplateView):
    template_name = 'questionnaire/success.html'
    context_object_name = 'case'
    
    def get_context_data(self, **kwargs):
        context = super(FormSuccessView, self).get_context_data(**kwargs)
        return context
