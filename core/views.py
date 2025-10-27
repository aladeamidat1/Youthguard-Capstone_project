from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company
from .serializers import UserCreateSerializer, CompanySerializer

User = get_user_model()


# Create User (Registration)
User = get_user_model()

@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User created successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ✅ 2. Get Current Logged-in User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserCreateSerializer(request.user)
    return Response(serializer.data)


# ✅ 3. Create Company (Only Employers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_company(request):
    serializer = CompanySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user  # already the logged-in user

    # Only employers can create companies
    if getattr(user, "is_employer", False):  # prevent attribute error if field missing
        Company.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            employer=user
        )
        return Response({"message": "Company created"}, status=status.HTTP_201_CREATED)

    return Response({"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
