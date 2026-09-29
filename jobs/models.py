from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Job(models.Model):
    class ExperienceLevel(models.TextChoices):
        ENTRY = 'entry', 'Entry level'
        MID = 'mid', 'Mid level'
        SENIOR = 'senior', 'Senior'
        LEAD = 'lead', 'Lead'

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full-time', 'Full-time'
        PART_TIME = 'part-time', 'Part-time'
        CONTRACT = 'contract', 'Contract'
        INTERNSHIP = 'internship', 'Internship'
        FREELANCE = 'freelance', 'Freelance'

    class WorkMode(models.TextChoices):
        ON_SITE = 'on-site', 'On-site'
        HYBRID = 'hybrid', 'Hybrid'
        REMOTE = 'remote', 'Remote'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    title = models.CharField(max_length=150)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    description = models.TextField()
    responsibilities = models.TextField(blank=True, help_text='One per line')
    requirements = models.TextField(blank=True, help_text='One per line')
    skills = models.CharField(max_length=500, blank=True, help_text='Comma-separated')
    benefits = models.TextField(blank=True, help_text='One per line')
    experience_level = models.CharField(max_length=10, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY)
    employment_type = models.CharField(max_length=15, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    work_mode = models.CharField(max_length=10, choices=WorkMode.choices, default=WorkMode.ON_SITE)
    location = models.CharField(max_length=120, blank=True, db_index=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    salary_max = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_at']
        indexes = [models.Index(fields=['status', 'location'])]

    def __str__(self):
        return f'{self.title} @ {self.company.name}'

    def get_absolute_url(self):
        return reverse('jobs:detail', args=[self.pk])

    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def lines(self, field):
        return [l.strip() for l in getattr(self, field).splitlines() if l.strip()]

    def is_open(self):
        return self.status == self.Status.ACTIVE and (not self.deadline or self.deadline >= timezone.now().date())


class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
