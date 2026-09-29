from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from .models import Category, Job
from .serializers import CategorySerializer, JobSerializer


class JobFilter(filters.FilterSet):
    class Meta:
        model = Job
        fields = {'employment_type': ['exact'], 'experience_level': ['exact'], 'work_mode': ['exact'], 'location': ['icontains'], 'category__slug': ['exact']}


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.filter(status=Job.Status.ACTIVE).select_related('company', 'category').order_by('-posted_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'skills']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
