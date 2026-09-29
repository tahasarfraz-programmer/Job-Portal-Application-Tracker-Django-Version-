from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'description', 'industry', 'website', 'location', 'size', 'founded_year', 'contact_email', 'linkedin', 'twitter']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
