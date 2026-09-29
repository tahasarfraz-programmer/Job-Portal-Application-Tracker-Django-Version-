from django.urls import path

from . import views

app_name = 'applications'

urlpatterns = [
    path('mine/', views.tracker, name='tracker'),
    path('<int:pk>/', views.application_detail, name='detail'),
    path('<int:pk>/withdraw/', views.withdraw, name='withdraw'),
    path('<int:pk>/status/', views.update_status, name='update_status'),
    path('<int:pk>/interview/', views.schedule_interview, name='schedule_interview'),
    path('job/<int:job_id>/applicants/', views.applicants, name='applicants'),
]
