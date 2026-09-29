from django.contrib import admin

from .models import Category, Job, SavedJob


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'employment_type', 'posted_at']
    list_filter = ['status', 'employment_type', 'experience_level', 'work_mode']
    search_fields = ['title', 'company__name']


admin.site.register(SavedJob)
