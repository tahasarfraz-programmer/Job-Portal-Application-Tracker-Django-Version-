from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('applications/', include('applications.urls')),
    path('notifications/', include('notifications.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('config.api_urls')),
    path('', include('jobs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'jobs.views.error_404'
handler500 = 'jobs.views.error_500'
