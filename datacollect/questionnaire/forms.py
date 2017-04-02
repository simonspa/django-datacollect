# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import FollowUp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div
from crispy_forms.bootstrap import TabHolder, Tab, InlineRadios, FormActions, Alert, FieldWithButtons, StrictButton
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices = settings.LANGUAGES, required=True, label=_('Change language / Cambiar el idioma / Changer la langue'))

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-5 col-md-5 col-lg-5'
        self.helper.field_class = 'col-sm-4 col-md-4 col-lg-4'
        self.helper.layout = Layout(
            FieldWithButtons(
                'language',
                StrictButton('Change language <span class="glyphicon glyphicon-refresh"></span>', type='submit', name='change_language', css_class="btn-success"),
            ),
        )


class FollowUpForm(forms.ModelForm):

    class Meta:
        model = FollowUp
        localized_fields = '__all__'
        fields = ('familiarity',
                  'rating',
                  'incident_date_1','incident_text_1',
                  'incident_date_2','incident_text_2',
                  'incident_date_3','incident_text_3',
                  'incident_date_4','incident_text_4',
                  'incident_date_5','incident_text_5',
                  'attention',
                  'intervention',
                  'impact',
                  'further_comments',
                  'want_informed',
                  'contact_again',
                  'email_address',
        )
        widgets = {
            'rating': forms.RadioSelect(),
            'familiarity': forms.RadioSelect(),
            'attention': forms.RadioSelect(),
            'intervention': forms.RadioSelect(),
            'impact': forms.Textarea(attrs={'rows': 3,
                                            'cols': 40,
                                            'style': 'height: 8em;'}),
            'incident_text_1' : forms.Textarea(attrs={'rows': 3,
                                                      'cols': 40,
                                                      'style': 'height: 8em;'}),
            'incident_text_2' : forms.Textarea(attrs={'rows': 3,
                                                      'cols': 40,
                                                      'style': 'height: 8em;'}),
            'incident_text_3' : forms.Textarea(attrs={'rows': 3,
                                                      'cols': 40,
                                                      'style': 'height: 8em;'}),
            'incident_text_4' : forms.Textarea(attrs={'rows': 3,
                                                      'cols': 40,
                                                      'style': 'height: 8em;'}),
            'incident_text_5' : forms.Textarea(attrs={'rows': 3,
                                                      'cols': 40,
                                                      'style': 'height: 8em;'}),
            'further_comments' : forms.Textarea(attrs={'rows': 3,
                                                       'cols': 40,
                                                       'style': 'height: 8em;'}),
        }

    def __init__(self, *args, **kwargs):
        super(FollowUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3 col-md-3 col-lg-3'
        self.helper.field_class = 'col-sm-9 col-md-9 col-lg-9'
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(_('1. Familiarity')),
                    css_class = 'panel-heading'
                ),
                Div(
                    HTML(_("<p>How familiar are you with the case of {{ form.instance.case.name }} in the one year period after {{ form.instance.case.date_intervention }}?</p>")),
                    'familiarity',
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('2. Development of the situation')),
                    css_class = 'panel-heading'
                ),
                Div(
                    HTML(_("<p>How would you describe the development of the case of {{ form.instance.case.name }} in the one year period after {{ form.instance.case.date_intervention }}, in light of the incidents listed above that occurred before the action of the Special Rapporteur?</p>")),
                    HTML(_("<p>We recommend you look at <a data-toggle='modal' data-target='#myModal'>this table</a> to ensure consistency in responses. The table lists various examples and explains how to rate developments of a case depending on the initial situation.</p>")),
                    'rating',
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('3. Significant incidents')),
                    css_class = 'panel-heading'
                ),
                Div(
                    HTML(_("<p>Please list all known significant incidents that occurred in the one year period after {{ form.instance.case.date_intervention }}. If there were more than 5, please concentrate on the most important ones:</p>")),
                    TabHolder(
                        Tab(
                            _('Incident #1'),
                            'incident_date_1',
                            'incident_text_1'
                        ),
                        Tab(
                            _('Incident #2'),
                            'incident_date_2',
                            'incident_text_2',
                        ),
                        Tab(
                            _('Incident #3'),
                            'incident_date_3',
                            'incident_text_3',
                        ),
                        Tab(
                            _('Incident #4'),
                            'incident_date_4',
                            'incident_text_4',
                        ),
                        Tab(
                            _('Incident #5'),
                            'incident_date_5',
                            'incident_text_5',
                        ),
                    ),
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('4. International attention')),
                    css_class = 'panel-heading'
                ),
                Div(
                    HTML(_("<p>Do you believe that the international attention given to the case of {{ form.instance.case.name }} had an impact on the development of his/her situation in the one year period after {{ form.instance.case.date_intervention }}?</p>")),
                    'attention',
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('5. Special Rapporteur\'s intervention')),
                    css_class = 'panel-heading'
                ),
                Div(
                    HTML(_("<p>Do you believe that the intervention of the Special Rapporteur had a distinguishable impact on this case (amidst broader international attention)?</p>")),
                    'intervention',
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('6. Impact of the attention')),
                    css_class = 'panel-heading'
                ),
                Div(
                    HTML(_('<p>Please provide as much detail as possible on what makes you come to your conclusion on question (4) and (5), as well as on what kind of impact the attention had (if any):</p>')),
                    'impact',
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('7. Further comments/feedback')),
                    css_class = 'panel-heading'
                ),
                Div(
                    'further_comments',
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('8. Voluntary contact information')),
                    css_class = 'panel-heading'
                ),
                Div(
                    'want_informed',
                    'contact_again',
                    'email_address',
                    HTML(_("Please note that by submitting your email address, your contact details can be connected to this case by the independent researcher carrying out the analysis. If you do not indicate your contact details, your submission will remain anonymous. If you wish to receive further information on the analysis but do not want to be connected to this case, you can write to <a href=\"mailto:info@defendersdatabase.org\">info@defendersdatabase.org</a>.")),
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-info'
            ),
            Div(
                Div(
                    HTML(_('Submission')),
                    css_class = 'panel-heading'
                ),
                Div(
                    Alert(content=_('<strong>Warning!</strong> You can only submit this form once. After your submission the link will be deactivated.'), css_class="alert-danger"),
                    HTML(_("<p>Thank you for your contribution!</p>")),
                    StrictButton(_('Submit <span class="glyphicon glyphicon-envelope"></span>'), type='submit', name='save', css_class="btn-primary"),
                    css_class = 'panel-body'
                ),
                css_class = 'panel panel-primary'
            ),
        )

    def clean(self):
        super(FollowUpForm,self).clean()
        if bool(self.cleaned_data['want_informed']) or bool(self.cleaned_data['contact_again']):
            try:
                validate_email(self.cleaned_data['email_address'])
            except ValidationError:
                raise ValidationError(_("Please fill the e-mail address field if you wish to receive information."))

    def save(self, commit=True, *args, **kwargs):
        instance = super(FollowUpForm, self).save(commit=False, *args, **kwargs)
        instance.timestamp = timezone.now()
        instance.is_answered = True
        if commit:
            instance.save()
        return instance
  
