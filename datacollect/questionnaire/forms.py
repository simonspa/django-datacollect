from django import forms
from django.utils import timezone

from .models import FollowUp

class FollowUpForm(forms.ModelForm):

    class Meta:
        model = FollowUp
        fields = ('further_comments', )

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
