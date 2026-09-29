from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        SEEKER = 'seeker', 'Job seeker'
        EMPLOYER = 'employer', 'Employer'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.SEEKER)
    email = models.EmailField(unique=True)

    # Job seeker profile fields
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True, help_text='Comma-separated')
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    preferred_job_type = models.CharField(max_length=30, blank=True)
    preferred_location = models.CharField(max_length=120, blank=True)
    expected_salary = models.PositiveIntegerField(blank=True, null=True)
    resume = models.FileField(
        upload_to='resumes/', blank=True, null=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
    )
    resume_uploaded_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.role})'
