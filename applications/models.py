from django.conf import settings
from django.db import models


class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'applied', 'Applied'
        UNDER_REVIEW = 'under-review', 'Under review'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        INTERVIEW = 'interview', 'Interview'
        OFFERED = 'offered', 'Offered'
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'
        HIRED = 'hired', 'Hired'

    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    additional_info = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.APPLIED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('candidate', 'job')
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.candidate} -> {self.job} ({self.status})'


class ApplicationStatusEvent(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=15)
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['at']


class Interview(models.Model):
    class Type(models.TextChoices):
        PHONE = 'phone', 'Phone'
        VIDEO = 'video', 'Video'
        IN_PERSON = 'in-person', 'In-person'

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    scheduled_at = models.DateTimeField()
    type = models.CharField(max_length=10, choices=Type.choices)
    location_or_link = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']
