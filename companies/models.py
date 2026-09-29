from django.conf import settings
from django.db import models


class Company(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    size = models.CharField(max_length=30, blank=True, help_text='e.g. 11-50')
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name
