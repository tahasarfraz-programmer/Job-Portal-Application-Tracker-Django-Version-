from rest_framework import permissions, viewsets

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]
