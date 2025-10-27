from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'is_approved', 'posted_at', 'created_at', 'deadline']
        read_only_fields = ['id', 'posted_at', 'created_at']