from django.contrib import admin

from .models import Application, ApplicationStatusEvent, Interview


class HistoryInline(admin.TabularInline):
    model = ApplicationStatusEvent
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'status', 'created_at']
    list_filter = ['status']
    inlines = [HistoryInline]


admin.site.register(Interview)
