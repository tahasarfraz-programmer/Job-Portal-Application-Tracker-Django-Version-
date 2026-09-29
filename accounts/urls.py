from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/resume/', views.resume_upload, name='resume_upload'),
    path('profile/resume/delete/', views.resume_delete, name='resume_delete'),
    path('profile/resume/download/', views.resume_download, name='resume_download'),
    path('candidate/<int:user_id>/resume/', views.candidate_resume_download, name='candidate_resume_download'),
]
