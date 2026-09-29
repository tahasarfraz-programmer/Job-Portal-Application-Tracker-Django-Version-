from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'description', 'responsibilities', 'requirements', 'skills', 'benefits',
            'experience_level', 'employment_type', 'work_mode', 'location', 'salary_min', 'salary_max',
            'deadline', 'status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 3}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
            'benefits': forms.Textarea(attrs={'rows': 3}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        lo, hi = cleaned.get('salary_min'), cleaned.get('salary_max')
        if lo is not None and hi is not None and lo > hi:
            raise ValidationError('Minimum salary cannot exceed maximum salary.')
        deadline = cleaned.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise ValidationError('Deadline cannot be in the past.')
        return cleaned


class JobSearchForm(forms.Form):
    q = forms.CharField(required=False)
    location = forms.CharField(required=False)
    category = forms.CharField(required=False)
    employment_type = forms.CharField(required=False)
    experience_level = forms.CharField(required=False)
    work_mode = forms.CharField(required=False)
    min_salary = forms.IntegerField(required=False)
    posted = forms.IntegerField(required=False)
    sort = forms.CharField(required=False)
