from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [path('read/', views.mark_read, name='mark_read')]
