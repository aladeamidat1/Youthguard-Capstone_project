from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
import re

from core.models import Company, User, UserProfile


class UserCreateSerializer(BaseUserCreateSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username','first_name','last_name','email','password','phone', 'role']
        read_only_fields = ['id', 'role']

    def get_role(self, obj):
        if obj.is_staff:
            return 'Admin'
        elif obj.is_facilitator:
            return 'Facilitator'
        elif obj.is_employer:
            return 'Employer'
        else:
            return 'Learner'

    def validate_phone(self, value):
        if value and not re.match(r'^\+?[\d\s\-\(\)]{10,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'email', 'avatar', 'date_of_birth', 'location', 'skills', 
                 'experience_level', 'linkedin_url', 'github_url', 'portfolio_url', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_skills(self, value):
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError("Skills must be at least 3 characters long.")
        return value.strip() if value else value


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='employer.id', read_only=True)
    website = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'employer', 'owner', 'website']
        read_only_fields = ['id', 'owner']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Company name must be at least 2 characters long.")
        return value.strip()