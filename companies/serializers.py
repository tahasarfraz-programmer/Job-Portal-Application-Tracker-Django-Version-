from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'industry', 'website', 'location', 'size', 'founded_year', 'logo']
