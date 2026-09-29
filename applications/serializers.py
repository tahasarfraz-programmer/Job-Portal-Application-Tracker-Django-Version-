from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.get_full_name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'candidate', 'candidate_name', 'job', 'job_title', 'cover_letter', 'additional_info', 'status', 'created_at', 'updated_at']
        read_only_fields = ['candidate', 'status']
