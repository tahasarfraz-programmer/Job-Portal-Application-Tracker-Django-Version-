from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='list'),
    path('jobs/suggestions/', views.job_suggestions, name='suggestions'),
    path('jobs/<int:pk>/', views.job_detail, name='detail'),
    path('jobs/<int:pk>/save/', views.toggle_save, name='toggle_save'),
    path('jobs/<int:pk>/apply/', views.apply, name='apply'),
    path('saved/', views.saved_jobs, name='saved'),
]
