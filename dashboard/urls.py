from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.redirect_dashboard, name='redirect'),
    path('employer/', views.employer_dashboard, name='employer'),
    path('employer/jobs/new/', views.job_create, name='job_create'),
    path('employer/jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('employer/jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('employer/jobs/<int:pk>/toggle/', views.job_toggle, name='job_toggle'),
    path('admin-panel/', views.admin_dashboard, name='admin'),
    path('admin-panel/users/<int:pk>/toggle/', views.toggle_user, name='toggle_user'),
    path('admin-panel/users/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('admin-panel/categories/', views.manage_categories, name='categories'),
]
