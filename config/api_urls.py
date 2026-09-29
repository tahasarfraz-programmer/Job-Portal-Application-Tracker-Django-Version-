from django.urls import include, path
from rest_framework.routers import DefaultRouter

from applications.api import ApplicationViewSet
from companies.api import CompanyViewSet
from jobs.api import CategoryViewSet, JobViewSet

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='job')
router.register('categories', CategoryViewSet, basename='category')
router.register('companies', CompanyViewSet, basename='company')
router.register('applications', ApplicationViewSet, basename='application')

urlpatterns = [path('', include(router.urls))]
