from django import forms
from django.utils import timezone
from .models import FollowUp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button
from crispy_forms.bootstrap import TabHolder, Tab, InlineRadios, FormActions

class FollowUpForm(forms.ModelForm):

    class Meta:
      model = FollowUp
      localized_fields = '__all__'
      fields = ('rating',
                'incident_date_1','incident_text_1',
                'incident_date_2','incident_text_2',
                'incident_date_3','incident_text_3',
                'incident_date_4','incident_text_4',
                'incident_date_5','incident_text_5',
                'attention',
                'impact',
                'further_comments',
                'want_informed',
                'contact_again',
                'email_address',
      )
      widgets = {
        'rating': forms.RadioSelect(),
        'attention': forms.RadioSelect(),
      }

    def __init__(self, *args, **kwargs):
      super(FollowUpForm, self).__init__(*args, **kwargs)
      self.helper = FormHelper(self)
      self.helper.form_class = 'form-horizontal'
      self.helper.label_class = 'col-lg-3'
      self.helper.field_class = 'col-lg-8'
      self.helper.layout = Layout(
        Fieldset(
          '1. In light of these attacks before the Special Rapporteur\'s action on {{ form.instance.case.date_intervention }}, how would you describe the development of {{ form.instance.case.name }}\'s situation within one year after this date?',
          #InlineRadios('rating'),
          'rating',
        ),
        Fieldset(
          '2. Please indicate all significant incidents during that period that you are aware of (if there were more than 5, concentrate on the most important ones):',
          TabHolder(
            Tab(
              'Incident #1',
              'incident_date_1',
              'incident_text_1'
            ),
            Tab(
              'Incident #2',
              'incident_date_2',
              'incident_text_2',
            ),
            Tab(
              'Incident #3',
              'incident_date_3',
              'incident_text_3',
            ),
            Tab(
              'Incident #4',
              'incident_date_4',
              'incident_text_4',
            ),
            Tab(
              'Incident #5',
              'incident_date_5',
              'incident_text_5',
            ),

          ),
        ),
        Fieldset(
          '3. Do you believe that the international attention to {{ form.instance.case.name }}\'s case, including from the UN, did have an impact on the development of [his/her] situation during this period?',
          'attention',
          ),
        Fieldset(
          '4. Please give as much detail as possible on what makes you believe that it had (no) impact, and what kind of impact it had, if any:',
          'impact',
        ),
        Fieldset(
          '5. Further comments/feedback:',
          'further_comments',
          ),
        Fieldset(
          '6. Voluntary contact information:',
          'want_informed',
          'contact_again',
          'email_address',
        ),
        Fieldset(
          'Submission',
          HTML('<div class="alert"><strong>Warning!</strong> You can only submit this form once. After submission, the link is deactivated.</div>'),
          HTML("<p>Thank you for your contribution!</p>"),
          FormActions(
            Submit('save', 'Submit'),
          ),
        ),
      )

    def clean(self):
      super(FollowUpForm,self).clean()
      #if bool(self.cleaned_data['first_field'])== bool(self.cleaned_data['first_field']):
      #raise ValidationError("Please, fill the first or second field")

    def save(self, commit=True, *args, **kwargs):
      instance = super(FollowUpForm, self).save(commit=False, *args, **kwargs)
      instance.timestamp = timezone.now()
      instance.is_answered = True
      if commit:
        instance.save()
      return instance
      
