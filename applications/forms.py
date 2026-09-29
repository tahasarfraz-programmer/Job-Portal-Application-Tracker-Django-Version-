from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Application, Interview


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'additional_info']
        widgets = {'cover_letter': forms.Textarea(attrs={'rows': 6}), 'additional_info': forms.Textarea(attrs={'rows': 3})}

    def clean_cover_letter(self):
        text = self.cleaned_data['cover_letter']
        if len(text.strip()) < 20:
            raise ValidationError('Cover letter must be at least 20 characters.')
        return text


class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=[c for c in Application.Status.choices if c[0] != 'withdrawn'])


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['scheduled_at', 'type', 'location_or_link', 'notes']
        widgets = {'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}), 'notes': forms.Textarea(attrs={'rows': 2})}

    def clean_scheduled_at(self):
        when = self.cleaned_data['scheduled_at']
        if when < timezone.now():
            raise ValidationError('Interview must be scheduled in the future.')
        return when
