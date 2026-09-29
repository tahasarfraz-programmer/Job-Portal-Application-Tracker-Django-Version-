from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User

MAX_RESUME_MB = 5


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=[(User.Role.SEEKER, 'Looking for a job'), (User.Role.EMPLOYER, 'Hiring for a company')])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'photo', 'phone', 'location', 'title', 'bio',
            'skills', 'education', 'experience', 'certifications', 'linkedin', 'github',
            'website', 'preferred_job_type', 'preferred_location', 'expected_salary',
        ]
        widgets = {'bio': forms.Textarea(attrs={'rows': 4}), 'education': forms.Textarea(attrs={'rows': 3}), 'experience': forms.Textarea(attrs={'rows': 3})}


class ResumeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['resume']

    def clean_resume(self):
        f = self.cleaned_data['resume']
        if f.size > MAX_RESUME_MB * 1024 * 1024:
            raise ValidationError(f'Resume must be smaller than {MAX_RESUME_MB} MB.')
        return f
