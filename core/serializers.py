from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

from core.models import Company, User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username','first_name','last_name','email','password','phone','re_password']




class CompanySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Company
        fields = ['name', 'description', 'employer']