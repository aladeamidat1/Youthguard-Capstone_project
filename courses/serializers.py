from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'facilitator', 'is_approved', 'created_at']
        read_only_fields = ['id', 'created_at']