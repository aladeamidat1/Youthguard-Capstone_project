from rest_framework import serializers
from .models import Job, JobApplication


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'company', 'company_name', 'title', 'description', 'job_type', 'location', 'is_approved', 'posted_at', 'created_at', 'deadline']
        read_only_fields = ['id', 'posted_at', 'created_at']

    def get_company(self, obj):
        from core.serializers import CompanySerializer
        return CompanySerializer(obj.company).data

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Job title must be at least 3 characters long.")
        return value.strip()

    def validate_description(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Job description must be at least 20 characters long.")
        return value.strip()


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    applicant_name = serializers.CharField(source='applicant.username', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'job_title', 'applicant', 'applicant_name', 'cover_letter', 'resume', 'status', 'applied_at', 'reviewed_at']
        read_only_fields = ['id', 'applied_at', 'reviewed_at']

    def validate_cover_letter(self, value):
        if len(value.strip()) < 50:
            raise serializers.ValidationError("Cover letter must be at least 50 characters long.")
        return value.strip()