from rest_framework import serializers

from companies.serializers import CompanySerializer

from .models import Category, Job


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'category', 'description', 'skills', 'experience_level',
            'employment_type', 'work_mode', 'location', 'salary_min', 'salary_max', 'deadline', 'status', 'posted_at',
        ]

    def get_skills(self, obj):
        return obj.skills_list()
