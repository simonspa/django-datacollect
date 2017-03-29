from django import forms
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import FollowUp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineRadios, FormActions, Alert
from django.utils.translation import ugettext_lazy as _

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
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                _('1. Familiarity'),
                HTML(_("<p>How familiar are you with {{ form.instance.case.name }}'s case in the period from {{ form.instance.case.date_intervention }} until one year later?</p>")),
                'familiarity',
            ),
            Fieldset(
                _('2. Development of the situation'),
                HTML(_("<p>In light of the attacks (see above) that occurred before the Special Rapporteur's action on {{ form.instance.case.date_intervention }}, how would you describe the development of {{ form.instance.case.name }}\'s situation/case <strong>within one year</strong> after this date?</p>")),
                'rating',
                HTML(_("<p>If you are not sure how to assess the case, here is a table with various examples.</p>")),
            ),
            Fieldset(
                _('3. Significant incidents'),
                HTML(_("<p>Please indicate all significant incidents during that period that you are aware of (if there were more than 5, concentrate on the most important ones):</p>")),
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
            ),
            Fieldset(
                _('4. International attention'),
                HTML(_("<p>Do you believe that the international attention to {{ form.instance.case.name }}\'s case, including from the UN, did have an impact on the development of his/her situation during this period?</p>")),
                'attention',
            ),
            Fieldset(
                _('5. Special Rapporteur\'s Intervention'),
                HTML(_("<p>Amidst the broader international attention, do you believe that the Special Rapporteur's intervention had a distinguishable impact?</p>")),
                'intervention',
            ),

            Fieldset(
                _('6. Impact of the attention'),
                HTML(_('<p>Please provide as much detail as possible on what makes you come to this conclusion, as well as on what kind of impact the attention had (if any):</p>')),
                'impact',
            ),
            Fieldset(
                _('6. Further comments/feedback:'),
                'further_comments',
            ),
            Fieldset(
                _('7. Voluntary contact information:'),
                'want_informed',
                'contact_again',
                'email_address',
                HTML(_("(Please note that by submitting your email address, your contact can be connected to this case by the independent researcher carrying out the analysis. If you don't indicate your contact details, your submission will remain anonymous. If you wish to receive further information but do not want to be connected to this case, you can write to <a href=\"mailto:info@defendersdatabase.org\">info@defendersdatabase.org</a>.)")),
            ),
            Fieldset(
                _('Submission'),
                Alert(content=_('<strong>Warning!</strong> You can only submit this form once. After submission, the link is deactivated.')),
                HTML(_("<p>Thank you for your contribution!</p>")),
                FormActions(
                    Submit('save', _('Submit')),
                ),
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
  
