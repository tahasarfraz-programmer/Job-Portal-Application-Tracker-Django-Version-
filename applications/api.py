from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_role():
            return Application.objects.all()
        if user.role == 'employer':
            return Application.objects.filter(job__company__owner=user)
        return Application.objects.filter(candidate=user)

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        if not self.request.user.resume:
            raise ValidationError('Upload a resume before applying.')
        if Application.objects.filter(candidate=self.request.user, job=job).exists():
            raise ValidationError('You have already applied to this job.')
        serializer.save(candidate=self.request.user)
