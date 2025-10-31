from rest_framework import serializers
from .models import Course, CourseEnrollment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'facilitator', 'is_approved', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Course name must be at least 3 characters long.")
        return value.strip()

    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Course description must be at least 10 characters long.")
        return value.strip()


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    learner_name = serializers.CharField(source='learner.username', read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'course', 'course_name', 'learner', 'learner_name', 'enrolled_at', 'progress', 'completed', 'completed_at']
        read_only_fields = ['id', 'enrolled_at', 'completed_at']

    def validate_progress(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Progress must be between 0 and 100.")
        return value