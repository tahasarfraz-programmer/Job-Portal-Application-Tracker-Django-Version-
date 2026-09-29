from django.urls import path

from . import views

app_name = 'companies'

urlpatterns = [
    path('mine/', views.my_company, name='mine'),
    path('<int:pk>/', views.company_detail, name='detail'),
]
